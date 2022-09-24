from tkinter import *

class GUI_Handler():

    window = Tk()
    window.title("Hello World!")
    window.minsize(width=500, height=500)
    window.resizable(width=False, height=False)

    def __init__(self, q_gui_rsp):
        self.q_gui_rsp = q_gui_rsp
        self.item_init()

    def item_init(self):
        self.label_range_start = Label(text="range_start:", font=("Arial", 14), padx=5, pady=5)
        self.label_range_start.pack()
        self.context_range_start = Label(text="", font=("Arial", 14), padx=5, pady=5)
        self.context_range_start.pack()
        self.label_range_end = Label(text="range_end:", font=("Arial", 14), padx=5, pady=5)
        self.label_range_end.pack()
        self.context_range_end = Label(text="", font=("Arial", 14), padx=5, pady=5)
        self.context_range_end.pack()

        self.button_set_range = Button(text="set range", font=("Arial", 14, "bold"), padx=5, pady=5, bg="blue", fg="light green", command=self.set_range)
        self.button_set_range.pack()
        self.button_cross_detect = Button(text="cross detect", font=("Arial", 14, "bold"), padx=5, pady=5, bg="blue", fg="light green", command=self.cross_detect)
        self.button_cross_detect.pack()

    def set_range(self):
        self.q_gui_rsp.put("set_range")
        self.button_set_range.config(text="setting")
        pass

    def set_range_result(self, x1, y1, x2, y2):
        self.context_range_start.config(text = str(x1)+","+str(y1))
        self.context_range_end.config(text = str(x2)+","+str(y2))
        self.button_set_range.config(text="set range")

    def cross_detect(self):
        self.q_gui_rsp.put("cross_detect")

    def get_window(self):
        return self.window