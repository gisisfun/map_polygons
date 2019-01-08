
sed -e "s#changeme#${1}#g" ../spatialite_db/cmds_tmpl >../spatialite_db/cmds
cat ../spatialite_db/cmds | spatialite ../spatialite_db/db.sqlite






