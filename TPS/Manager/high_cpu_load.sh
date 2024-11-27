#!/bin/bash

# Ciclo infinito para consumir intensivamente la CPU
while true; do
  echo $((13**99)) > /dev/null
done
