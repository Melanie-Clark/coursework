import requests
from datetime import datetime
from colorama import Fore, Back, Style
import sys

# Base URL for accessing openweathermap API endpoints
base_url = "https://api.openweathermap.org/data/2.5/"


# Prints game introduction message
def game_intro():
    # bold, underline, itallic formatting
    intro_message = (f"""\n\033[1m\033[4mGAME INTRO AND RULES\033[0m
The game will use the 5 day weather forecast for a chosen UK location.
Each round, you must guess whether the next days temperature will be higher or lower.
\x1B[3mYou win a point if you guess correctly or if it's the same temperature.\x1B[23m """)

    print(intro_message)
    run()


# Prompts player for their OpenWeather API key
def player_api_key():
    key = input("\nEnter your OpenWeather API key: ")
    return key


# Prompts player to enter a town, city, or county and formats it for URL use
def player_town_city_county():
    uk_town_city_county = input("Enter a UK town, city or county: ")
    return uk_town_city_county.replace(") ", "%20")


# Retrieves today's weather based on location including lat/lon for five-day forecast URL
def get_weather_today(api_key, town_city_county):
    weather_url = f"{base_url}weather?q={town_city_county},uk&appid={api_key}"
    response = requests.get(weather_url)
    status_code = response.status_code
    weather_today = response.json()

    if status_code == 200:
        return weather_today, api_key
    else:
        return weather_url_error_handling(weather_today, status_code, api_key, town_city_county)


# Prints an error message when retrieval fails
def failed_to_retrieve(error_message):
    print(f"{Fore.RED}Failed to retrieve data ({error_message}){Style.RESET_ALL}")


# Prints error message from endpoint if location or API key input error, and displays user input again
def weather_url_error_handling(weather, status_code, api_key, town_city_county):
    error_message = weather['message'].capitalize()

    failed_to_retrieve(error_message)

    if status_code == 401:
        api_key = player_api_key()
    elif status_code == 404:
        town_city_county = player_town_city_county()
    else:
        sys.exit()
    return get_weather_today(api_key, town_city_county)


# Retrieves five-day forecast based on latitude and longitude
def get_five_day_forecast(weather_today, api_key):
    lon = weather_today['coord']['lon']
    lat = weather_today['coord']['lat']

    forecast_url = f"{base_url}forecast?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(forecast_url)
    forecast = response.json()

    if response.status_code != 200:
        error_message = forecast['message'].capitalize()
        failed_to_retrieve(error_message)
        sys.exit()

    return forecast


# Replaces current weather condition with a condition that will be accepted by PoetryDB API
def get_poem_weather_condition(weather_today):
    poem_conditions = {
        "Thunderstorm": "Storm",
        "Drizzle": "Rainy",
        "Rain": "Rainy",
        "Snow": "Snow",
        "Clear": "Sky",
        "Clouds": "Cloud",
        "Atmosphere": "Atmosphere"
    }

    if weather_today['weather'][0]['icon'] == "50d":
        poem_weather_condition = "Atmosphere"
    else:
        weather_condition = weather_today['weather'][0]['main']
        poem_weather_condition = poem_conditions[weather_condition]

    return poem_weather_condition


# Retrieves a poem based on an adapted weather condition which will be accepted by PoetryDB API
def get_poem(poem_weather_condition):
    poem_url = f"https://poetrydb.org/title/{poem_weather_condition}"
    response = requests.get(poem_url)

    if response.status_code == 200:
        return response.json()
    else:
        failed_to_retrieve(response.status_code)


# Returns full poem including title and author
def poem_details(poem_weather_condition):
    poem_structure = get_poem(poem_weather_condition)

    title = poem_structure[0]["title"]
    author = poem_structure[0]["author"]
    lines = poem_structure[0]["lines"]

    poem = "\n".join(line for line in lines)
    complete_poem = f"{title} by {author}\n\n{poem}"

    return complete_poem


# formats weather datetime
def formatted_date_time(forecast, day):
    forecast_str_date_time = forecast['list'][day]['dt_txt']
    forecast_unformatted_date_time = datetime.strptime(forecast_str_date_time, '%Y-%m-%d %H:%M:%S')
    date_time = forecast_unformatted_date_time.strftime('%A %d %b %Y (%H:%M)')

    return date_time


# converts Kelvin to Celsius and casts as integer
def temp_conversion(forecast, day):
    kelvin_to_celsius = 273.15
    temperature = forecast['list'][day]['main']['temp']
    celsius = int(temperature - kelvin_to_celsius)
    return celsius


# Abbreviates location to (3 letters if a single word) or (first letter of each word if multiple words)
def abbreviate_town_city_county(town_city_county_name):
    if " " in town_city_county_name:
        split_town_city_county_name = town_city_county_name.split()
        abbreviated_town_city_county = "".join(word[0] for word in split_town_city_county_name).upper()
    else:
        abbreviated_town_city_county = town_city_county_name[0:3].upper()
        # [:3] will function the same, but [0:3] seems more readable
    return abbreviated_town_city_county


# Retrieves the starting temperature for a chosen location
def starting_message(forecast, date_time, day_index):
    town_city_county_name = forecast['city']['name']
    abbreviated_town_city_county = abbreviate_town_city_county(town_city_county_name)

    message = (f"\nHere's your starting temperature in \033[1m{town_city_county_name} ({abbreviated_town_city_county})\033[0m "
               f"on {date_time}: {Back.LIGHTGREEN_EX}{Fore.BLACK}{temp_conversion(forecast, day_index)}°C{Style.RESET_ALL}\n""")
    print(message)


# Prints higher or lower question and returns players total score
def hi_lo_question(forecast, day_index):
    score = 0

    answer_options = {'H': {'H', 'HIGH', 'HIGHER'}, 'L': {'L', 'LOW', 'LOWER'}}
    valid_responses = answer_options['H'] | answer_options['L']  # | combines both sets (union)

    for _ in range(4):
        temperature = temp_conversion(forecast, day_index)

        day_index += 8

        next_day_temperature = temp_conversion(forecast, day_index)
        date_time = formatted_date_time(forecast, day_index)

        answer = input(
            f"-> Will the temperature on {date_time} be Higher or Lower (H/L) than the previous day?: ").upper()

        while answer not in valid_responses:
            answer = input(f"{Fore.RED}Invalid response: Enter H or L: {Style.RESET_ALL}").upper()

        score = hi_lo_score(answer, answer_options, temperature, next_day_temperature, score)

    return score


# Prints answer and returns score
def hi_lo_score(answer, answer_options, temperature, next_day_temperature, score):
    if ((temperature <= next_day_temperature and answer in answer_options['H']) or
            (temperature >= next_day_temperature and answer in answer_options['L'])):
        correct = f"{Fore.GREEN}Correct!{Style.RESET_ALL}"
        print(correct)
        score += 1
    else:
        incorrect = f"{Fore.RED}Incorrect!{Style.RESET_ALL}"
        print(incorrect)

    next_day_message = f"It will be {next_day_temperature}°C\n"
    print(next_day_message)

    return score


# Writes final result (win or lose) to new file
def write_final_result(result):
    with open('final_result.txt', 'w+') as text_file:
        text_file.write(result)


# Prints if the player has won or lost
def win_lose_message(score, forecast, weather_today):
    players_total_score_message = f"You scored {score} out of 4!"
    print(players_total_score_message)

    location = forecast['city']['name']
    todays_weather = weather_today['weather'][0]['description']

    if score == 4:
        winning_message = (
            f"\nCongratulations...you WON the game! "
            f"\nYour winning poem, \x1B[3minspired by today's weather in {location} ({todays_weather})\x1B[23m,"
            f" is saved to the \033[1m'final_result.txt'\033[0m file")
        print(winning_message)

        poem_weather_condition = get_poem_weather_condition(weather_today)
        result = poem_details(poem_weather_condition)
    else:
        result = f"\nBetter luck next time! 🌧️"
        print(result)
        file_message = f"See the \033[1m'final_result.txt'\033[0m file"
        print(file_message)
    write_final_result(result)


# Asks if player wants to play again, if not the program ends
def play_again():
    play = input("\nDo you want to play again (Y/N)? ").upper()
    while True:
        if play == "Y":
            run()
        elif play == "N":
            sys.exit()
        else:
            play = input("\nInvalid input. Do you want to play again (Y/N)? ").upper()


# Runs the main program
def run():
    day_index = 0

    # Gets user input
    api_key = player_api_key()
    town_city_county = player_town_city_county()

    # Gets weather data
    weather_today, api_key = get_weather_today(api_key, town_city_county)
    forecast = get_five_day_forecast(weather_today, api_key)
    date_time = formatted_date_time(forecast, day_index)

    # Game play
    starting_message(forecast, date_time, day_index)
    score = hi_lo_question(forecast, day_index)
    win_lose_message(score, forecast, weather_today)
    play_again()


# Starts the program with game introduction and rules
game_intro()