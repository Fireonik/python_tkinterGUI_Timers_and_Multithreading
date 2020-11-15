
import time
storage = []


def start_timer(interval):
    storage.append(interval)


def per_tick_bookkeeping():
    while True:
        time.sleep(1)
        for index, item in enumerate(storage):
            storage[index] -= 1
            if storage[index] == 0:
                print("timer expired!")
                del storage[index]


start_timer(10)

per_tick_bookkeeping()
