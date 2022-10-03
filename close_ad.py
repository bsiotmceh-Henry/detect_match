from gui import GUI_Handler
from game_controller import Game_Controller
from queue import Queue
from threading import Thread
from time import sleep
from keras.models import load_model
from PIL import Image, ImageOps, ImageGrab
import cv2
import numpy as np

class Application(Thread):
    range_x1:int
    range_y1:int
    range_x2:int
    range_y2:int

    # 對螢幕的尺寸修正
    window_rate_x = 1920 / 1920
    window_rate_y = 1080 / 1080

    def __init__(self, gui_rsp, cont_rsp) -> None:
        Thread.__init__(self)
        self.q_gui_rsp = gui_rsp
        self.q_cont_rsp = cont_rsp

        self.keras_init()

    def keras_init(self):
        # Load the model
        self.model = load_model('x2.h5')
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # 預處理
        self.model.predict(self.data)
            
    def fix_range(self):
        # 原本是用576*1280去做辨識的，所以要依選取範圍調整大小
        size_x = abs(self.range_x1 - self.range_x2)
        size_y = abs(self.range_y1 - self.range_y2)

        # 尺寸修正
        rate_x = size_x / 576
        rate_y = size_y / 1280

        # 尺寸大約60px
        size_list = [
            (60 * rate_x, 60 * rate_y),
            (60 * rate_x, 60 * rate_y),
            (90 * rate_x, 90 * rate_y),
            (60 * rate_x, 60 * rate_y),
            (60 * rate_x, 60 * rate_y),
        ]
        
        # 擷取圖片叉叉的左上位置
        # 使用range1代表以左上為準，使用range2代表以右下為準
        left_position_list = [
            (0 + self.range_x1, 0 + self.range_y1),
            (60 + self.range_x1, 60 + self.range_y1),
            (self.range_x2 - size_list[2][0], 60 + self.range_y1),
            (self.range_x2 - size_list[3][0], 40 + self.range_y1),
            (self.range_x2 - size_list[4][0], 80 + self.range_y1),
        ]

        # 填入辨識範圍清單
        self.position_list = []
        for left in left_position_list:
            # 擷取圖片叉叉的右下位置
            right = (left[0]+size_list[0][0], left[1]+size_list[1][1])
            self.position_list.append([left, right])

    def cross_detect(self):
        # 搜尋所有可能的區域
        result = None
        for p in self.position_list:
            # 擷取區域
            image = ImageGrab.grab(bbox = (p[0][0], p[0][1], p[1][0], p[1][1]))
            # image = self.img.crop((p[0][0], p[0][1], p[1][0], p[1][1]))
            # image.show()

            # resize to 224, 224
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

            # 轉換成np數組
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            self.data[0] = normalized_image_array

            # 進行辨識
            prediction = self.model.predict(self.data)
            # print(prediction)

            x, not_x, skip, background = prediction[0]
            if not_x > 0.8:
                continue
            if x > 0.8:
                result_x = (p[0][0] + p[1][0]) / 2
                result_y = (p[0][1] + p[1][1]) / 2
                result = [result_x, result_y]
                break
            elif skip > 0.8:
                result_x = (p[0][0] + p[1][0]) / 2
                result_y = (p[0][1] + p[1][1]) / 2
                result = [result_x, result_y]
                break
            else:
                continue
        return result

    def run(self):
        while True:
            if not self.q_gui_rsp.empty():
                msg = self.q_gui_rsp.get(True, 0.5)
                self.handle_gui_msg(msg)

            if not self.q_cont_rsp.empty():
                msg = self.q_cont_rsp.get(True, 0.5)
                self.handle_cont_msg(msg)

            sleep(0.1)

    def handle_gui_msg(self, msg):
        global gui, cont
        if msg == 'set_range':
            cont.game_listen()
        
        elif msg == 'cross_detect':
            position = self.cross_detect()
            if position != None:
                cont.mouse_click(position[0] * self.window_rate_x, position[1] * self.window_rate_y)
            gui.cross_detect_finish()

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
                    self.fix_range()
                    gui.set_range_result(self.range_x1, self.range_y1, self.range_x2, self.range_y2)

if __name__ == '__main__':
    q_gui_rsp = Queue()
    q_cont_rsp = Queue()

    app = Application(q_gui_rsp, q_cont_rsp)

    cont = Game_Controller(q_cont_rsp)

    app.start()

    gui = GUI_Handler(q_gui_rsp)
    gui.window.mainloop()