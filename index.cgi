#! /bin/bash
echo "Content-type: text/html"
echo ""
echo "<html><head><title>Bash as CGI2</title>"
echo "<meta http-equiv='refresh' content='5'>"
echo "</head><body>"

echo "<table width='56%' align='center' border='1'>"
echo "<th>NGINX_ADDR:</th>"
echo "<th>NGINX_PORT:</th>"
echo "<th>CLIENT_ADDR:</th> "
echo "<th>CLIENT_PORT:</th> "
echo "<th>NGINX_VERSION:</th></tr>"
echo "<tr><td align='center'>$REMOTE_ADDR </td>"
echo "<td align='center'>$REMOTE_PORT</td>"
echo "<td align='center'>$HTTP_X_REAL_IP </td>"
echo "<td align='center'>$HTTP_X_FORWARDER_FOR_PORT </td>"
echo "<td align='center'>$HTTP_X_NGX_VERSION </td></tr>"
echo "</table>"

NCPU=$(lscpu | grep ^CPU\(s\) | awk '{print $2}')
CRIT=$(echo "$NCPU*2" | bc)
LAVG1=`cut -f1 -d" " /proc/loadavg`
LAVG5=`cut -f2 -d" " /proc/loadavg`
LAVG15=`cut -f3 -d" " /proc/loadavg`
avg_color () {
if [[ $(echo "$1 > $CRIT*0.9" | bc -l) -eq 1 ]]; then
OUT="<span style='color: red;'>$1</span>"
elif [[ $(echo "$1 > $CRIT*0.8" | bc -l) -eq 1 ]]; then
OUT="<span style='color: yellow;'>$1</span>"
else
OUT="<span style='color: green;'>$1</span>"
fi
echo $OUT
}

echo "<h2> Load Average: "
avg_color $LAVG1
echo ", "
avg_color $LAVG5
echo ", "
avg_color $LAVG15
echo "</h2><h1>$(cat /var/www/html/sysinfo/cronbak)</h1>"

echo "<h1>CPU</h1>"
echo "<table border='1' width='40%'>"
echo "<tr><th>Usr+nice</th><th>sys</th><th>idle</th><th>iowait</th></tr>"
echo "<tr>$(cat /var/log/mpstat.log|tail -n 1 | awk '{printf("<td>%f</td> <td>%s</td> <td>%s</td> <td>%s</td>",$3+$4, $5, $12, $6)}')</tr>"
echo "</table>" 

echo "<h1>CPU (1 minute ago)</h1>"
echo "<table border='1' width='40%'>"
echo "<tr><th>Usr+nice</th><th>sys</th><th>idle</th><th>iowait</th></tr>"
echo "<tr>$(cat /var/log/mpstat.log | tail -n 3 | head -n 1 | awk '{printf("<td>%f</td> <td>%s</td> <td>%s</td> <td>%s</td>",$3+$4, $5, $12, $6)}')</tr>"
echo "</table>" 

echo "<h1>Load Disks</h1>"
echo "<table width=80% border=1><tr><th>Device</th><th>r/s</th><th>w/s</th><th>await</th><th>%util</th></tr>"
echo "<tr>$(cat /var/log/iostat.log | tail -n 3 | awk '{printf("<td align=center>%s</td><td align=center>%.1lf</td><td align=center>%.1lf</td><td align=center>%.1lf</td><td align=center>%.1lf</td></tr>",$1, $4, $5, $10, $14)}')</table>" 

echo "<h1>Load Disks (1 min ago)</h1>"
echo "<table width=80% border=1><tr><th>Device</th><th>r/s</th><th>w/s</th><th>await</th><th>%util</th></tr>"
echo "<tr>$(cat /var/log/iostat.log | tail -n 9 | head -n 3 | awk '{printf("<td align=center>%s</td><td align=center>%.1lf</td><td align=center>%.1lf</td><td align=center>%.1lf</td><td align=center>%.1lf</td></tr>",$1, $4, $5, $10, $14)}')</table>" 


echo "<h1>Disk and Inodes info</h1>"
echo "<table width=80% border=1><tr><th>File system</th><th>%Free space</th><th>Free space</th><th>%Free inodes</th><th>Free inodes</th></tr>"  
echo "$(cat /var/log/df.log| grep -v /dev* |grep -v /proc* |grep -v /sys*  | awk ' NR>1 {printf("<tr><td align=center>%s</td><td align=center> %s</td><td align=center>%s</td><td align=center>%s</td><td align=center>%s</td></tr>",$1,(100-$2),$3,(100-$4),$5)}')</table>"

echo "<h1>TCP connection status</h1>"
echo "<pre> ESTABLISHED $(netstat | grep EST | wc -l )</pre>"
echo "<pre> SYN_SENT $(netstat | grep SYN_SENT | wc -l )</pre>"
echo "<pre> SYN_RECV $(netstat | grep SYN_RECV | wc -l )</pre>"
echo "<pre> FIN_WAIT1 $(netstat | grep FIN_WAIT1 | wc -l )</pre>"
echo "<pre> FIN_WAIT2 $(netstat | grep FIN_WAIT2 | wc -l )</pre>"
echo "<pre> CLOSE $(netstat | grep CLOSE | wc -l )</pre>" 

echo "<h1>TCP connection</h1>"
echo "<pre>$(cat /var/log/tcp.log)</pre>"

echo "<h1>UDP connection</h1>"
echo "<pre>$(cat /var/log/udp.log)</pre>"

echo "<h1>Network Loading</h1>"
echo "<table border='1' width='40%'>"
echo "<tr><th>interface</th><th>bytes_received</th><th>packet_received</th><th>bytes_transmit</th><th>packet_transmit</th></tr>"
echo "$(cat /var/log/network.log | head -n 1 | awk ' {printf("<td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td>",$1,$2,$3,$10,$11)}')</tr>
<tr>$(cat /var/log/network.log | tail -n 1 | awk ' {printf("<td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td>",$1,$2,$3,$10,$11)}')</tr></table>"


