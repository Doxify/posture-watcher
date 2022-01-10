import cv2
import keyboard
import time

from detector import PoseDetector, PoseLandmarks
from deviation import Deviation
from threading import Thread
from utils import Utils
from logger import Logger


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

    def __init__(self, deviation_interval=5, deviation_adjustment=5, deviation_threshold=30, base_posture=None):
        """
        Initializes the PostureWatcher.
        :param deviation_interval: The interval in seconds between checking for deviation
        :param deviation_adjustment: The amount of deviation to allow before triggering an alert
        :param base_posture: The base posture to compare to
        """
        self.detector = PoseDetector()
        self.deviation = Deviation(threshold=deviation_threshold)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.last_fps_calc_timestamp = 0
        self.deviation_interval = deviation_interval
        self.deviation_adjustment = deviation_adjustment
        self.base_posture = base_posture
        self.thread = None
        self.logger = Logger('PW')
        self._run()

    def stop(self):
        """
        Stops Posture Watcher and destroys allocated resources.
        """
        self.cap.release()
        cv2.destroyAllWindows()

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

        deviation = int(((nose + mouth_l + mouth_r + l_shoulder + r_shoulder) / (self.base_posture.nose.x +
             self.base_posture.mouth_left.x + self.base_posture.mouth_right.x + self.base_posture.left_shoulder.x +
             self.base_posture.right_shoulder.x) * 100))

        adjusted_deviation = deviation - self.deviation_adjustment

        return 100 if adjusted_deviation > 100 else adjusted_deviation

    def _handle_deviation(self):
        """
        Handles the deviation from the base posture and notifies the user if the deviation is above the threshold.
        """
        if self.deviation.get_current_deviation() is None:
            return

        cd = self.deviation.get_current_deviation()
        cdma = self.deviation.get_moving_average()

        if self.deviation.has_deviated():
            self.logger.notify(f"You are deviating from base posture by {cd}% (MA: {cdma}%)",
                               color='red',
                               with_sound=True)
        elif not self.deviation.get_last_deviation_passed_threshold():
            self.logger.notify(f"You are doing great! {cd}% (MA: {cdma}%)", color='green')

    def _set_base_posture(self):
        _, img = self.cap.read()
        _, lm = self.detector.find_pose(img)
        if lm:
            nose = lm[PoseLandmarks.NOSE]
            mouth_l = lm[9]
            mouth_r = lm[10]
            l_shoulder = lm[11]
            r_shoulder = lm[12]
            self.base_posture = BasePosture(nose, mouth_l, mouth_r, l_shoulder, r_shoulder)

    def _listen_for_base_posture(self):
        def init():
            self.logger.notify("Stand still and press 'SPACE' to set base posture", color='yellow')
            while self.base_posture is None:
                keyboard.wait('space')
                self._set_base_posture()
                cv2.destroyAllWindows()
                self.logger.notify("Base posture set, now monitoring for deviation", color='green')
        Thread(target=init).start()

    def _run(self):
        self._listen_for_base_posture()
        while True:
            _, img = self.cap.read()
            img = cv2.flip(img, 1)
            img, _ = self.detector.find_pose(img)
            # img = cv2.resize(img, (600, 400))
            fps = Utils.calculate_fps(self.last_fps_calc_timestamp)
            deviation = self.deviation.get_current_deviation()
            self.last_fps_calc_timestamp = time.time()

            if not self.base_posture:
                cv2.putText(img, "Press 'SPACE' to set base posture.", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 255, 255), 2)
            else:
                cv2.putText(img, f"Deviation: {deviation}%", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # calculate deviation at an interval
            if self.base_posture and time.time() - self.deviation.get_last_updated() > self.deviation_interval:
                deviation = self._get_deviation_from_base_posture()
                self.deviation.set_current_deviation(deviation)
                self._handle_deviation()

            cv2.putText(img, f"FPS: {fps}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("PostureWatcher", img)
            cv2.waitKey(1)
