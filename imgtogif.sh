#!/bin/bash
# 
# Script that create a gif animation from ps file
# Usage:
#       ./imgtogif thick.s <>
#       ./imgtogif surf.w
#

#inputfiles=$1.*_*.png
#inputfiles=$(echo $1*.png | sort -n -t _ -k 2)
inputfiles=`for i in $1*.png; do echo $i; done | sort -n -t _ -k 2`

if [ $# -lt 2 ]; then
     # default name for the gif output file
     outfile="out.gif"
     if [ $# -lt 1 ]; then
 	echo "You have to give at least the basename of the inputfiles"
 	echo "thick.s : to make an animation with the slide snapshot"
 	echo "surf.w : to make an animation with the tsunami wave snaphot"
 	exit 111
     fi
else
     outfile=$2
fi

#W=`identify -format '%wx%h' map_1.png | cut -f 1 -d "x"`
#H=`identify -format '%wx%h' map_1.png | cut -f 2 -d "x"`
#echo 'Width x Height: '${W}x${H}


echo " Input files list:" ${inputfiles} 
echo ""
echo "Output file (gif): " ${outfile}
#inputfiles2=${inputfiles} | sort -n -t _ -k 2
#echo $inputfiles2

#convert -delay 50 $inputfiles -loop 0 $outfile
convert -delay 50 $inputfiles -resize 603x693 -gravity center +repage -loop 0 $outfile
if [ $? -eq  "0" ] ;then 
    echo "gif created : "$outfile
    #eog ${outfile}
    
else
    echo "someting very bad happened"
    sys 112
fi
