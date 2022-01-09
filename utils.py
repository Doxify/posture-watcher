import time


class Utils:
    """
    Generic utility functions.
    """

    @staticmethod
    def calculate_fps(previous_time):
        """
        Calculates the current frames per second given the last time it was calculated.
        :param: previous_time: The last time it was calculated.
        :return: The current frames per second.
        """
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        return int(fps)
