# import pyautogui
from gui import GUI_Handler
from game_controller import Game_Controller
from queue import Queue
from threading import Thread
from time import sleep

class Application(Thread):
    def __init__(self, gui_rsp, cont_rsp) -> None:
        Thread.__init__(self)
        self.gui_rsp = gui_rsp
        self.cont_rsp = cont_rsp

    def run(self):
        while True:
            if not self.gui_rsp.empty():
                msg = self.gui_rsp.get(True, 0.5)
                self.handle_gui_msg(msg)

            if not self.cont_rsp.empty:
                msg = self.cont_rsp.get(True, 0.5)
                self.handle_cont_msg(msg)

            sleep(1)

    def handle_gui_msg(self, msg):
        pass

    def handle_cont_msg(self, msg):
        pass


if __name__ == '__main__':
    gui_rsp = Queue()
    cont_rsp = Queue()

    app = Application(gui_rsp, cont_rsp)

    cont = Game_Controller(cont_rsp)

    app.start()

    gui = GUI_Handler(gui_rsp)
    gui.window.mainloop()
    