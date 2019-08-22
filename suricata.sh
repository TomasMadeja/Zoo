#!/bin/bash

# /home/user/qq/zoo/testfiles
# test_file_path = $1

# /testfiles/BINAlinav/BIN_Alinav5.3_4C754150639AA3A86CA4D6B6342820BE.pcap
# pcap_path = $2

# log_path = $3

echo $1
echo $2
echo $3

sudo docker run -it --privileged=true --net=host -v $3/logs:/var/log/suricata --mount src=$1,target=/testfiles,type=bind dtagdevsec/suricata:1903 suricata -c /etc/suricata/suricata.yaml -r $2 --init-errors-fatal
wait
