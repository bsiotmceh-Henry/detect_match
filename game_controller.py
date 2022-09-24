from pynput.mouse import Listener


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


class Game_Controller():

    def __init__(self, q_cont_rsp):
        self.q_cont_rsp = q_cont_rsp

    def game_listen(self):
        self.game_listener = Game_Listener(self.q_cont_rsp)
        self.game_listener.daemon = True
        self.game_listener.name = 'game_listener'
        self.game_listener.start()

    def game_listen_stop(self):
        self.game_listener.stop()
