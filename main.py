import cv2
import numpy as np
import time


class Converter:
    CHARACTERS = (" ", " ", ".", "-", "+", "*", "&", "#", "@")
    MIN_ASPECT_CHARS = 50

    def __init__(self, filename) -> None:
        self.vid = cv2.VideoCapture(filename)
        frame = self.vid.read()[1]
        self.aspect = self.MIN_ASPECT_CHARS / min(frame.shape[:2])
        self.ms_per_frame = 1 / self.vid.get(cv2.CAP_PROP_FPS)

    def getCharacter(self, pixel):
        intensity = pixel / 255
        return self.CHARACTERS[round(intensity * len(self.CHARACTERS)) - 1]

    def convertToTerminal(self):
        gotime = time.time()
        while self.vid.isOpened():
            if time.time() >= gotime:
                gotime += self.ms_per_frame
                ret, frame = self.vid.read()
                if ret == True:
                    frame = cv2.resize(frame, (0, 0), fx=self.aspect, fy=self.aspect)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    h = frame.shape[0]
                    w = frame.shape[1]
                    cols = []
                    for y in range(h):
                        row = ""
                        for x in range(w):
                            row += self.getCharacter(frame[y, x]) * 2
                        cols.append(row)
                    print(np.matrix(cols))
                else:
                    break
        self.vid.release()


c = Converter("vid.mp4")
c.convertToTerminal()
