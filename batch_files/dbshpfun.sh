
sed -e "s#changeme1#${1}#g" ../spatialite_db/shpcmds_tmpl >../spatialite_db/cmds1
sed -e "s#changeme2#${2}#g" ../spatialite_db/cmds1 >../spatialite_db/cmds
cat ../spatialite_db/cmds | spatialite ../spatialite_db/db.sqlite






