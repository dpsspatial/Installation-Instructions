# Using ogr2ogr #

First, open the OSGeo4W Shell from the Windows start menu

## Loading SHP to MSSQL Server ##

Navigate to the location of the shapefile using 

`cd c:/temp/location/shp` 

Then run the following command:

    ogr2ogr -skipfailures -overwrite -nln "schema.new_table_name" -f MSSQLSpatial "MSSQL:driver={SQL Server};server=servername;database=databasename;trusted_connection=yes" "shapefile_name.shp" -s_srs EPSG:4326 -t_srs EPSG:2877 -lco geom_name=shape -lco UPLOAD_GEOM_FORMAT=wkt 

## Loading SHP to PostGIS ##

From the location of the shapefile:

    ogr2ogr -f "ESRI Shapefile" shapefile_name PG:"host=server_name user=username dbname=databasename password=******" new_table_name

## Loading PostGIS table to MSSQL Server ##

From anywhere:

    ogr2ogr -skipfailures -overwrite -nln "schema.mssql_table_name" -f MSSQLSpatial "MSSQL:driver={SQL Server};server=servername;database=mssqldatabasename;trusted_connection=yes" PG:"host=pghostname user=username dbname=pgdatabasename password=******" source_pg_tablename -s_srs EPSG:4326 -t_srs EPSG:2877 -lco GEOMETRY_NAME=shape -lco UPLOAD_GEOM_FORMAT=wkt

## Further Syntax Examples ##

To use any MSSQL tasks that require specifying a username and password (rather than a trusted_connection), use this syntax:


    "MSSQL:driver={SQL Server};server=servername;database=databasename;uid=username;pwd=password"
