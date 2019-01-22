
sed -e "s#changeme#${1}#g" ../spatialite_db/shpcmds_tmpl.txt >../spatialite_db/cmds.txt
cat ../spatialite_db/cmds.txt | spatialite ../spatialite_db/db.sqlite






