#!/bin/bash
fission spec init
fission env create --spec --name post-close-env --image nexus.sigame.com.br/python-env-3.8:0.0.5 --builder nexus.sigame.com.br/python-builder-3.8:0.0.2
fission fn create --spec --name post-close-fn --env post-close-env --src "./func/*" --entrypoint main.post_user_ticket --executortype newdeploy --maxscale 1
fission route create --spec --method POST --url /ticket/post_user_account_close --function post-close-fn
