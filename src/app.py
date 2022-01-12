import rumps
from posture import PostureWatcher


class Application(rumps.App):

    def __init__(self):
        super().__init__("Posture Watcher", quit_button=None)
        self.pw = PostureWatcher()

    @rumps.clicked("Set base posture")
    def set_base_posture(self, _):
        self.pw.set_base_posture()

    @rumps.clicked("Clear base posture")
    def clear_base_posture(self, _):
        self.pw.base_posture = None

    @rumps.clicked("Quit")
    def quit(self, _):
        self.pw.stop()
        rumps.quit_application()

    @rumps.timer(5)
    def check_posture(self, _):
        self.pw.run()

    @rumps.timer(1)
    def update_title(self, _):
        if not self.pw.base_posture:
            self.title = "⚠️ Please set your base posture."
        else:
            cd = self.pw.deviation.current_deviation
            self.title = "Posture Watcher: "
            if cd < 25:
                self.title += "✅ Great posture!"
            elif cd < 35:
                self.title += f"⚠️ Improve your posture! ({cd}%)"
            else:
                self.title += f"⛔️ Fix your posture! ({cd}%)"


if __name__ == "__main__":
    app = Application()
    app.run()
