import cv2
import mediapipe as mp
import time


class HandSensor():
    def __init__(self, mode=False, max=2, model_complexity=1, detconf=0.5, trackconf=0.5):
        self.mode = mode
        self.max = max
        self.detconf = detconf
        self.trackconf = trackconf
        self.mphands = mp.solutions.hands
        self.model_complexity = model_complexity
        self.hands = self.mphands.Hands(self.mode, self.max, self.model_complexity, self.detconf, self.trackconf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mphands.HAND_CONNECTIONS)

    def findPos(self, img, handNo=0, draw=True):
        lmlis = []
        if self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape[0],img.shape[1],img.shape[2]
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlis.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 2, (255, 0, 255), cv2.FILLED)
        return lmlis


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandSensor()
    while True:
        success, img1 = cap.read()
        img = detector.findHands(img1)
        lis = detector.findPos(img1)
        if len(lis) != 0:
            print(lis[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img1, f'{int(fps)}', (5, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("IMAGE", img1)
        if      cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
