import time


class MovingAverage:
    """
    Provides a simple moving average of a given size.
    """

    def __init__(self, max_size=10):
        """
        Initializes the moving average.
        :param: max_size: The maximum size of the moving average.
        """
        self.values = []
        self.sum = 0
        self.count = 0
        self.max_size = max_size

    def add(self, value):
        """
        Adds a value to the moving average.
        :param: value: The value to add.
        """
        self.values.append(value)
        self.sum += value
        self.count += 1
        if self.count > self.max_size:
            self.sum -= self.values.pop(0)
            self.count -= 1

    def get_average(self):
        """
        Returns the moving average.
        :return:
        """
        if self.count == 0:
            return 0

        return self.sum / self.count


class Deviation:

    def __init__(self, threshold=30):
        """
        Initializes the deviation instance
        :param threshold: The threshold for deviation on a scale of 0-100.
        """
        self._movingaverage = MovingAverage(max_size=10)
        self._threshold = threshold
        self._last_updated = 0
        self._current_deviation = 0
        self._last_deviation_passed_threshold = False

    def set_current_deviation(self, value):
        """
        Sets the current deviation and updates the last deviation time.
        :param value: The value of the current deviation.
        """
        self._movingaverage.add(value)
        self._current_deviation = value
        self._last_updated = time.time()

    def get_current_deviation(self):
        """
        Returns the current deviation.
        :return: The current deviation.
        """
        return self._current_deviation

    def get_moving_average(self):
        """
        Returns the current deviation moving average.
        :return: The current deviation moving average.
        """
        return self._movingaverage.get_average()

    def get_last_deviation_passed_threshold(self):
        """
        Returns whether the last deviation was above the threshold.
        :return: True if the last deviation was above the threshold, False otherwise.
        """
        return self.has_deviated() and self._last_deviation_passed_threshold

    def get_last_updated(self):
        """
        Returns the time the current deviation was last updated.
        :return: The time the current deviation was last updated.
        """
        return self._last_updated

    def has_deviated(self):
        """
        Returns whether the current deviation is above the threshold.
        :return: True if the current deviation is above the threshold, False otherwise.
        """

        self._last_deviation_passed_threshold = self._current_deviation > self._threshold
        return self._last_deviation_passed_threshold
