import cv2
import time
import sys
import mimetypes


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
            frame = self.file.read()[1]
        else:
            self.file = cv2.imread(filename)
            frame = self.file

        self.aspect = self.MIN_ASPECT_CHARS / min(frame.shape[:2])
        self.h = round(frame.shape[0] * self.aspect)
        self.w = round(frame.shape[1] * self.aspect)

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

    def saveFile(self):
        # TODO save text to img and videos
        pass

    def displayInTerminal(self):
        if self.isVid:
            ms_per_frame = 1 / self.file.get(cv2.CAP_PROP_FPS)
            ascii_frames = self.asciiVidGenerator()
            gotime = time.time()
            for frame in ascii_frames:
                while True:
                    if time.time() >= gotime:
                        gotime += ms_per_frame
                        for row in frame:
                            print(row)
                        for _ in range(len(frame)):
                            sys.stdout.write("\x1b[1A")  # cursor up one line
                            sys.stdout.write("\x1b[2K")  # delete the last line
                        break
        else:
            frame = self.imgToAscii(self.file)
            for row in frame:
                print(row)
            input()
            for _ in range(len(frame) + 1):
                sys.stdout.write("\x1b[1A")  # cursor up one line
                sys.stdout.write("\x1b[2K")  # delete the last line


if __name__ == "__main__":
    c = Converter("vid.mp4")
    c.displayInTerminal()
