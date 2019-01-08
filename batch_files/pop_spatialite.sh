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
    sh dbshpfun.sh   ${var} 4283
done

for filename in ../shapefiles/gis*.shp; do
    [ -e "$filename" ] || continue
    thetable=$(echo $filename| cut -d'/' -f 3)
    echo $thetable
    length=${#thetable}
    endindex=$(expr $length - 4)
    echo ${thetable:0:$endindex}
    var=${thetable:0:$endindex}
    echo $var
    #echo $tablename
    sh dbshpfun.sh   ${var} 4326
done

for filename in ../csv/*.csv; do
    [ -e "$filename" ] || continue
    thetable=$(echo $filename| cut -d'/' -f 3)
    echo $thetable
    length=${#thetable}
    endindex=$(expr $length - 4)
    echo ${thetable:0:$endindex}
    var=${thetable:0:$endindex}
    echo $var
    #echo $tablename
    sh dbcsvfun.sh   ${var}
done