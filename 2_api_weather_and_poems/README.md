# WEATHER HI LO

In the **Weather Hi Lo** game, the player is asked for their OpenWeather API key and to enter a UK town, city or county.

The player is then asked to guess if the next days temperature will be higher or lower for the next four days.

The player scores a point if they guess correctly or if it's the same temperature on both days.

At the end of the game, the total score is displayed. 

If the player scores 4 out of 4, a poem based on the current weather condition is written to a **final_result.txt** file.

If the player scores less than 4, **Better luck next time!** is written to a **final_result.txt** file.

The player is then asked if they would like to play again.


## How to request an OpenWeather API key
1. Sign up via https://home.openweathermap.org/users/sign_up
2. Verify e-mail
3. Once logged in, click on your profile name in the top-right corner and select **My API keys**

## OpenWeather and PoetryDB API usage
This program uses two different parts of OpenWeather:

### Geocoding API
This is required to access the locations latitude and longitude for the **5 day weather forecast** endpoint.

The `country_code` has been set to **UK** for the purposes of the game.

https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_key}

_Further information can be found here_:

https://openweathermap.org/current#name

### 5 day weather forecast
This requires a locations latitude and longitude (from the Geocoding API) to be able to access the 5 day weather forecast.

The forecast is available in 3-hour intervals.

https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}

_Further information can be found here_:
https://openweathermap.org/forecast5
    
### Weather Conditions
Used to identify available weather conditions, which are mapped to possible weather conditions in the PoetryDB API. 
The mappings can be found in the `get_poem_weather_condition` dictionary.

_Further information can be found here_:
https://openweathermap.org/weather-conditions

### PoetryDB API
This API is used to retrieve a poem if the player scores 4 out of 4 guesses correctly.
    
It uses `poem_weather_condition` in the place of `{title_word}`.

https://poetrydb.org/title/{title_word}

_Further information can be found here_:
https://poetrydb.org/index.html


## Python requirements 
For ease of reference, line numbers are listed below for some of the key requirements.\
All other requirements are throughout the program.

- boolean value:  line 245
- string slicing: line 153

## Importing additional modules
The following modules/libraries have been imported and are listed in the `requirements.txt` file:

- **requests** _(allows HTTP requests to interact with APIs)_
- **datetime** _(used for date manipulation)_
- **colorama** _(used to access colours by name)_
- **sys** _(used to exit the program) - Note: This is an in-built python module_

To install them, either click on them in the program file and import package, or in the terminal type i.e:
```
pip3 install requests
``` 
```
pip install requests
```