
sed -e "s#changeme1#${1}#g; s#changeme2#${2}#g; s#changeme3#${3}#g" ../spatialite_db/shpcmds_tmpl.txt >../spatialite_db/cmds.txt
cat ../spatialite_db/cmds.txt | spatialite ../spatialite_db/${3}.sqlite






