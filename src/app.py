import rumps
from posture import PostureWatcher
# rumps.debug_mode(True)  # turn on command line logging information for development - default is off


class Application(rumps.App):

    def __init__(self):
        super().__init__("Posture Watcher", quit_button=None)
        self.pw = PostureWatcher()

    @rumps.clicked("Set Base Posture")
    def set_base_posture(self, _):
        self.pw.set_base_posture()

    @rumps.timer(5)
    def check_posture(self, _):
        self.pw.run()

    @rumps.timer(1)
    def update_title(self, _):
        if not self.pw.base_posture:
            self.title = "Please set your base posture to continue!"
        else:
            cd = self.pw.deviation.current_deviation
            self.title = "Posture Watcher: "
            if cd < 25:
                self.title += "✅ Great posture!"
            elif cd < 35:
                self.title += f"⚠️ Improve your posture! ({cd}%)"
            else:
                self.title += f"⛔️ Fix your posture! ({cd}%)"

    @rumps.clicked("Quit")
    def quit(self, _):
        self.pw.stop()
        rumps.quit_application()


if __name__ == "__main__":
    app = Application()
    app.run()
