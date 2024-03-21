#######################################################################################
# FirstName/Surname:
# Student ID:
# Github repository URL: 
#######################################################################################
# Instruction
# Reads README.md in https://github.com/chotipat/NPA2023-Final-Example for more information.
#######################################################################################
 
#######################################################################################
# 1. Import libraries for API requests, JSON formatting, and time.

import json
import requests
import time

#######################################################################################
# 2. Assign the Webex hard-coded access token to the variable accessToken.


accessToken = "Bearer NjNkMzg5ZDctZjAzOS00Y2FhLWJmYTQtOTg2MWY4NjgyNjBhZTUyOTRmYmEtZjcy_P0A1_a61a0b2b-feba-43a3-8a20-e8cc10a43c9a" 

#######################################################################################
# 3. Prepare GetParameters to get the latest message for messages API.

# Defines a variable that will hold the roomId 
roomIdToGetMessages = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vOGQ1NTdlMTAtZGQ3MC0xMWVlLTk2OWQtY2YxOGM1MDlhZjJh" 

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    GetParameters = {
                            "roomId": roomIdToGetMessages,
                            "max": 1
                        }

#######################################################################################
# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get("https://webexapis.com/v1/messages",
                         params = GetParameters, 
                         headers = {"Authorization": accessToken}
                    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception( "Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))
    
    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")
    
    # store the array of messages
    messages = json_data["items"]
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)
    
    # check if the text of the message starts with the magic character "/" and yourname followed by a location name
    # e.g.  "/chotipat San Jose"
    if message.find("/") == 0:
        # extract name of a location (city) where we check for GPS coordinates using the OpenWeather Geocoding API
        # Enter code below to hold city name in location variable.
        # For example location should be "San Jose" if the message is "/chotipat San Jose".
        location = message[message.find(" ")+1:]
        # print("Location: " + location)
    
#######################################################################################     
# 5. Prepare openweather Geocoding APIGetParameters..
        # Openweather Geocoding API GET parameters:
        # - "q" is the the location to lookup
        # - "limit" is always 1
        # - "key" is the openweather API key, https://home.openweathermap.org/api_keys
        openweatherGeoAPIGetParameters = {
            "q": location,
            "limit": 1,
            "appid": "9394df5832daa5f73c96a3a0318d6715",
        }
        # print(openweatherGeoAPIGetParameters)

# 6. Provide the URL to the OpenWeather Geocoding address API.
        # Get location information using the OpenWeather Geocoding API geocode service using the HTTP GET method
        r = requests.get("http://api.openweathermap.org/geo/1.0/direct", 
                             params = openweatherGeoAPIGetParameters
                        )
        # Verify if the returned JSON data from the OpenWeather Geocoding API service are OK
        json_data = r.json()
        # check if the status key in the returned JSON data is "0"
        if not r.status_code == 200:
            raise Exception("Incorrect reply from OpenWeather Geocoding API. Status code: {}".format(r.statuscode))

#######################################################################################
# 7. Provide the OpenWeather Geocoding key values for latitude and longitude.
        # Set the lat and lng key as retuned by the OpenWeather Geocoding API in variables
        locationLat = json_data[0].get("lat") #เป็นการ get ค่าจาก json ที่ได้มาโดยใช้ key ที่เราต้องการ
        locationLng = json_data[0].get("lon") #เป็นการ get ค่าจาก json ที่ได้มาโดยใช้ key ที่เราต้องการ
        # print(locationLat, locationLng)

# 8. Prepare openweatherAPIGetParameters for OpenWeather API, https://openweathermap.org/api; current weather data for one location by geographic coordinates.
        # Use current weather data for one location by geographic coordinates API service in Openweathermap
        openweatherAPIGetParameters = {
                                "lat" : locationLat,
                                "lon" : locationLng,
                                "appid": "9394df5832daa5f73c96a3a0318d6715",
                            }
        # print(openweatherAPIGetParameters)

# 9. Provide the URL to the OpenWeather API; current weather data for one location.
        rw = requests.get("https://api.openweathermap.org/data/2.5/weather", 
                             params = openweatherAPIGetParameters
                        )
        json_data_weather = rw.json()

        if not "weather" in json_data_weather:
            raise Exception("Incorrect reply from openweathermap API. Status code: {}. Text: {}".format(rw.status_code, rw.text))
        # print(json_data_weather)

# 10. Complete the code to get weather description and weather temperature
        weather_desc = json_data_weather["weather"][0]["description"]
        weather_temp = json_data_weather["main"]["temp"] - 273
        # print(weather_desc, weather_temp)

# 11. Complete the code to format the response message.
        # Example responseMessage result: In Austin, Texas (latitude: 30.264979, longitute: -97.746598), the current weather is clear sky and the temperature is 12.61 degree celsius.
        responseMessage = "In {} (latitude: {}, longitute: {}), the current weather is {} and the temperature is {} degree celsius.\n".format(location, locationLat, locationLng, weather_desc, weather_temp)
        print("Sending to Webex Teams: " + responseMessage)

# 12. Complete the code to post the message to the Webex Teams room.         
        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        HTTPHeaders = { 
                             "Authorization": accessToken,
                             "Content-Type": "application/json"
                           }
        # The Webex Teams POST JSON data
        # - "roomId" is is ID of the selected room
        # - "text": is the responseMessage assembled above
        PostData = {
                            "roomId": roomIdToGetMessages,
                            "text": responseMessage
                        }
        # Post the call to the Webex Teams message API.
        r = requests.post( "https://webexapis.com/v1/messages", 
                              data = json.dumps(PostData), 
                              headers = HTTPHeaders
                         )
        if not r.status_code == 200:
            raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))
