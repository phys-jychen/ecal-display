#! /bin/bash
source /home/chenjiyuan/conda.env

energy=500
particle="e-"

filename="/lustre/collider/chenjiyuan/dss-ecal/run/pid/root/training/${particle}_${energy}MeV.root"
#tree=dp
event_index=2024
save_dir="/lustre/collider/chenjiyuan/ecal-display/figs/"
output="EventDisplay_${particle}_${energy}MeV.pdf"
#show=0

title="${energy}-MeV"
if [ $particle = "e-" ]
then
    title+=' $e^-$'
elif [ $particle = "mu-" ]
then
    title+=' $\mu^-$'
elif [ $particle = "pi-" ]
then
    title+=' $\pi^-$'
elif [ $particle = "e+" ]
then
    title+=' $e^+$'
elif [ $particle = "mu+" ]
then
    title+=' $\mu^+$'
elif [ $particle = "pi+" ]
then
    title+=' $\pi^+$'
elif [ $particle = "neutron" ]
then
    title+=' $n$ ('
elif [ $particle = "proton" ]
then
    title+=' $p$ ('
fi

#python event_display.py -f=$filename -i="$title" -e=$event_index -d=$save_dir -o=$output -s=$show
python event_display.py -f=$filename -i="$title" -e=$event_index -d=$save_dir -o="$output"
