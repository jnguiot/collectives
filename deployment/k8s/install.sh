#!/usr/bin/bash
sudo snap install microk8s --classic
sudo microk8s enable ingress
sudo microk8s enable cert-manager


sudo usermod -a -G microk8s ubuntu

sudo microk8s status # to check whether intsalled or not


wget https://raw.githubusercontent.com/Club-Alpin-Annecy/collectives/docker/deployment/k8s/collectives.yaml

sudo microk8s kubectl apply -f collectives.yaml