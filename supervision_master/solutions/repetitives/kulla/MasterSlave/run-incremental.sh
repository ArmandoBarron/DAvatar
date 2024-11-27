#!/bin/bash
# Execution command: bash run-incremental.sh -w 8 -c 1

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

##  begin experiment ##
echo "begin experiment 1-$WORKERS workers repeat 1 times each one"

for (( i = 1; i <= $WORKERS; i++ ))
do
  echo "exp $i workers"
  # for (( j = 1; j <= 10; j++ ))
  # do
    ./Master /home/Volume/Source /home/Volume/Sink $i
    sleep 1
  # done
  if [ ! -z ${CLEANFILES+x} ];
  then
    rm /home/Volume/Sink/*;
    sleep 1;
  fi
done



echo "end experiment"
##  end experiment ##

fi
