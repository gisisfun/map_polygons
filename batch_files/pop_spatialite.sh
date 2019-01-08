#!/bin/bash
for filename in ../shapefiles/*.shp; do
    [ -e "$filename" ] || continue
    thetable=$(echo $filename| cut -d'/' -f 3)
    echo $thetable
    length=${#thetable}
    endindex=$(expr $length - 4)
    echo ${thetable:0:$endindex}
    var=${thetable:0:$endindex}
    echo $var
    #echo $tablename
    sh dbfun.sh   ${var}
done