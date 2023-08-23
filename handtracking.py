import cv2 as cv
import mediapipe as mp

count = 0
draw = True


class CountHands():
    def __init__(self, mode=False, max=2, model_complexity=1, detconf=0.5, trackconf=0.5):
        self.mode = mode
        self.max = max
        self.count = count
        self.detconf = detconf
        self.trackconf = trackconf
        self.mphands = mp.solutions.hands
        self.model_complexity = model_complexity
        self.hands = self.mphands.Hands(self.mode, self.max, self.model_complexity, self.detconf, self.trackconf, )
        self.mpDraw = mp.solutions.drawing_utils

    def handcounter(self, img):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                self.count = +1
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mphands.HAND_CONNECTIONS)
        return count


def main():
    image = cv.imread('twohands.jpg')
    find = CountHands(image)
    print(find.handcounter(image))


if __name__ == '__main__':
    main()
