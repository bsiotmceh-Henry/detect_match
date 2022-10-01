from tkinter import *

class GUI_Handler():

    window = Tk()
    window.title("Close AD")
    window.minsize(width=500, height=500)
    window.resizable(width=False, height=False)

    def __init__(self, q_gui_rsp):
        self.q_gui_rsp = q_gui_rsp
        self.item_init()

    def item_init(self):
        self.label_range_start = Label(text="range start:", font=("Arial", 14), padx=5, pady=5)
        self.label_range_start.pack()
        self.context_range_start = Label(text="", font=("Arial", 14), padx=5, pady=5)
        self.context_range_start.pack()
        self.label_range_end = Label(text="range end:", font=("Arial", 14), padx=5, pady=5)
        self.label_range_end.pack()
        self.context_range_end = Label(text="", font=("Arial", 14), padx=5, pady=5)
        self.context_range_end.pack()
        self.label_detect_result = Label(text="detect result:", font=("Arial", 14), padx=5, pady=5)
        self.label_detect_result.pack()
        self.context_detect_result = Label(text="", font=("Arial", 14), padx=5, pady=5)
        self.context_detect_result.pack()

        self.button_set_range = Button(text="set range", font=("Arial", 14, "bold"), padx=5, pady=5, bg="blue", fg="light green", command=self.set_range)
        self.button_set_range.pack()
        self.button_cross_detect = Button(text="cross detect", font=("Arial", 14, "bold"), padx=5, pady=5, bg="blue", fg="light green", command=self.cross_detect)
        self.button_cross_detect.pack()

    def set_range(self):
        self.q_gui_rsp.put("set_range")
        self.button_set_range.config(text="setting")
        self.button_set_range['state'] = 'disable'
        pass

    def set_range_result(self, x1, y1, x2, y2):
        self.context_range_start.config(text = str(x1)+","+str(y1))
        self.context_range_end.config(text = str(x2)+","+str(y2))
        self.button_set_range.config(text="set range")
        self.button_set_range['state'] = 'normal'

    def cross_detect(self):
        self.q_gui_rsp.put("cross_detect")
        self.button_cross_detect['text'] = 'detecting'
        self.button_cross_detect['state'] = 'disable'

    def cross_detect_finish(self):
        self.button_cross_detect['text'] = 'cross_detect'
        self.button_cross_detect['state'] = 'normal'

    def get_window(self):
        return self.window