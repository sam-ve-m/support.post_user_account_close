#!/bin/bash
fission spec init
fission env create --spec --name post-close-env --image nexus.sigame.com.br/python-env-3.8:0.0.5 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name post-close-fn --env post-close-env --src "./func/*" --entrypoint main.post_user_ticket
fission route create --spec --name post-close-route --method POST --url /ticket/post_user_account_close --function post-close-fn
