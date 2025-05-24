import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pyautogui
import time


keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "⌫"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", "ENTER"],
    ["SHIFT", "Z", "X", "C", "V", "B", "N", "M", "SPACE"]
]

shift = False
finalText = ""


cap = cv2.VideoCapture(0)
cap.set(3, 2048) 
cap.set(4, 900)   

detector = HandDetector(detectionCon=0.8)


class Button:
    def __init__(self, pos, text, size=[110, 110]):
        self.pos = pos
        self.text = text
        self.size = size


def draw_all(img, button_list):
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 30, y + 75),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    return img


button_list = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        width = 110
        if key == "SPACE":
            width = 500
        elif key == "ENTER" or key == "SHIFT":
            width = 160
        button_list.append(Button([120 * j + 50, 120 * i + 50], key, size=[width, 110]))


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    img = draw_all(img, button_list)

    if hands:
        lmList = hands[0]["lmList"]
        index_finger = lmList[8]
        middle_finger = lmList[12]

        for button in button_list:
            x, y = button.pos
            w, h = button.size

            if x < index_finger[0] < x + w and y < index_finger[1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 30, y + 75),
                            cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

                l, _, _ = detector.findDistance(index_finger[:2], middle_finger[:2], img)
                if l < 40:
                    if button.text == "⌫":
                        finalText = finalText[:-1]
                    elif button.text == "SPACE":
                        finalText += " "
                    elif button.text == "ENTER":
                        finalText += "\n"
                    elif button.text == "SHIFT":
                        shift = not shift
                    else:
                        char = button.text.upper() if shift else button.text.lower()
                        finalText += char
                        pyautogui.press(char)
                    time.sleep(0.5)  


    cursor_visible = int(time.time() * 2) % 2 == 0
    display_text = finalText + ("|" if cursor_visible else " ")


    cv2.rectangle(img, (50, 600), (1500, 720), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, display_text, (60, 690),
                cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 6)

    cv2.namedWindow("Virtual Keyboard", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Virtual Keyboard", 1600, 900)
    cv2.imshow("Virtual Keyboard", img)

    if cv2.waitKey(1) == ord('q'):
        break
