from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
   

@app.route('/weather', methods=['POST'])
def weather():
     # Get the text (zip code) entered by the user
    zip_code = request.form.get('text').strip()

    # Your API key from OpenWeatherMap
    api_key = '70e27adc27aa41afa2c25823241704'

    # Make a request to OpenWeatherMap API
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}q={zip_code}&aqi=no'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        # Extract relevant data from the response
        location = data['location']
        current = data['current']
        
        # Weather details
        city_name = location['name']
        region = location['region']
        country = location['country']
        temperature = current['temp_f']  # Temperature in Fahrenheit
        humidity = current['humidity']
        weather_description = current['condition']['text']

        # Return formatted weather info
        weather_info = f"Weather for {city_name}, {region}, {country}:\n" \
                       f"Temperature: {temperature}°F\n" \
                       f"Humidity: {humidity}%\n" \
                       f"Condition: {weather_description.capitalize()}"
        
        return jsonify({
            'response_type': 'in_channel',  # Shows the message to everyone in the channel
            'text': weather_info
        })
    else:
        # Handle API error or invalid zip code
        return jsonify({
            'response_type': 'ephemeral',  # Shows the message only to the user who invoked the command
            'text': f"Could not retrieve weather data for ZIP code {zip_code}. Please check the zip code and try again."
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)