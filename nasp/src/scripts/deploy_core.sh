DIR="../helm_charts/free5gc"
grep -rl "sst: 1" $DIR | xargs sed -i 's/sst: 1/sst: 2/g'
helm install core $DIR -n free5gc