## MINTEL - Option 2 - Show weather information by Geolocation

### Setup
To run the application run setup.sh which will build and run the docker instance.  

### Runtime 
Once running you will see a "processing please wait..." message.  This means the container is currently collecting a sample of IPs and collecting geolocation data for which weather information is being retrieved (this process can take up to a minute).

### Output
The IPs are parsed and their city, region and country are recorded.  Data will then be displayed onscreen using panda dataframes to display the current temperature, precipitation probability, wind speed and humidity.

Below the dataframe output the raw dictionary data is output for easy use elsewhere.

### Data sources
- The IPs are obtained using calls to wikipedias api.
- Geolocation information is obtained via ipstacks api
- Weather information is gathered using the DarkSky api

---
During testing both DarkSky and ipstacks proved free is not always enough, the free of which I exhausted during my tests.  I have subscribed to both at minimal cost to ensure the application continues to work as intended.


 