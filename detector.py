import cv2
import mediapipe as mp


class PoseLandmarks:
    """
    Indexes for Mediapipe Pose Landmarks
    :reference: https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png
    """
    NOSE = 0
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12


class PoseDetector:
    
    def __init__(self):
        self.results = None
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()

    def find_pose(self, img, draw=True):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # mediapipe requires RGB
        self.results = self.pose.process(img)
        
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

            return img, self.results.pose_landmarks.landmark

        return img, None

