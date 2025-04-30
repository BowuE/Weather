import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import customtkinter as ctk
import requests
import os
from tkvideo import tkvideo

API_KEY = '6a62cbd8b6fd43188180367db9ac8d95'

video_label = None
player = None
current_video = None

# GUI
root = ctk.CTk()
root.title("Weather")
root.geometry("1060x600")
root.update()
window_width = root.winfo_width()
window_height = root.winfo_height()
root.resizable(False, False)
root.configure(fg_color="#ecf0f1")

def stop_current_video():
    global player, video_label
    if player:
        try:
            player._running = False
        except Exception as e:
            print("Ошибка при остановке видео:", e)
        player = None
    if video_label:
        try:
            video_label.destroy()
        except:
            pass
        video_label = None

def play_video(video_path):
    global video_label, player, current_video
    if current_video == video_path:
        return
    stop_current_video()
    video_label = Label(root)
    video_label.place(x=0, y=0, width=window_width, height=window_height)
    player = tkvideo(video_path, video_label, loop=1, size=(window_width, window_height))
    current_video = video_path
    player.play()

    for widget in root.winfo_children():
        if widget != video_label and not isinstance(widget, tk.Canvas):
            widget.lift()

def get_weather():
    city = city_entry.get()
    if not city:
        city_label.configure(text="No city name", text_color="orange")
        clear_labels()
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            raise Exception("City not found")

        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        main = data['weather'][0]['main'].lower()

        city_label.configure(text=city.upper(), text_color="black")
        temp_label.configure(text=f"{temp:.1f}°C")
        desc_label.configure(text=desc.capitalize())
        humidity_label.configure(text=f"Humidity: {humidity}%")

        # Иконка
        icon_path = f"icons/{main}.png"
        if not os.path.exists(icon_path):
            icon_path = "icons/default.png"
        icon_image = Image.open(icon_path).resize((50, 50))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.configure(image=icon_photo)
        icon_label.image = icon_photo

        # Видео
        video_path = f"videos/{main}.mp4"
        if not os.path.exists(video_path):
            video_path = "videos/default.mp4"
        play_video(video_path)

    except Exception as e:
        print("Ошибка:", e)
        city_label.configure(text="No city found", text_color="red")
        clear_labels()

def clear_labels():
    temp_label.configure(text="")
    desc_label.configure(text="")
    humidity_label.configure(text="")
    icon_label.configure(image="")
    icon_label.image = None

def on_closing():
    stop_current_video()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# ----------- Виджеты -----------

city_label = ctk.CTkLabel(root, text="City", font=("Arial", 34, "bold"), text_color="black")
city_label.pack(pady=50)

city_entry = ctk.CTkEntry(root, width=200)
city_entry.pack(pady=10)

city_search_btn = ctk.CTkButton(root, text="Find city", command=get_weather)
city_search_btn.pack(pady=5)

temp_label = ctk.CTkLabel(root, text="", font=("Arial", 40, "bold"), text_color="black")
temp_label.pack(pady=15)

desc_label = ctk.CTkLabel(root, text="", font=("Arial", 18), text_color="black")
desc_label.pack(pady=10)

icon_label = ctk.CTkLabel(root, text="")
icon_label.pack(pady=5)

humidity_label = ctk.CTkLabel(root, text="", font=("Arial", 16), text_color="black")
humidity_label.pack(pady=10)

# ----------- Запуск -----------

play_video("videos/default.mp4")
root.mainloop()
