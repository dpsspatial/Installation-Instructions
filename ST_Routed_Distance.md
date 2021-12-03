##Create Custom Routing Functions using OSRM

The ST_Routed_Distance() and ST_Routed_Line() functions use the OSRM routing server and the Postgresql HTTP Client to return a routed distance and geometry from two input geometries. 

###Set Up OSRM Server

http://project-osrm.org/

We use Docker to run the OSRM server. 

###Install PostgreSQL HTTP Client

Follow the instructions provided by Paul Ramsey posted here: 

https://github.com/pramsey/pgsql-http

Note the creation of the http_get() SQL function, which will be used below. 

###Create ST_Routed_Distance() 

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

###Create ST_Routed_Line() 

    CREATE OR REPLACE FUNCTION public.st_routed_line(g_start geometry, g_finish geometry, exclude_value character varying DEFAULT 'ferry'::character varying)
     RETURNS geometry
     LANGUAGE sql
     COST 10000
    AS $function$
    SELECT ST_GeomFromGeoJSON((http_get(
               'http://px-geo02-p:5000/route/v1/driving/' ||
               ST_X(ST_Transform(g_start, 4326)) || ',' || ST_Y(ST_Transform(g_start, 4326)) ||';' ||
               ST_X(ST_Transform(g_finish, 4326)) || ',' || ST_Y(ST_Transform(g_finish, 4326)) ||
               '?geometries=geojson&overview=full&alternatives=false&steps=false&exclude='|| exclude_value) :: jsonb -> 'routes' -> 0 ->
               'geometry'
            )::text) --::text **Put that between the )) if PG complains about jsonb
    $function$
    ;

###Using Custom Functions


