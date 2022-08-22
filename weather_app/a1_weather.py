from tkinter  import *
from tkinter import messagebox
from configparser import ConfigParser
from urllib import request
import json as convert

#Student Name: Varij Rughani
#Student Number: c0804317

url='http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file='config.ini'
config=ConfigParser()
config.read(config_file)
api_key=config['api_key']['key']

def get_weather(city):
    my_result=request.urlopen(url.format(city,api_key))
    if my_result:
        charset=my_result.info().get_content_charset()
        content=my_result.read().decode(charset)
        json = convert.loads(content)
        #Parameter sequence -> (City,Country,temp_celsius,temp_fahrenheit,icon,weather)
        my_city=json['name']
        my_country=json['sys']['country']
        my_temp_kelvin=json['main']['temp']
        my_temp_celsius=my_temp_kelvin-273.15
        my_temp_farhenheit=(my_temp_kelvin-273.15)*9/5+32
        my_icon=json['weather'][0]['icon']
        my_weather=json['weather'][0]['main']
        my_final=(my_city,my_country,my_temp_celsius,my_temp_farhenheit,my_icon,my_weather)
        return my_final

    else:
        return None

def search():
    city=city_text.get()
    weather=get_weather(city)
    if weather:
        location_lbl['text']='{},{}'.format(weather[0],weather[1])
        try:
            image['bitmap']= "http://openweathermap.org/img/wn/{}@2x.png".format(weather[4])
        except:
            print("error loading image")
        temp_lbl['text']='{:.2f}°C , {:.2f}°F'.format(weather[2],weather[3])
        weather_lbl['text']=weather[5]
    else:
        messagebox.showerror('Error !!!!','Cannot find the Expected City{}'.format(city))


app = Tk()
app.title("Weather App")
app.geometry("800x400")

city_text=StringVar()
city_entry=Entry(app,textvariable=city_text)
city_entry.pack()

search_btn=Button(app,text='Search Weather Here',width=16,command=search)
search_btn.pack()

location_lbl=Label(app,text='',font=('bold',22))
location_lbl.pack()

image=Label(app,bitmap='')
image.pack()

temp_lbl=Label(app,text='')
temp_lbl.pack()

weather_lbl=Label(app,text='')
weather_lbl.pack()

counter_lbl = Label(app)
counter_lbl.pack()

counter = 0
def counter_label(label):
    def count():
        global counter
        counter +=1
        label['text'] = counter
        label.after(60000,count)
        if counter>30:
            search()
            label['text'] = 0
            counter = 0
    count()
counter_label(counter_lbl)

app.mainloop()