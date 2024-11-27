#!/bin/bash

# Incrementar consumo de memoria
declare -a array
while true; do
  array+=( $(head -c 1000000 /dev/urandom | base64) )
  echo "Consumiendo más memoria... Tamaño del array: ${#array[@]}"
  sleep 0.1
done
