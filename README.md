## MINTEL - Option 2 - Show weather information by Geolocation

### Setup
To run the application execute the setup.sh file which will build and run the docker instance, then auto run the python application.  

### Runtime 
Once running you will see a "processing please wait..." message.  This means the container is currently collecting a sample of IPs and geolocation data for which weather information is being retrieved (this process can take a minute).

### Output
The IPs are parsed and their city, region and country are recorded.  Data will then be displayed onscreen using panda dataframes to display the current temperature, precipitation probability, wind speed and humidity.  There is a dataset for each with headings.

Below the dataframe output the raw dictionary data is output for use elsewhere.

### Data sources
- The IPs are obtained using calls to wikipedias api.
- Geolocation information is obtained via ipstacks api
- Weather information is gathered using the DarkSky api

### Improvements
The speed of the application could br improved.  A key part of this is the dictionary manipulation at the weather collection phase.  I added some basic output but was hoping to graph the data using matplotlib or ideally export it to a dashboard.

---
During testing both DarkSky and ipstacks proved free is not always enough, the free daily/monthly allowances of which I exhausted during my various tests.  I have subscribed to both at minimal cost to ensure the application continues to work as intended.


 
