import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtGui import QIcon,QPalette, QBrush, QImage
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)

        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.setWindowIcon(QIcon("png-transparent-cloud-drawing-cloud-white-cloud-heart.png"))
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(600,300,500,600)
        #________________the line of codes is writen by palette ____________
        image = QImage("background.jpg")

        if image.isNull():
            print("❌ Error: Image could not be loaded. Check the filename or path.")
            return

        scaled_image = image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_image))
        self.setPalette(palette)

        #_____________________________________________________
        vbox=QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setObjectName('emoji_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.setStyleSheet("""
        /* General style settings */
        QPushButton,
        QLabel,
        QLineEdit {
            font-weight: bold;
            font-family: Calibri;
        }

        /* Input field (for city name) */
        QLineEdit {
            font-size: 30px;
            padding: 5px;
            border-radius: 6px;
            background-color: rgba(255, 255, 255, 0.6);
        }
        /* Button style */
        QPushButton {
            font-size: 30px;
            padding: 8px 16px;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.7);
        }

        /* Emoji label (large weather icon) */
        QLabel#emoji_label {
            font-size: 100px;
            margin: 20px 0;
        }
        /* get weather button*/
        QPushButton#get_weather_button:hover {
            background-color: hsl(171, 100%, 50%);;
        }
         /* Other labels */
        QLabel {
            font-size: 40px;
            color: black;
            margin: 30px;
            background: transparent;
        }
              """)
        self.city_input.setPlaceholderText("Bartin")
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api="5290c6a425058fabe57a4c4c899cf247"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data= response.json()
            #print(data)
            if data["cod"]==200:
             self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            if response.status_code==400:
                self.display_error("Bad Request")
            elif response.status_code==401:
                self.display_error("Unauthorized")
            elif response.status_code==403:
                self.display_error("Forbidden")
            elif response.status_code==404:
                self.display_error("Not Found")
            elif response.status_code==429:
                self.display_error("Too Many Requests")
            elif response.status_code==500:
                self.display_error("Internal Server Error")
            elif response.status_code==502:
                self.display_error("Bad Gateway")
            elif response.status_code==503:
                self.display_error("Service Unavailable")
            elif response.status_code==504:
                self.display_error("Gateway Timeout")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error} degree")


    def display_weather(self,data):
        print(data)
        temperature=data["main"]["temp"]
        temperature_c =  temperature - 273.15
        weather_id=data["weather"][0]["id"]
        weather_description=data["weather"][0]["description"]
        self.temperature_label.setText(f"{temperature_c:0f} ")
        self.emoji_label.setText(self.display_emoji(weather_id))
        self.description_label.setText(f"{weather_description}")
    def display_error(self,message):
        self.temperature_label.setText(message)
        self.emoji_label.setText(message)
        self.description_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    @staticmethod
    def display_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""




if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
