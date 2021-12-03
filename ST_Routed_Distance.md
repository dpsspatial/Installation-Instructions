## Create Custom Routing Functions using OSRM

The ST_Routed_Distance() and ST_Routed_Line() functions use the OSRM routing server and the Postgresql HTTP Client to return a routed distance and geometry from two input geometries. We use this instead of PGRouting because we process 10's of thousands of routes (students, bus routes, etc.) and we are fine using OpenStreetMap as it is a good source of regional street network data (vs. using the City and County of Denver Street Centerline file) 

### Set Up OSRM Server

http://project-osrm.org/

We use Docker to run the OSRM server. 

### Install PostgreSQL HTTP Client

Follow the instructions provided by Paul Ramsey posted here: 

https://github.com/pramsey/pgsql-http

Note the creation of the http_get() SQL function, which will be used below. 

### Create ST_Routed_Distance() 

    CREATE OR REPLACE FUNCTION public.st_routed_distance(g_start geometry, g_finish geometry, exclude_value character varying DEFAULT 'ferry'::character varying)
     RETURNS double precision
     LANGUAGE sql
     COST 10000
    AS $function$
    SELECT  (http_get(
               'http://server-name:5000/route/v1/driving/' ||
               ST_X(ST_Transform(g_start, 4326)) || ',' || ST_Y(ST_Transform(g_start, 4326)) ||';' ||
               ST_X(ST_Transform(g_finish, 4326)) || ',' || ST_Y(ST_Transform(g_finish, 4326)) ||
               '?geometries=geojson&overview=false&alternatives=false&steps=false&exclude='|| exclude_value)::jsonb -> 'routes' -> 0 ->
           'distance')::text::float * 0.000621371
    $function$
    ;

Notes: 

- The function includes the exclude_value parameter, giving the ability to omit types of streets/lines in the routing. Be default, 'ferry' lines are excluded. Using this parameter is outlined below; 
- The URL to the OSRM server points to the DRIVING profile, you can also other profiles such as WALKING, etc.


### Create ST_Routed_Line() 

    CREATE OR REPLACE FUNCTION public.st_routed_line(g_start geometry, g_finish geometry, exclude_value character varying DEFAULT 'ferry'::character varying)
     RETURNS geometry
     LANGUAGE sql
     COST 10000
    AS $function$
    SELECT ST_GeomFromGeoJSON((http_get(
               'http://server-name:5000/route/v1/driving/' ||
               ST_X(ST_Transform(g_start, 4326)) || ',' || ST_Y(ST_Transform(g_start, 4326)) ||';' ||
               ST_X(ST_Transform(g_finish, 4326)) || ',' || ST_Y(ST_Transform(g_finish, 4326)) ||
               '?geometries=geojson&overview=full&alternatives=false&steps=false&exclude='|| exclude_value) :: jsonb -> 'routes' -> 0 ->
               'geometry'
            )::text) --::text **Put that between the )) if PG complains about jsonb
    $function$
    ;

### Using Custom Functions

A typical use case for us would be something like this:

    select
        stu.studentnumber
        , ST_Routed_Distance(
            stu.geom
            , sch.geom
        )
    from
        dpsdata."Active_Students" as stu
    join dpsdata."Schools_Current" as sch on
        stu.schnum = sch.schnum
    where
        1 = 1
        and stu.geom is not null
        and sch.schnum = '215'
        

This requests the routed distance for each student attending SchNum 215 (using the WHERE filter). Other information can be retrieved if needed, and other WHERE filters can be applied where necessary. 

This can also be used in an UPDATE if you wanted to assign a distance to an existing column in a table of students. 

### Excluding Values in Routing Calculation

To exclude highways, for example (the types of features are defined in the OSM data), simply add the type to the function when using it: 

    ST_Routed_Distance(geoma, geomb, 'highways')