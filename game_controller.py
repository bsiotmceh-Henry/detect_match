from pynput.mouse import Listener, Controller, Button
from time import sleep

# mouse = Listener()
# mouse.press(Button.left)

class Game_Listener(Listener):
    def __init__(self, q_cont_rsp):
        Listener.__init__(self, on_click=self.on_click)
        self.q_cont_rsp = q_cont_rsp
        self.time = 0
        # self.listen_click = False

    def on_click(self, x, y, button, pressed):
        # print(x, y, button, button.name, pressed)
        if button.name == 'left' and pressed == False:
            self.time += 1
            self.q_cont_rsp.put(['on_click', self.time, x, y])

class Mouse_Controller(Controller):
    def __init__(self) -> None:
        Controller().__init__()


class Game_Controller():

    def __init__(self, q_cont_rsp):
        self.q_cont_rsp = q_cont_rsp
        self.mouse = Mouse_Controller()

    def game_listen(self):
        self.game_listener = Game_Listener(self.q_cont_rsp)
        self.game_listener.daemon = True
        self.game_listener.name = 'game_listener'
        self.game_listener.start()

    def game_listen_stop(self):
        self.game_listener.stop()

    def mouse_click(self, x, y):
        self.mouse.position = (x, y)
        sleep(0.1)
        self.mouse.click(Button.left, 1)
        print(self.mouse.position)
        
if __name__ == '__main__':
    g = Game_Controller(None)
    
    g.mouse_click(1920, 1080)