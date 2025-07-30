import random
import pygame
import time
class Timer:
    def rand_timer(self):
        while True:
            r = random.random()
            time.sleep(1)
            if r < 0.017:
                print ("stop")
                break
            else :
                print ("continue")


if __name__ == "__main__":
    timer= Timer()
    timer.rand_timer()