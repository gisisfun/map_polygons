
sed -e "s#changeme1#${1}#g" ../spatialite_db/shpcmds_tmpl.txt >../spatialite_db/cmds1.txt
sed -e "s#changeme2#${2}#g" ../spatialite_db/cmds1.txt >../spatialite_db/cmds.txt
cat ../spatialite_db/cmds.txt | spatialite ../spatialite_db/db.sqlite






