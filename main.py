import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
from gtts import gTTS
from dotenv import load_dotenv
import os


load_dotenv()



TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWM_TOKEN = os.getenv("OWM_TOKEN")


config_dict = get_default_config()
config_dict['language'] = 'en'
owm = OWM(OWM_TOKEN, config_dict)
mgr = owm.weather_manager()

bot = telebot.TeleBot(TELEGRAM_TOKEN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

@bot.message_handler(commands=['start'])
def start(message):
    text = f"<b>Hello, {message.from_user.first_name}!</b>\nEnter the name of the city to get the weather forecast."
    bot.send_message(message.chat.id, text, parse_mode='html')

@bot.message_handler(content_types=['text'])
def send_weather(message):
    try:
        observation = mgr.weather_at_place(message.text)
        w = observation.weather

        status = w.detailed_status
        humidity = w.humidity
        temp = w.temperature('celsius')['temp']
        wind_speed = w.wind()['speed']

        answer = (f"In city {message.text} now {status}\n"
                  f"Temperature: {round(temp)}°C\n"
                  f"humidity: {humidity}%\n"
                  f"Wind speed: {wind_speed} m/s")
        bot.send_message(message.chat.id, answer)

        
        images = {
            'clear sky': 'sun.jpg',
            'overcast clouds': 'clouds.jpg',
            'scattered clouds': 'clouds.jpg',
            'broken clouds': 'clouds.jpg',
            'few clouds': 'clouds.jpg',
            'light rain': 'rain1.png',
            'rain': 'rain1.png',
            'light rain shower': 'rain1.png'
        }

        if status in images:
            image_path = os.path.join(IMAGE_DIR, images[status])
            with open(image_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)

        # Голос
        tts = gTTS(text=answer, lang='en')
        mp3_path = os.path.join(BASE_DIR, "pogoda.mp3")
        tts.save(mp3_path)

        with open(mp3_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

bot.infinity_polling()













