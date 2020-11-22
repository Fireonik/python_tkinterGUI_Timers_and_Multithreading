class EditingWindow:
    def __init__(self):
        self.__interval = [0]
        self.__signal = ""

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, val):
        self.__interval = val

    @property
    def signal(self):
        return self.__signal

    @signal.setter
    def signal(self, val):
        self.__signal = val


