./Dis $1 $2 $3 $4

n=$2
m=$1

dis=" ";
rec=$((n-1))


for i in `seq 0 $rec`
do
    dis=$dis"D$i "
done

./Rec $5 $3 $dis


num=$((m-1))

echo "Borrando dispersos"
for i in $(seq 0 $num);do
       rm D$i;
done