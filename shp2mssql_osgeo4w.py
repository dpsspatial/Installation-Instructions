__author__ = 'matthew_baker'
import os

#Define input SHP and database parameters:
#location of OSGEO4W:
osgeo4w = 'C:\Program Files\QGIS 2.18\OSGeo4W.bat'
#database parameters
servername = 'servername'
databasename = 'databasename'
#spatial data parameters
sourceshp = 'shp\ELECTORAL_DISTRICT.shp'
crs_source = '5320'
crs_dest = '4326'

#MSSQL Destination Table
desttable = 'schema.tablename'

##########
#build OGR2OGR statement
#as trusted connection
cmd = 'call "' + osgeo4w + '" ' \
      'ogr2ogr -skipfailures -overwrite -progress -nln ' \
       + desttable + ' -f MSSQLSpatial "MSSQL:driver={SQL Server};server=' \
      + servername +';database=' + databasename + ';trusted_connection=yes" ' \
      + sourceshp + ' -s_srs EPSG:' + crs_source + ' -t_srs EPSG:' + crs_dest + \
      ' -lco geom_name=shape -lco UPLOAD_GEOM_FORMAT=wkt'


#test OGR2OGR statement
print cmd

print "Loading PGSQL table to MSSQL"
#run command
os.system(cmd)

print "Table Loaded"

