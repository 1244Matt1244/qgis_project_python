The task involves developing a methodology and a Python script to automatically measure three dimensions (length, width, and height) of manually drawn boulders using MBES (Multibeam Echosounder) data. 
The script requires two input data layers: a vector layer in SHP format containing polygons approximating boulder shapes, and a gridded surface of bathymetric average values in GeoTiff format. 
The output should be a vector layer in SHP format with points approximating centroids of the boulder polygons, including attributes like Poly_ID, Target ID, Block, Easting, Northing, Water depth, Length, Width, and Height. 
The results are stored in the same folder as the input vector layer.           
