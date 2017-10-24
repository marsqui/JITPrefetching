size=10
day=16oct
num_objs=2000

#upload
# java -jar arctur_trace_executor_fixedsize.jar -o WRITE -t arctur -sm $(($size * 1024*1024)) -m 1 -no $num_objs
# mv results_workload.txt results/results_put_${size}Mb_${date}.txt

# sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc del dev eth1 root" > /dev/null
# sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc del dev eth1 root" > /dev/null
# sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc del dev eth1 root" > /dev/null

# #100mbit
# sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc add dev eth1 root tbf rate 100mbit latency 500ms burst 15400" > /dev/null
# sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc add dev eth1 root tbf rate 100mbit latency 500ms burst 15400" > /dev/null
# sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc add dev eth1 root tbf rate 100mbit latency 500ms burst 15400" > /dev/null

# sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
# sshpass -p "stackme" ssh  10.30.1.5 "swift-init main restart" > /dev/null

# sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
# java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
# sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog | grep served" > results_paper/log_${size}Mb_100mbit_1st_${day}.txt
# mv results_workload.txt results_paper/${size}Mb_100mbit_1st_${day}.txt
# sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

# sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
# java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
# sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog | grep served" > results_paper/log_${size}Mb_100mbit_2nd_${day}.txt
# mv results_workload.txt results_paper/${size}Mb_100mbit_2nd_${day}.txt
# sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

# sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
# java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
# sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog | grep served" > results_paper/log_${size}Mb_100mbit_3rd_${day}.txt
# mv results_workload.txt results_paper/${size}Mb_100mbit_3rd_${day}.txt

# sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc del dev eth1 root" > /dev/null
# sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc del dev eth1 root" > /dev/null
# sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc del dev eth1 root" > /dev/null

# #200mbit
# sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc add dev eth1 root tbf rate 200mbit latency 500ms burst 15400" > /dev/null
# sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc add dev eth1 root tbf rate 200mbit latency 500ms burst 15400" > /dev/null
# sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc add dev eth1 root tbf rate 200mbit latency 500ms burst 15400" > /dev/null

# sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
# sshpass -p "stackme" ssh  10.30.1.5 "swift-init main restart" > /dev/null

# sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
# java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
# sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog | grep served" > results_paper/log_${size}Mb_200mbit_1st_${day}.txt
# mv results_workload.txt results_paper/${size}Mb_200mbit_1st_${day}.txt
# sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

# sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
# java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
# sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog | grep served" > results_paper/log_${size}Mb_200mbit_2nd_${day}.txt
# mv results_workload.txt results_paper/${size}Mb_200mbit_2nd_${day}.txt
# sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

# sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
# java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
# sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog | grep served" > results_paper/log_${size}Mb_200mbit_3rd_${day}.txt
# mv results_workload.txt results_paper/${size}Mb_200mbit_3rd_${day}.txt

sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc del dev eth1 root" > /dev/null

#300mbit
sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc add dev eth1 root tbf rate 300mbit latency 50ms burst 1540"
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc add dev eth1 root tbf rate 300mbit latency 50ms burst 1540"
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc add dev eth1 root tbf rate 300mbit latency 50ms burst 1540"

sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
sshpass -p "stackme" ssh  10.30.1.5 "swift-init main restart" > /dev/null

sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog |grep served" > results_paper/log_${size}Mb_300mbit_1st_${day}.txt
mv results_workload.txt results_paper/${size}Mb_300mbit_1st_${day}.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog |grep served" > results_paper/log_${size}Mb_300mbit_2nd_${day}.txt
mv results_workload.txt results_paper/${size}Mb_300mbit_2nd_${day}.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog |grep served" > results_paper/log_${size}Mb_300mbit_3rd_${day}.txt
mv results_workload.txt results_paper/${size}Mb_300mbit_3rd_${day}.txt

sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc del dev eth1 root" > /dev/null

#500mbit
sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc add dev eth1 root tbf rate 500mbit latency 500ms burst 15400" > /dev/null
sshpass -p "stackme" ssh  10.30.1.25 "tc qdisc add dev eth1 root tbf rate 500mbit latency 500ms burst 15400" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc add dev eth1 root tbf rate 500mbit latency 500ms burst 15400" > /dev/null

sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
sshpass -p "stackme" ssh  10.30.1.5 "swift-init main restart" > /dev/null

sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog |grep served" > results_paper/log_${size}Mb_500mbit_1st_${day}.txt
mv results_workload.txt results_paper/${size}Mb_500mbit_1st_${day}.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog |grep served" > results_paper/log_${size}Mb_500mbit_2nd_${day}.txt
mv results_workload.txt results_paper/${size}Mb_500mbit_2nd_${day}.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog |grep served" > results_paper/log_${size}Mb_500mbit_3rd_${day}.txt
mv results_workload.txt results_paper/${size}Mb_500mbit_3rd_${day}.txt

sshpass -p "stackme" ssh  10.30.1.24 "tc qdisc del dev eth1 root" > /dev/null
shpass -p "stackme" ssh  10.30.1.25 "tc qdisc del dev eth1 root" > /dev/null
sshpass -p "stackme" ssh  10.30.1.26 "tc qdisc del dev eth1 root" > /dev/null

#1gbit
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"
sshpass -p "stackme" ssh  10.30.1.5 "swift-init main restart" > /dev/null

sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog |grep served" > results_paper/log_${size}Mb_1gbit_1st_${day}.txt
mv results_workload.txt results_paper/${size}Mb_1gbit_1st_${day}.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog |grep served" > results_paper/log_${size}Mb_1gbit_2nd_${day}.txt
mv results_workload.txt results_paper/${size}Mb_1gbit_2nd_${day}.txt
sshpass -p "stackme" ssh  10.30.1.5 "echo 3 > /var/log/syslog"

sshpass -p "stackme" ssh 10.30.1.5 "./scripts_bsc/drop_caches.sh"
java -jar arctur_trace_executor_fixedsize.jar -o READ -t arctur -sm $(($size * 1024*1024)) -no $num_objs
sshpass -p "stackme" ssh  10.30.1.5 "cat /var/log/syslog |grep served" > results_paper/log_${size}Mb_1gbit_3rd_${day}.txt
mv results_workload.txt results_paper/${size}Mb_1gbit_3rd_${day}.txt
