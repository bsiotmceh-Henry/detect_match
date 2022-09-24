from gui import GUI_Handler
from game_controller import Game_Controller
from queue import Queue
from threading import Thread
from time import sleep
from keras.models import load_model
from PIL import Image, ImageOps
import cv2
import numpy as np



class Application(Thread):
    range_x1:int
    range_y1:int
    range_x2:int
    range_y2:int

    def __init__(self, gui_rsp, cont_rsp) -> None:
        Thread.__init__(self)
        self.q_gui_rsp = gui_rsp
        self.q_cont_rsp = cont_rsp

        self.keras_init()

    def keras_init(self):
        # Load the model
        self.model = load_model('x.h5')

        # 576*1280
        self.img = Image.open('../image_ad/1.jpg')

        # 尺寸大約60px
        size_list = [
            60,
            90,
            60,
            60,
        ]
        x_position_list = [
            (60, 60),
            (self.img.width - size_list[1], 60),
            (self.img.width - size_list[2], 40),
            (self.img.width - size_list[3], 80),
        ]
        
        self.position_list = []
        for x in x_position_list:
            y = (x[0]+size_list[0], x[1]+size_list[1])
            self.position_list.append([x, y])

        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    def cross_detect(self):
        # 搜尋所有可能的區域
        for p in self.position_list:
            # 擷取區域
            image = self.img.crop((p[0][0], p[0][1], p[1][0], p[1][1]))

            # resize to 224, 224
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

            # 轉換成np數組
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            self.data[0] = normalized_image_array

            # 進行辨識
            prediction = self.model.predict(self.data)
            print(prediction)

            x, not_x, skip = prediction[0]
            if x > 0.8:
                print("x!")
            elif skip > 0.8:
                print("skip!")

    def run(self):
        while True:
            if not self.q_gui_rsp.empty():
                msg = self.q_gui_rsp.get(True, 0.5)
                self.handle_gui_msg(msg)

            if not self.q_cont_rsp.empty():
                msg = self.q_cont_rsp.get(True, 0.5)
                self.handle_cont_msg(msg)

            sleep(1)

    def handle_gui_msg(self, msg):
        global cont
        if msg == 'set_range':
            cont.game_listen()

    def handle_cont_msg(self, msg):
        global gui, cont
        if type(msg) == list:
            if msg[0] == 'on_click':
                # print(msg)
                if msg[1] == 1:
                    self.range_x1, self.range_y1 = msg[2], msg[3]
                elif msg[1] == 2:
                    self.range_x2, self.range_y2 = msg[2], msg[3]
                    cont.game_listen_stop()
                    gui.set_range_result(self.range_x1, self.range_y1, self.range_x2, self.range_y2)

if __name__ == '__main__':
    gui_rsp = Queue()
    cont_rsp = Queue()

    app = Application(gui_rsp, cont_rsp)

    cont = Game_Controller(cont_rsp)

    app.start()

    gui = GUI_Handler(gui_rsp)
    gui.window.mainloop()