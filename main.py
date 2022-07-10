import cv2
import time
import sys
import mimetypes
import numpy as np


class Converter:
    CHARACTERS = (" ", ".", "-", "+", "*", "&", "#", "@")
    MIN_ASPECT_CHARS = 50

    def __init__(self, filename) -> None:
        type = self.getMediaType(filename)
        if not type:
            print("Error: Not a valid filetype")
            return

        self.isVid = True if type == "video" else False

        if self.isVid:
            self.file = cv2.VideoCapture(filename)
            self.ms_per_frame = 1 / self.file.get(cv2.CAP_PROP_FPS)
            frame = self.file.read()[1]
        else:
            self.file = cv2.imread(filename)
            frame = self.file

        self.og_h = frame.shape[0]
        self.og_w = frame.shape[1]
        self.aspect = self.MIN_ASPECT_CHARS / min(frame.shape[:2])
        self.h = round(frame.shape[0] * self.aspect)
        self.w = round(frame.shape[1] * self.aspect)
        self.ascii_frame = self.imgToAscii(frame)

        if self.isVid:
            self.ascii_frames = self.asciiVidGenerator()

    def getMediaType(self, filename):
        mimestart = mimetypes.guess_type(filename)[0]
        if mimestart != None:
            type = mimestart.split("/")[0]
            if type in ["video", "image"]:
                return type
        return False

    def getCharacter(self, pixel):
        intensity = pixel / 255
        return self.CHARACTERS[round(intensity * len(self.CHARACTERS)) - 1]

    def imgToAscii(self, img):
        img = cv2.resize(img, (0, 0), fx=self.aspect, fy=self.aspect)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cols = []
        for y in range(self.h):
            row = ""
            for x in range(self.w):
                row += self.getCharacter(img[y, x]) * 2
            cols.append(row)
        return cols

    def asciiVidGenerator(self):
        while self.file.isOpened():
            ret, frame = self.file.read()
            if ret == True:
                yield self.imgToAscii(frame)
            else:
                break

    def displayAscii(self):
        x_increment = round(self.og_w / len(self.ascii_frame[0]))
        y_increment = round(self.og_h / len(self.ascii_frame))
        width = x_increment * len(self.ascii_frame[0])
        height = y_increment * len(self.ascii_frame)

        if self.isVid:
            pass
        else:
            img = np.zeros((height, width, 3), np.uint8)
            for i, row in enumerate(self.ascii_frame):
                y = (i + 1) * y_increment
                for j, char in enumerate(row):
                    x = j * x_increment
                    cv2.putText(
                        img=img,
                        text=char,
                        org=(x, y),
                        fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=0.45,
                        color=(0, 255, 0),
                        thickness=1,
                    )

        cv2.imshow("test", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def displayInTerminal(self):
        if self.isVid:
            gotime = time.time()
            for ascii_frame in self.ascii_frames:
                while True:
                    if time.time() >= gotime:
                        gotime += self.ms_per_frame
                        for row in ascii_frame:
                            print(row)
                        for _ in range(len(ascii_frame)):
                            sys.stdout.write("\x1b[1A")  # cursor up one line
                            sys.stdout.write("\x1b[2K")  # delete the last line
                        break
        else:
            for row in self.ascii_frame:
                print(row)
            input()
            for _ in range(len(self.ascii_frame) + 1):
                sys.stdout.write("\x1b[1A")  # cursor up one line
                sys.stdout.write("\x1b[2K")  # delete the last line


if __name__ == "__main__":
    c = Converter("pic.png")
    c.displayInTerminal()
    c.displayAscii()
