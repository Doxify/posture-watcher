import time


class Deviation:
    """
    Handles the deviation from base posture.
    """

    def __init__(self, threshold=30, max_buffer=0):
        """
        Initializes the deviation instance
        :param threshold: The threshold for deviation on a scale of 0-100.
        :param max_buffer: Buffer (in terms of deviations) to allow before a deviation is considered.
        """
        self._threshold = threshold
        self._max_buffer = max_buffer
        self._current_buffer = 0
        self._current_deviation = 0

        self._last_updated = 0
        self._last_deviation_passed_threshold = False

    @property
    def max_buffer(self):
        """
        :return: The max size of the deviation buffer.
        """
        return self._max_buffer

    @property
    def current_buffer(self):
        """
        :return: The current deviation buffer.
        """
        return self._current_buffer

    @property
    def current_deviation(self):
        """
        :return: The current deviation.
        """
        return self._current_deviation

    @property
    def deviation_threshold(self):
        """
        :return: The current deviation threshold.
        """
        return self._threshold

    @property
    def last_updated(self):
        """
        :return: The time the current deviation was last updated.
        """
        return self._last_updated

    @current_deviation.setter
    def current_deviation(self, value):
        """
        :param value: The value of the updated deviation.
        """
        self._current_deviation = value
        self._last_updated = time.time()

    def has_deviated(self):
        """
        Returns whether the current deviation is above the threshold.
        :return: True if the current deviation is above the threshold, False otherwise.
        """
        deviated = self._current_deviation > self._threshold

        # uses buffer to allow for a deviation before it is alerted
        if deviated:
            if self._current_buffer < self._max_buffer:
                self._current_buffer += 1
                return False
            else:
                self._current_buffer = 0
                return True
        else:
            self._current_buffer = 0
            return False
