import tkinter as tk  
from datetime import datetime  
import pandas as pd  
import os  
  
class TimerApp:  
    def __init__(self, root):  
        self.root = root  
        self.start_time = None  
        self.timer_running = False  
        self.csv_file = 'timer_data.csv'#title and path for the CSV file  
  
        self.timer_label = tk.Label(root, text="00:00:00", font=('Helvetica', 20))  
        self.timer_label.pack()  
  
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)  
        self.start_button.pack()  
  
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer, state='disabled')  
        self.stop_button.pack()  
  
    def start_timer(self):  
        self.start_time = datetime.now()  
        self.timer_running = True  
        self.start_button['state'] = 'disabled'  
        self.stop_button['state'] = 'normal'  
        self.update_timer()  
  
    def stop_timer(self):  
        self.timer_running = False  
        self.start_button['state'] = 'normal'  
        self.stop_button['state'] = 'disabled'  
        self.save_time()  
  
    def update_timer(self):  
        if self.timer_running:  
            elapsed_time = datetime.now() - self.start_time  
            minutes, seconds = divmod(elapsed_time.total_seconds(), 60)  
            h_seconds = elapsed_time.microseconds // 10000  
            self.timer_label['text'] = "{:02}:{:02}:{:02}".format(int(minutes), int(seconds), h_seconds)  
            self.root.after(10, self.update_timer)  # Updating every 10 ms to get hundredths of seconds  

    def save_time(self):  
        elapsed_time = datetime.now() - self.start_time  
        minutes, seconds = divmod(elapsed_time.total_seconds(), 60)  
        h_seconds = elapsed_time.microseconds // 10000  
        data = {  
            'ID': [self.get_next_id()],  
            'Date': [datetime.now().strftime('%Y-%m-%d')],  
            'Time': [datetime.now().strftime('%H:%M:%S')],  
            'ElapsedTime': ["{:02}:{:02}:{:02}".format(int(minutes), int(seconds), h_seconds)]   
        }  
  
        df = pd.DataFrame(data)  
  
        if not os.path.isfile(self.csv_file):  
            df.to_csv(self.csv_file, index=False)  
        else:  
            df.to_csv(self.csv_file, mode='a', header=False, index=False)
  
    def get_next_id(self):  
        if os.path.isfile(self.csv_file):  
            df = pd.read_csv(self.csv_file)  
            return df['ID'].max() + 1  
        else:  
            return 1  
  
root = tk.Tk()
root.geometry("300x110")#resizing the GUI window
root.title("Elevator Waiting Timer")#title of the GUI window  
app = TimerApp(root)  
root.mainloop()  