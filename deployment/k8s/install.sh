#!/usr/bin/bash

if [[ $EUID -ne 0 ]];
then
    exec sudo /bin/bash "$0" "$@"
fi

snap install microk8s --classic
usermod -a -G microk8s ubuntu
microk8s enable ingress
microk8s enable cert-manager
microk8s enable cis-hardening

microk8s status 


echo TODO: mettre à jour le yaml avec le hostname