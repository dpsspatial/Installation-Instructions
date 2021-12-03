##Create Custom Routing Functions using OSRM

The ST_Routed_Distance() and ST_Routed_Line() functions use the OSRM routing server and the Postgresql HTTP Client to return a routed distance and geometry from two input geometries. 

###Install PostgreSQL HTTP Client

Follow the instructions provided by Paul Ramsey posted here: 

https://github.com/pramsey/pgsql-http

###Create ST_Routed_Distance() Function


