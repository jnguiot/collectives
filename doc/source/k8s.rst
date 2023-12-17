Deployment on Kubernetes
==========================

This document is meant to help the deployment of the collectives application on Kubernetes. 
However, don't hesitate to adapt scripts and definitions to your own needs


How to install collectives on a Kubernetes
---------------------------------------------

For this How To, we will explain an OVH installation. But you can deploy the app on other
providers.

.. warning::
  Please note that you have to keep an informed eye  while performing thoses indications. 
  CAF Annecy or the collectives project cannot and will not be held accountable for any 
  dommages or costs that may occurs from this how to.


Requirements : `kubectl <https://kubernetes.io/fr/docs/tasks/tools/install-kubectl/>`_ and 
`helm <https://helm.sh/docs/intro/install/>`_ 

#. Go to OVH and purchase a Public Cloud Managed Kubernetes. Cheapest with one node is OK.
#. Setup collectives.yaml by copy `deployment/k8s/collectives.exemple.yaml`` with your 
   hostnames and secrets: look for the 4 `--to-be-replaced--`
#. Download the `kubeconfig.yml` file, and set it up for kubectl and helm
#. Install `cert-manager <https://help.ovhcloud.com/csm/en-public-cloud-kubernetes-install-cert-manager?id=kb_article_view&sysparm_article=KB0049779>`_ 
   and `nginx ingress <https://help.ovhcloud.com/csm/fr-public-cloud-kubernetes-secure-nginx-ingress-cert-manager?id=kb_article_view&sysparm_article=KB0055580>`_ : 

   .. code-block:: bash

     helm repo add jetstack https://charts.jetstack.io
     helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
     helm repo update 
     helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set installCRDs=true
     helm -n ingress-nginx install ingress-nginx ingress-nginx/ingress-nginx --create-namespace

#. Get the external IP with ``kubectl get svc -n ingress-nginx ingress-nginx-controller`` and setup your DNS record
#. Apply collectives.yaml ``kubectl apply -f collectives.yaml`` 
#. After a while, the website should be available on `https://your-hostname.com`

.. warning::
  The file `collectives.yaml` contains secrets and it should not be shared publicly!!

How does it works?
---------------------

`nginx <https://www.nginx.com/>`_ is used as an ingress.

It automatically loads a `Let's Encrypt <https://letsencrypt.org/fr/>`_ free certificate for TLS.

It works with the `collectives <https://hub.docker.com/repository/docker/cafannecy/collectives/general>`_ docker
published by the `CAF Annecy <https://www.cafannecy.fr/>`_.

Data persistence is achieved by :

- block storages for files
- a Kubernetes instance of `MariaDB <https://mariadb.org/>`_ for database, itself using block storage.
- object storage for mysql backup.

No auto-scaling, replication, or load balancing is configured.

Backup can be achieved by leveraging the 
`volume backup <https://help.ovhcloud.com/csm/fr-public-cloud-storage-volume-backup?id=kb_article_view&sysparm_article=KB0057449>`
functionnality of the public cloud. However, I don't know how to automate it.