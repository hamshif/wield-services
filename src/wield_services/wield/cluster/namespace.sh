#!/usr/bin/env bash

# TODO make this work or delete it
#
#kubectl config set-context wielder-services --namespace=wielder-services \
#  --cluster=docker-for-desktop-cluster \
#  --user=docker-for-desktop


kubectl config set-context wielder-services --namespace=wielder-services \
  --cluster=docker-desktop-cluster \
  --user=docker-desktop
