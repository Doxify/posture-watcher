import logger
from detector import PoseDetector, PoseLandmarks
from deviation import Deviation
from threading import Thread
from utils import Utils
from logger import Logger
import cv2
import keyboard
import time


class BasePosture:
    """
    Wrapper for Mediapipe Pose Landmarks
    """
    def __init__(self, nose: float, mouth_right: float, mouth_left: float, left_shoulder: float, right_shoulder: float):
        self.nose = nose
        self.mouth_left = mouth_left
        self.mouth_right = mouth_right
        self.left_shoulder = left_shoulder
        self.right_shoulder = right_shoulder


class PostureWatcher:
    """
    PostureWatcher is responsible for monitoring the posture of a user.
    It uses PoseDetector to compare the user's current posture to the base posture.
    """

    def __init__(self,
                 deviation_interval=5,
                 deviation_adjustment=5,
                 deviation_threshold=25,
                 deviation_buffer=3,
                 base_posture=None,
                 debug=True,):
        """
        Initializes the PostureWatcher.
        :param deviation_interval: The interval in seconds between checking for deviation
        :param deviation_adjustment: The amount of deviation to allow before triggering an alert
        :param deviation_threshold: The threshold at which a deviation should trigger an alert
        :param deviation_buffer: The number of consecutive deviations to allow before triggering an alert
        :param base_posture: The base posture to compare to
        :param debug: Whether to print debug messages
        """
        self.detector = PoseDetector()
        self.deviation = Deviation(threshold=deviation_threshold, max_buffer=deviation_buffer)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.last_fps_calc_timestamp = 0
        self.deviation_interval = deviation_interval
        self.deviation_adjustment = deviation_adjustment
        self.base_posture = base_posture
        self.thread = None
        self.debug = debug
        self.logger = Logger('PW')

    def stop(self):
        """
        Stops Posture Watcher and destroys allocated resources.
        """
        self.cap.release()
        cv2.destroyAllWindows()

    def set_base_posture(self):
        _, img = self.cap.read()
        _, lm = self.detector.find_pose(img)
        if lm:
            nose = lm[PoseLandmarks.NOSE]
            mouth_l = lm[9]
            mouth_r = lm[10]
            l_shoulder = lm[11]
            r_shoulder = lm[12]
            self.base_posture = BasePosture(nose, mouth_l, mouth_r, l_shoulder, r_shoulder)

    def _log_deviation(self):
        cd = self.deviation.current_deviation
        cdma = self.deviation.moving_average
        buffer = self.deviation.current_buffer

        logger.clear_console()

        if self.deviation.has_deviated():
            self.logger.notify(f"Detected deviation from base posture by {cd}%", color='red', with_sound=True)
        else:
            self.logger.notify(f"You are doing great! {cd}% (MA: {cdma}%)", color='green')

        if self.debug:
            self.logger.notify(f"Deviation MA: {cdma}%", color='grey')
            self.logger.notify(f"Deviation buffer: {buffer}", color='grey')

    def _get_deviation_from_base_posture(self):
        """
        Calculates the deviation from the base posture as a percentage
        :returns: float from 0-100, 100 being the most deviant from the base posture
        """
        if self.base_posture is None:
            return None

        _, img = self.cap.read()
        _, lm = self.detector.find_pose(img)

        if not lm:  # No pose found
            return 100

        nose = abs(self.base_posture.nose.x - lm[0].x) + abs(self.base_posture.nose.y - lm[0].y) + abs(
            self.base_posture.nose.z - lm[0].z)
        mouth_l = abs(self.base_posture.mouth_left.x - lm[9].x) + abs(self.base_posture.mouth_left.y - lm[9].y) + abs(
            self.base_posture.mouth_left.z - lm[9].z)
        mouth_r = abs(self.base_posture.mouth_right.x - lm[10].x) + abs(self.base_posture.mouth_right.y - lm[10].y) + \
            abs(self.base_posture.mouth_right.z - lm[10].z)
        l_shoulder = abs(self.base_posture.left_shoulder.x - lm[11].x) + abs(self.base_posture.left_shoulder.y - lm[11].y) + \
            abs(self.base_posture.left_shoulder.z - lm[11].z)
        r_shoulder = abs(self.base_posture.right_shoulder.x - lm[12].x) + abs(self.base_posture.right_shoulder.y - lm[12].y) + \
            abs(self.base_posture.right_shoulder.z - lm[12].z)

        deviation = int(
            ((nose + mouth_l + mouth_r + l_shoulder + r_shoulder) / (self.base_posture.nose.x +
             self.base_posture.mouth_left.x + self.base_posture.mouth_right.x + self.base_posture.left_shoulder.x +
             self.base_posture.right_shoulder.x) * 100))

        adjusted_deviation = 100 if deviation >= 100 else deviation - self.deviation_adjustment
        return adjusted_deviation

    def _handle_deviation(self):
        """
        Handles the deviation from the base posture and notifies the user if the deviation is above the threshold.
        """
        if self.deviation.current_deviation is None:
            return

        self._log_deviation()

    # def _listen_for_base_posture(self):
    #     def init():
    #         self.logger.notify("Stand still and press 'SPACE' to set base posture", color='yellow')
    #         while self.base_posture is None:
    #             keyboard.wait('space')
    #             self.set_base_posture()
    #             self.logger.notify("Base posture set, now monitoring for deviation", color='green')
    #     Thread(target=init).start()

    def run(self):
        # self._listen_for_base_posture()
        # while True:
        if not self.base_posture:
            return

        def execute():
            _, img = self.cap.read()
            img, _ = self.detector.find_pose(img)
            # img = cv2.flip(img, 1)
            # img = cv2.resize(img, (600, 400))
            # fps = Utils.calculate_fps(self.last_fps_calc_timestamp)
            # deviation = self.deviation.current_deviation
            # self.last_fps_calc_timestamp = time.time()

            self.deviation.current_deviation = self._get_deviation_from_base_posture()
            self._handle_deviation()

            # cv2.putText(img, f"FPS: {fps}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # cv2.imshow("PostureWatcher", img)
            # cv2.waitKey(1)
        Thread(target=execute).start()
