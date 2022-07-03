import cv2
import numpy as np
import time

CHARACTERS = (" ", ".", "-", "+", "*", "&", "#", "@")


def getCharacter(pixel):
    intensity = pixel / 255
    return CHARACTERS[round(intensity * len(CHARACTERS)) - 1]


def getVidProps(vid):
    _, frame = vid.read()
    aspect = 50 / min(frame.shape[:2])
    ms_per_frame = 1 / vid.get(cv2.CAP_PROP_FPS)
    return aspect, ms_per_frame


vid = cv2.VideoCapture("vid.mp4")
aspect, ms_per_frame = getVidProps(vid)
gotime = time.time()
while vid.isOpened():
    if time.time() >= gotime:
        gotime += ms_per_frame
        time.sleep(0.01)
        ret, frame = vid.read()
        if ret == True:
            frame = cv2.resize(frame, (0, 0), fx=aspect, fy=aspect)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            h = frame.shape[0]
            w = frame.shape[1]
            cols = []
            for y in range(h):
                row = ""
                for x in range(w):
                    row += getCharacter(frame[y, x]) * 2
                cols.append(row)
            print(np.matrix(cols))
        else:
            break
vid.release()
cv2.destroyAllWindows()
