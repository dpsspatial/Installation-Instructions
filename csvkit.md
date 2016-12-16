##Using CSVKit to load CSV files into PostGIS##

This tutorial will show how to load a large CSV file into PostgreSQL and turn the LAT/LON columns into geometry using CSVKit.

CSVKit is a utility used at command line / terminal and installed via Python.

Not only is CSVKit the best way to generate a SQL 'create table' expression from your CSV file (accurately determines the column types based on the data in the table), it allows you to directly load a CSV using that column definition AND the super-fast PostgreSQL COPY tool all in one command.

*A lot of this is based on the [Eleven Awesome Things you can do with CSVKit](https://source.opennews.org/en-US/articles/eleven-awesome-things-you-can-do-csvkit/) article.*

**Installing CSVKit**

While in command line / terminal:

    pip install csvkit 

*Note: this requires PIP for Python to be installed*

**Inspect a CSV**

Next browse to a folder where you have a CSV loaded, for me in my Downloads folder. I will use the City and County of Denver Crimes dataset which you can [download for free](https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-crime).

The downloaded file is called **crime.csv**

Use CSVKit to inspect the data and column types:

    csvstat crime.csv

Since this is a large dataset, it may take a few minutes to run.

The output gives a summary of each column of data in the CSV. Here's a sample of the first column: 

      1. INCIDENT_ID
    <type 'float'>
    Nulls: False
    Min: 20111.0
    Max: 2.01414951534e+12
    Sum: 1.80117318226e+15
    Mean: 3996399331.39
    Median: 2014379750.0
    Standard Deviation: 8147580639.94
    Unique values: 419339
    5 most frequent values:
    2016233674.0:   8
    201530686.0:6
    2013409529.0:   6
    2011180275.0:   6
    2016134777.0:   6

Next, you can get a SQL table definition from the CSV file (but don't run the SQL command, we'll load it all in the next step):

    csvsql -i postgresql crime.csv

*Note: I've added a flag to specify I want the SQL syntax in PostgreSQL format. You can get [all the database types here](http://csvkit.readthedocs.io/en/latest/scripts/csvsql.html).* 

Again, since this is a big file, it will take a few moments to run. 

The output will give us a SQL statement that can be used to create an empty table in PostgreSQL (but don't do this yet):

    CREATE TABLE crime (
	    "INCIDENT_ID" FLOAT NOT NULL,
	    "OFFENSE_ID" BIGINT NOT NULL,
	    "OFFENSE_CODE" VARCHAR(4) NOT NULL,
	    "OFFENSE_CODE_EXTENSION" INTEGER NOT NULL,
	    "OFFENSE_TYPE_ID" VARCHAR(30) NOT NULL,
	    "OFFENSE_CATEGORY_ID" VARCHAR(28) NOT NULL,
	    "FIRST_OCCURRENCE_DATE" TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	    "LAST_OCCURRENCE_DATE" TIMESTAMP WITHOUT TIME ZONE,
	    "REPORTED_DATE" TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	    "INCIDENT_ADDRESS" VARCHAR(97),
	    "GEO_X" FLOAT NOT NULL,
	    "GEO_Y" FLOAT NOT NULL,
	    "GEO_LON" FLOAT,
	    "GEO_LAT" FLOAT,
	    "DISTRICT_ID" INTEGER,
	    "PRECINCT_ID" INTEGER,
	    "NEIGHBORHOOD_ID" VARCHAR(26),
	    "IS_CRIME" INTEGER NOT NULL,
	    "IS_TRAFFIC" INTEGER NOT NULL
    );

Again, the next step will show how to load the data with the correct schema definition in one command. Otherwise, you could take that SQL statement, run it in the database, then use the Import / COPY command to load your CSV. 

**Load the CSV into PostgreSQL**

Next, we'll load the data into the PostgreSQL database in one easy command skipping the CSVSQL command above and the COPY step.

This is the syntax to specify the database to connect to, the name of the table to create, and the csv file you want to load: 

    csvsql --db postgresql://username:password@servername/databasename --table denver_crime --insert crime.csv

Again, this is a large dataset, but when complete, open up PGAdmin and see the new table:

![](https://raw.githubusercontent.com/dpsspatial/Images/master/denver_crime_table.PNG)

**Create Geometry from Lat/Lon**

The table we created from the CSV doesn't have a geometry column, instead it comes with the LAT and LON values in both State Plane (GEO_X, GEO_Y) and WGS84 (GEO_LON, GEO_LAT).

Using the a couple of spatial functions, we can turn the GEO_LON and GEO_LAT columns into geometry in WGS84 (SRID: 4326)

First, our denver_crime table needs a geometry column. In the PGAdmin SQL window, run:

    alter table denver_crime add geom geometry(point, 4326);

Then, fill the empty geometry column up with a geometry object built from the GEO_LON and GEO_LAT columns:

    UPDATE denver_crime set geom = ST_SetSRID(ST_MakePoint("GEO_LON", "GEO_LAT"), 4326)

The above SQL uses the [ST_MakePoint](http://postgis.net/docs/ST_MakePoint.html) to assemble a geometry object from the two columns. Then, wrap that with the [ST_SetSRID](http://postgis.net/docs/ST_SetSRID.html) function to set the spatial reference of the points to 4326 (WGS84).

The denver_crime table now has geometry in the geom column, so you can now view the points in QGIS:

![](https://github.com/dpsspatial/Images/blob/master/denver_crime_map.png?raw=true)
