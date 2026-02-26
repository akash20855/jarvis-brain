import time
from datetime import timedelta

def update_time():
    now = time.localtime()
    hours, minutes, seconds = map(lambda x: str(x).zfill(2) if x < 10 else str(x), now)
    clock_label.config(text=f"{hours}:{minutes}:{seconds}")

def main():
    window = tkinter.Tk()
    window.title("Digital Clock")
    clock_label = tkinter.Label(window, font=("Arial", 24), bg="white")
    clock_label.pack(padx=10, pady=10)

    # Update the time every second
    update_time()
    window.after(1000, update_time)

    # Main loop to keep the window open
    window.mainloop()

if __name__ == "__main__":
    main()