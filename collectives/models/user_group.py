""" Handle dynamic user groups, for restricting or payment options """
from asyncio import events
import enum
from typing import List

from sqlalchemy import and_, or_, true

from collectives.models.globals import db

from collectives.models.role import RoleIds, Role
from collectives.models.user import User
from collectives.models.event import Event


class GroupRoleCondition(db.Model):
    """Relationship indicating that group members must have a certain role"""

    __tablename__ = "group_role_conditions"

    id = db.Column(db.Integer, primary_key=True)
    """Database primary key

    :type: int"""

    group_id = db.Column(
        db.Integer, db.ForeignKey("user_groups.id"), nullable=False, index=True
    )
    """ ID of the group this condition applies to

    :type: int"""

    role_id = db.Column(
        db.Enum(RoleIds),
        nullable=True,
        info={"choices": RoleIds.choices(), "coerce": RoleIds.coerce, "label": "Rôle"},
    )
    """ Id of the role that group members must have. If null, any role is allowed

    :type: :py:class:`collectives.models.RoleId``
    """

    activity_id = db.Column(
        db.Integer, db.ForeignKey("activity_types.id"), nullable=True
    )
    """ ID of the activity to which the user role should relate to. If null, any activity is allowed

    :type: int"""

    def get_condition(self):
        """:returns: the SQLAlchemy expression corresponding to this condition"""
        if self.role_id and self.activity_id:
            return User.roles.any(and_(Role.role_id == self.role_id, Role.activity_id == self.activity_id))
        if self.role_id:
            return Role.role_id == self.role_id
        if self.activity_id:
            Role.activity_id == self.activity_id
        return true

class GroupEventCondition(db.Model):
    """Relationship indicating that group members must participate (or lead) a given event."""

    __tablename__ = "group_event_conditions"

    id = db.Column(db.Integer, primary_key=True)
    """Database primary key

    :type: int"""

    group_id = db.Column(
        db.Integer, db.ForeignKey("user_groups.id"), nullable=False, index=True
    )
    """ ID of the group this condition applies to

    :type: int"""

    event_id = db.Column(
        db.Integer, db.ForeignKey("activity_types.id"), nullable=False
    )
    """ ID of the activity to which the user role should relate to. 

    :type: int"""

    is_leader = db.Column(
        db.Boolean, nullable=True
    )
    """ Whether group members should be leaders of the activity or normal users.
    If null, both are allowed.

    :type: int"""

    def get_condition(self):
        """:returns: the SQLAlchemy expression corresponding to this condition"""
        if self.is_leader is None:
            return or_(User.events.any(Event.id == self.event_id), User.led_events.any(Event.id == self.event_id) )
        if self.is_leader:
            return User.led_events.any(Event.id == self.event_id)

        return User.events.any(Event.id == self.event_id)

class GroupLicenseCondition(db.Model):
    """Relationship indicating that group members must have a certain license type"""

    id = db.Column(db.Integer, primary_key=True)
    """Database primary key

    :type: int"""

    group_id = db.Column(
        db.Integer, db.ForeignKey("user_groups.id"), nullable=False, index=True
    )
    """ ID of the group this condition applies to

    :type: int"""

    license_category = db.Column(db.String(2), info={"label": "Catégorie de licence"})
    """ User club license category.

    :type: string (2 char)"""


class UserGroup(db.Model):
    """ Dynamically-defined set of users based on various conditions.

        Currently three type of conditions are available:

         - Role: User must have a specific role, optionnaly for a given activity
         - Event: User must be registered or be a leader to a given event
         - Licence: Use must have a specific licence type

        Those conditions are multiplicative, i.e. the user must satisfy all conditions ("and").
        However, within each condition, allowed values are additive ("or")
        All three types of conditions are also optional.

        For instance, a user group may be defined as follow:
        Users which have ((the role President) or (the role Leader for activity "Ski")) 
        and ((lead event "Foo") or (are registered to event "Bar"))
        
    """
    
    id = db.Column(db.Integer, primary_key=True)
    """Database primary key

    :type: int"""

    role_conditions = db.relationship("GroupRoleConditions", backref="group", cascade="all, delete")
    """ List of role conditions associated with this group

    :type: list(:py:class:`collectives.models.user_group.GroupRoleCondition`)
    """

    event_conditions = db.relationship("GroupEventConditions", backref="group", cascade="all, delete")
    """ List of event conditions associated with this group

    :type: list(:py:class:`collectives.models.user_group.GroupRoleCondition`)
    """

    license_conditions = db.relationship("GroupLicenceConditions", backref="group", cascade="all, delete")
    """ List of license conditions associated with this group

    :type: list(:py:class:`collectives.models.user_group.GroupRoleCondition`)
    """


    def get_members(self) -> List[User]:
        """:return: the list of group members
        """
        query  = User.query

        if self.role_conditions:
            roles = [role.get_condition() for role in self.role_conditions]
            query = query.filtee(or_(*roles))
       
        if self.event_conditions:
            events = [event.get_condition() for event in self.event_conditions]
            query = query.filtee(or_(*events))

        if self.license_conditions:
            categories = [condition.license_category for condition in self.license_conditions]
            query = query.filter( User.license_category in categories)
