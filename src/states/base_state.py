class BaseState:
    def __init__(self, game_ctx):
        self.game_ctx = game_ctx

    def enter(self):
        pass  

    def exit(self):
        pass  

    def handle_events(self, event):
        pass

    def update(self, current_time):
        pass

    def render(self):
        pass