size=1
day=28jul
num_objs=2000

#100mbit
sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc add dev eth1 root tbf rate 100mbit latency 50ms burst 1540" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc add dev eth1 root tbf rate 100mbit latency 50ms burst 1540" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc add dev eth1 root tbf rate 100mbit latency 50ms burst 1540" > /dev/null

sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
sshpass -p "stackme" ssh  10.30.1.5 "swift-init main restart" > /dev/null

java -jar arctur_trace_executor_fixedsize_nowait.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs &&
mv results_workload.txt results_paper/finals/results_${size}Mb_100mbit_nofilter.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc del dev eth1 root" > /dev/null


#200mbit
sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc add dev eth1 root tbf rate 200mbit latency 50ms burst 1540" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc add dev eth1 root tbf rate 200mbit latency 50ms burst 1540" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc add dev eth1 root tbf rate 200mbit latency 50ms burst 1540" > /dev/null

sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
sshpass -p "stackme" ssh  10.30.1.5 "swift-init main restart" > /dev/null

java -jar arctur_trace_executor_fixedsize_nowait.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs &&
mv results_workload.txt results_paper/finals/results_${size}Mb_200mbit_nofilter.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc del dev eth1 root" > /dev/null

#300mbit
sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc add dev eth1 root tbf rate 300mbit latency 50ms burst 1540" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc add dev eth1 root tbf rate 300mbit latency 50ms burst 1540" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc add dev eth1 root tbf rate 300mbit latency 50ms burst 1540" > /dev/null

sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
sshpass -p "stackme" ssh  10.30.1.5 "swift-init main restart" > /dev/null

java -jar arctur_trace_executor_fixedsize_nowait.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs &&
mv results_workload.txt results_paper/finals/results_${size}Mb_300mbit_nofilter.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc del dev eth1 root" > /dev/null

#500mbit
sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc add dev eth1 root tbf rate 500mbit latency 500ms burst 15400" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc add dev eth1 root tbf rate 500mbit latency 500ms burst 15400" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc add dev eth1 root tbf rate 500mbit latency 500ms burst 15400" > /dev/null

sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
sshpass -p "stackme" ssh  10.30.1.5 "swift-init main restart" > /dev/null

java -jar arctur_trace_executor_fixedsize_nowait.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs &&
mv results_workload.txt results_paper/finals/results_${size}Mb_500mbit_nofilter.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc del dev eth1 root" > /dev/null

#1gbit
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
sshpass -p "stackme" ssh  10.30.1.5 "swift-init main restart" > /dev/null

java -jar arctur_trace_executor_fixedsize_nowait.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs &&
mv results_workload.txt results_paper/finals/results_${size}Mb_1gbit_nofilter.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
