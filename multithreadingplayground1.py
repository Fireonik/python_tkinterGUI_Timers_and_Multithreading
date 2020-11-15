import threading
import time


class Factory:
    def __init__(self):
        self.__lock = threading.Lock()
        self.__name = "Name"

    def locked_update(self):
        time.sleep(10)
        with self.__lock:
            print(self.__name)

    def work(self):
        workplaces = []
        for i in range(1000):
            t1 = threading.Thread(target=self.locked_update)
            workplaces.append(t1)

        for t in workplaces:
            t.start()


factory1 = Factory()
factory1.work()
