#!/bin/bash
#Script para ajuste de permissões da pasta de db do grafana

chown -R 472:472 grafana/dados

## Chama o gerador de chaves para o mosquitto
cd mosquitto
bash gerachaves.sh
