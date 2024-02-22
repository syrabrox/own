import os
import json
import time
from datetime import datetime, timedelta
from tkinter import Tk, messagebox
import threading
import tkinter as tk
from pystray import Icon, MenuItem as item
from PIL import Image
import atexit
import asyncio

name = "Timeouter"
mainStatus = 0 # 0: Main;  1: Testing
script_pfad = os.path.join(os.path.expanduser("~"), "Documents", "Timeouter")
os.makedirs(script_pfad, exist_ok=True)
#script_pfad = os.path.dirname(os.path.abspath(__file__))

def show_toast(message):
    #root = Tk()
    #root.withdraw()
    messagebox.showinfo(name, message)
    #root.after(3000, root.destroy)

    #root.mainloop()

def updateLine(file_path, current_date, status, runtime):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    if lines:
        lines.pop()
    with open(file_path, 'w') as file:
        file.write('\n'.join(lines))
        file.write(f"{current_date},{status},{runtime}\n")
    
def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), int(seconds)

class Config:
    def __init__(self, file_path, file):
        self.file_path = os.path.join(script_pfad, file_path)
        self.file = file
        self.create()

    def create(self):
        if not os.path.exists(self.file_path):
          with open(self.file_path, 'w') as file:
            empty_data = {}
            json.dump(empty_data, file)
          if self.file == "config":
            self.insert("datePath", "date.json")
            self.insert("timeout", 7200)
                
    def insert(self, key, value):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        data[key] = value
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    def get(self, key):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data.get(key, None)

    def update(self, key, new_value):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        if key in data:
            data[key] = new_value
            with open(self.file_path, 'w') as file:
                json.dump(data, file)

    def delete(self, key):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        if key in data:
            del data[key]
            with open(self.file_path, 'w') as file:
                json.dump(data, file)

    def get_all_dates(self):
      with open(self.file_path, 'r') as file:
        data = json.load(file)

      all_dates = {}
      index = 1
      for key, value in data.items():
        if key.startswith("runTime"):
            date_key = key[7:]
            all_dates[index] = date_key
            index += 1
      return all_dates



configPath = 'config.json'
configConfig = Config(configPath, "config")
configConfig.create()

datePath = configConfig.get('datePath')
dateConfig = Config(datePath, "date")
dateConfig.create()
#all_dates_info = dateConfig.get_all_dates()
#print(all_dates_info)

#config.insert('name', 'John Doe')
#print(config.get('timeout'))

#config.update('name', 'Jane Doe')
#print(config.get('name'))

#config.delete('name')
#print(config.get('name'))

# new_time_minutes = add_time(current_time, minutes=30)
# new_time_seconds = add_time(current_time, seconds=5)

def run_thinker(duration, unit):
    print(f"Running thinker for {duration} {unit}") # Minutes Hours
    if unit == "Hours":
        return duration * 60 * 60
    else:
        return duration * 60 

def submit_action():
    global duration, unit, error_label, root
    try:
        durationINT = int(duration.get())
        unitTXT = unit.get()
        if durationINT is None:
            error_label.config(text="Duration can't be Null.")
        else:
            run_thinker(durationINT, unitTXT)
            root.destroy()
    except ValueError:
        error_label.config(text="Duration must be a valid integer.")
    except Exception as e:
        print(e)
        error_label.config(text="Duration can't be Null or a String.")

def configRoot(): 
    global error_label, duration, unit, root
    root = tk.Tk()
    width = 300
    height = 300
    root.title(name)
    root.geometry(f"{width}x{height}+{(root.winfo_screenwidth() - width) // 2}+{(root.winfo_screenheight() - height) // 2}")
    # root.overrideredirect(True)
    root.attributes("-topmost", True)
    
    title = tk.Label(root, text=name, wraplength=200, justify=tk.LEFT, fg="black", font=("Arial", 17, "bold"))
    title.pack(padx=10, pady=10)
    
    label = tk.Label(root, text="Enter Duration:")
    label.pack(pady=10)
    
    duration = tk.Entry(root)
    duration.pack(pady=10)
    duration.focus()  # Set focus on the entry
    
    unit = tk.StringVar(root)
    unit.set("Minutes")
    
    unit_label = tk.Label(root, text="Select Unit:")
    unit_label.pack()
    
    unit_menu = tk.OptionMenu(root, unit, "Minutes", "Hours")
    unit_menu.pack(pady=10)
    
    submit_button = tk.Button(root, text="Submit", command=submit_action)
    submit_button.pack(pady=20)
    
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()
    
    root.mainloop()

# def exit():
#   icon.stop()
# Annahme: show_toast und Icon-Klassen sind definiert

class IconRunner:
    def __init__(self):
        self.icon_thread = None

    def run_icon(self):
        global icon
        image = Image.open("pic.png")
        self.icon = Icon("tray_icon", image, "Timeouter Menu", menu=(
            item('Config Menu', configRoot),
            item('Exit', exit),
        ))
        self.icon.run()

    def start_icon_thread(self):
        self.icon_thread = threading.Thread(target=self.run_icon)
        self.icon_thread.start()

    def stop_icon_thread(self):
        if self.icon_thread and self.icon_thread.is_alive():
            self.icon.stop()
            self.icon_thread.join()

icon_runner = IconRunner()

async def main():
    icon_runner.start_icon_thread()
    print("1")
    await asyncio.sleep(1)
    print("2")
    currentDate = datetime.now().strftime("%d.%m.%Y")
    while 1:
        print(123)
    return 
    
    while dateConfig.get(f'{currentDate}') is None:
        dateConfig.insert(currentDate, currentDate)
        dateConfig.insert(f'status{currentDate}', "False")
        dateConfig.insert(f'runTime{currentDate}', 0)
        await asyncio.sleep(1)
    
    date = dateConfig.get(f'{currentDate}')
    status = dateConfig.get(f'status{currentDate}')
    runTime = dateConfig.get(f'runTime{currentDate}')
    
    if status == "True":
        show_toast(f"Status für {currentDate} ist bereits auf 'true'.")
        print(f"Status für {currentDate} ist bereits auf 'true'.")
        await asyncio.sleep(1)
        os.system("shutdown /s /t 1")
    elif runTime == 0:
        show_toast(f"Runtime: Started")
        print("RunTime: Started")
        dateConfig.update(f'runTime{currentDate}', runTime + 1)
        await asyncio.sleep(1)
    else:
        show_toast(f"Runtime: Updating")
        print("Runtime: Updating")
        newRunTime = int(runTime)
        while newRunTime < configConfig.get('timeout'):
            newRunTime += 1
            print(newRunTime)
            dateConfig.update(f'runTime{currentDate}', newRunTime)
            await asyncio.sleep(1)
        
        dateConfig.update(f'status{currentDate}', "True")
        print("down")

if __name__ == "__main__":
  if mainStatus == 1:
    print("Testing Started")
  else:
    asyncio.run(main())

