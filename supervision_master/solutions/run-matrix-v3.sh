#!/bin/bash
# Execution command: bash run-matrix-v3.sh -e 4 -m 2 -r 2 -p experiments/11-1-matrix/tests-dell

while getopts e:m:r:p: option
do
case "${option}"
in
e) EXPERIMENTS=${OPTARG};;
m) MINUTES=${OPTARG};;
r) REPEAT=${OPTARG};;
p) SINKPATH=${OPTARG};;
esac
done

# validate if flag was declared
if [ -z ${EXPERIMENTS+x} ];
then 
echo "please add -e numberofexperiment"; 
else 
echo "var is set to '$EXPERIMENTS'";
fi
if [ -z ${MINUTES+x} ];
then 
echo "please add -r minutesofmonitoring"; 
else 
echo "var is set to '$MINUTES'";
fi
if [ -z ${REPEAT+x} ];
then 
echo "please add -r numberofrepetitions"; 
else 
echo "var is set to '$REPEAT'";
fi
if [ -z ${SINKPATH+x} ];
then 
echo "please add -p sinkpath"; 
else 
echo "var is set to '$SINKPATH'";
fi

if [ $EXPERIMENTS = 1 ] ; then
EXPERIMENTS=sol1c1
elif [ $EXPERIMENTS = 2 ] ; then
EXPERIMENTS="sol1c1 sol1c10"
elif [ $EXPERIMENTS = 3 ] ; then
EXPERIMENTS="sol1c1 sol1c10 sol10c1"
elif [ $EXPERIMENTS = 4 ] ; then
EXPERIMENTS="sol1c1 sol1c10 sol10c1 sol10c10"
elif [ $EXPERIMENTS = 11 ] ; then
EXPERIMENTS=sol1c1
elif [ $EXPERIMENTS = 22 ] ; then
EXPERIMENTS=sol1c10
elif [ $EXPERIMENTS = 33 ] ; then
EXPERIMENTS=sol10c1
elif [ $EXPERIMENTS = 44 ] ; then
EXPERIMENTS=sol10c10
else
    echo expression default invalid option
fi

export DOCKER_CLIENT_TIMEOUT=1200
export COMPOSE_HTTP_TIMEOUT=1200
NSECONDS=$((60*$MINUTES))

# for EXP in sol1c1 sol1c10 sol10c1 sol10c10
for SOLUTION in $EXPERIMENTS
do
    # clear docker containers
    # docker system prune --force
    docker container prune --force
    docker network prune --force
    wait
    # deploy containers of the solution
    bash solutions/matrix-1-10-100/run-$SOLUTION.sh
    wait
    sleep 10
    for (( RP = 1; RP <= $REPEAT; RP++ )) ; do
        
        # make folder by solution
        OUT_FOLDER=$SINKPATH/$SOLUTION/$RP
        [ -d $OUT_FOLDER ] || mkdir -p $OUT_FOLDER
        echo "--- BEGIN $SOLUTION R $RP ---" >> $OUT_FOLDER/run-matrix.log
        
        GLOBAL_START=$(date +%s.%N)
        if [ $SOLUTION = "sol1c1" ]  || [ $SOLUTION = "sol1c10" ] ; then
            curl -G http://localhost:22010/replacesolution/$SOLUTION.yml/10/1
            sleep $NSECONDS
            curl -G http://localhost:22004/v5/aggregates/$SOLUTION.yml/END/$MINUTES/1/status-$SOLUTION-$MINUTES
            curl -G http://localhost:22003/solution/model/wot-td/status/status-$SOLUTION-$MINUTES
            GLOBAL_END=$(date +%s.%N)
            DIFF=$(echo "( $GLOBAL_END - $GLOBAL_START - $NSECONDS)" | bc)
            printf "%.6f\r\n" $DIFF >> $OUT_FOLDER/log-rt-$SOLUTION.csv
            curl -G http://localhost:22001/monitor/stop/10
            curl -G http://localhost:22010/times/gather/logs-st-$SOLUTION.csv
            cp 0_solutionmanager/src/logs-st-$SOLUTION.csv $OUT_FOLDER
            curl -X DELETE http://localhost:22002/solutions/$SOLUTION.yml/metrics/1
            
        elif [ $SOLUTION = "sol10c1" ] ; then
            for (( i = 1; i <= 10; i++ )) ; do
                curl -G http://localhost:22010/replacesolution/sol${i}c1.yml/10/1
            done
            sleep $NSECONDS
            for (( i = 1; i <= 10; i++ )) ; do
                curl -G http://localhost:22004/v5/aggregates/sol${i}c1.yml/END/$MINUTES/1/status-sol${i}c1-$MINUTES
                curl -G http://localhost:22003/solution/model/wot-td/status/status-sol${i}c1-$MINUTES
            done
            GLOBAL_END=$(date +%s.%N)
            DIFF=$(echo "( $GLOBAL_END - $GLOBAL_START - $NSECONDS)" | bc)
            printf "%.6f\r\n" $DIFF >> $OUT_FOLDER/log-rt-$SOLUTION.csv
            curl -G http://localhost:22001/monitor/stop/10
            curl -G http://localhost:22010/times/gather/logs-st-$SOLUTION.csv
            cp 0_solutionmanager/src/logs-st-$SOLUTION.csv $OUT_FOLDER
            for (( i = 1; i <= 10; i++ )) ; do
                curl -X DELETE http://localhost:22002/solutions/sol${i}c1.yml/metrics/1
            done

        elif [ $SOLUTION = "sol10c10" ] ; then
            for (( i = 1; i <= 10; i++ )) ; do
                curl -G http://localhost:22010/replacesolution/sol${i}c10.yml/10/1
            done
            sleep $NSECONDS
            for (( i = 1; i <= 10; i++ )) ; do
                curl -G http://localhost:22004/v5/aggregates/sol${i}c10.yml/END/$MINUTES/1/status-sol${i}c10-$MINUTES
                curl -G http://localhost:22003/solution/model/wot-td/status/status-sol${i}c10-$MINUTES
            done
            GLOBAL_END=$(date +%s.%N)
            DIFF=$(echo "( $GLOBAL_END - $GLOBAL_START - $NSECONDS)" | bc)
            printf "%.6f\r\n" $DIFF >> $OUT_FOLDER/log-rt-$SOLUTION.csv
            curl -G http://localhost:22001/monitor/stop/10
            curl -G http://localhost:22010/times/gather/logs-st-$SOLUTION.csv
            cp 0_solutionmanager/src/logs-st-$SOLUTION.csv $OUT_FOLDER
            for (( i = 1; i <= 10; i++ )) ; do
                curl -X DELETE http://localhost:22002/solutions/sol${i}c1.yml/metrics/1
            done
            
        else
            echo expression default
        fi
        echo "--- END $SOLUTION R $RP ---" >> $OUT_FOLDER/run-matrix.log
        echo "--- CLEAN SERVICE LOGS $SOLUTION R $RP ---" >> $OUT_FOLDER/run-matrix.log
        curl -X DELETE http://localhost:22010/times/clear
    done

    bash solutions/matrix-1-10-100/down-$SOLUTION.sh
    wait
done
