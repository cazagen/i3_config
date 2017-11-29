exec 3>&1;
result=$(dialog --inputbox "Hacklab Speak" 0 0 2>&1 1>&3);
exitcode=$?;
exec 3>&-;
echo $result $exitcode;
mosquitto_pub -h mqtt -t 'sound/g1/speak' -m $result
