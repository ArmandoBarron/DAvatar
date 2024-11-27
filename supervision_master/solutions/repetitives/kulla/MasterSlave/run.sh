#!/bin/bash
# Execution command: bash run.sh -w 8 -c 1

while getopts w:c: option
do
case "${option}"
in
w) WORKERS=${OPTARG};;
c) CLEANFILES=${OPTARG};;
esac
done

# validate if flag was declared
if [ -z ${WORKERS+x} ]; 
then 
  echo "var is unset";
  echo "please add -w numberofworkers"; 
else 
  echo "var is set to '$WORKERS'"; 


echo "Press <CTRL+C> to exit."
while :
do
##  begin experiment ##
echo "begin experiment with $WORKERS workers"
  ./Master /home/MasterSlave/Volume/Source /home/MasterSlave/Volume/Sink $WORKERS
  sleep 1
  if [ ! -z ${CLEANFILES+x} ] && [[ $CLEANFILES -eq 1 ]];
  then
    rm /home/MasterSlave/Volume/Sink/*;
    sleep 1;
  fi
echo "end experiment"
##  end experiment ##
done



fi
