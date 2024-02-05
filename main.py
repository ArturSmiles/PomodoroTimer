import time
import threading
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import winsound


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
    Path(r"assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class PomodorTimer:

    def __init__(self):
        self.window = Tk()
        self.window.geometry("500x400")
        self.window.title("Pomodoro Timer")
        self.window.tk.call("wm", "iconphoto", self.window._w,
                            PhotoImage(
                                file=relative_to_assets("image_1.png")))
        self.canvas = Canvas(
            self.window,
            bg="#862929",
            height=400,
            width=500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            250.0,
            200.0,
            image=self.image_image_1
        )
        self.canvas.create_rectangle(
            110.0,
            223.0,
            397.0,
            274.0,
            fill="#941B18",
            outline="")

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            activebackground="#D13834",
            command=self.start_timer_thread,
            relief="flat"
        )
        self.button_1.place(
            x=110.0,
            y=288.0,
            width=86.0,
            height=36.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            activebackground="#D13834",
            command=self.stop_clock,
            relief="flat"
        )
        self.button_2.place(
            x=315.0,
            y=288.0,
            width=82.0,
            height=36.0
        )

        self.Short_Break_Text = self.canvas.create_text(
            175.0,
            70.0,
            anchor="nw",
            text="Short Break",
            fill="#D13834",
            font=("Inter", 20),
            state="hidden"
        )
        self.Long_Break_Text = self.canvas.create_text(
            175.0,
            70.0,
            anchor="nw",
            text="Long Break",
            fill="#D13834",
            font=("Inter", 20),
            state="hidden"
        )

        self.work_Text = self.canvas.create_text(
            210.0,
            70.0,
            anchor="nw",
            text="Work",
            fill="#D13834",
            font=("Inter", 20),
            state="hidden"
        )
        self.stop_Text = self.canvas.create_text(
            195.0,
            70.0,
            anchor="nw",
            text="Stopped",
            fill="#D13834",
            font=("Inter", 20),
        )
        self.Timer_Text = self.canvas.create_text(
            200.0,
            225.0,
            anchor="nw",
            text="25:00",
            fill="#D13834",
            font=("Inter", 30)
        )
        self.counter = 0
        self.Counter_Text = self.canvas.create_text(
            240.0,
            335.0,
            anchor="nw",
            text=0,
            fill="#951B18",
            font=("Inter", 30)
        )
        self.stopped = False
        self.timer_id = 0
        self.running = False
        self.full_seconds = 0
        self.stop_clicked = False
        self.window.mainloop()

    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target=self.start_timer)
            t.daemon = True
            t.start()
            self.running = True

    def start_timer(self):
        self.stopped = False
        self.canvas.itemconfigure(self.stop_Text, state="hidden")
        if self.timer_id == 0:
            self.canvas.itemconfigure(self.work_Text, state="normal")
            if not self.stop_clicked:
                self.full_seconds = 60 * 25
            while self.full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(self.full_seconds, 60)
                self.canvas.itemconfigure(
                    self.Timer_Text, text=f"{minutes:02d}:{seconds:02d}")
                self.window.update()
                time.sleep(1)
                self.full_seconds -= 1
            if not self.stopped:
                winsound.Beep(500, 200)
                self.stop_clicked = False
                self.counter += 1
                self.canvas.itemconfigure(
                    self.Counter_Text, text=f"{self.counter}")
                if self.counter % 4 == 0:
                    self.timer_id = 2
                else:
                    self.timer_id = 1
                self.canvas.itemconfigure(self.work_Text, state="hidden")
                self.start_timer()

        elif self.timer_id == 1:
            self.canvas.itemconfigure(self.Short_Break_Text, state="normal")
            if not self.stop_clicked:
                self.full_seconds = 60 * 5
            while self.full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(self.full_seconds, 60)
                self.canvas.itemconfigure(
                    self.Timer_Text, text=f"{minutes:02d}:{seconds:02d}")
                self.window.update()
                time.sleep(1)
                self.full_seconds -= 1
            if not self.stopped:
                winsound.Beep(1000, 200)
                self.stop_clicked = False
                self.timer_id = 0
                self.canvas.itemconfigure(
                    self.Short_Break_Text, state="hidden")
                self.start_timer()

        elif self.timer_id == 2:
            self.canvas.itemconfigure(self.Long_Break_Text, state="normal")
            if not self.stop_clicked:
                self.full_seconds = 60 * 15
            while self.full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(self.full_seconds, 60)
                self.canvas.itemconfigure(
                    self.Timer_Text, text=f"{minutes:02d}:{seconds:02d}")
                self.window.update()
                time.sleep(1)
                self.full_seconds -= 1
            if not self.stopped:
                winsound.Beep(1000, 200)
                self.stop_clicked = False
                self.timer_id = 0
                self.canvas.itemconfigure(
                    self.Long_Break_Text, state="hidden")
                self.start_timer()
        else:
            print("Invalid Timer ID")

    def stop_clock(self):
        self.stopped = True
        self.stop_clicked = True
        self.running = False


PomodorTimer()
