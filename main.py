import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pyautogui

keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "⌫"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", "ENTER"],
    ["SHIFT", "Z", "X", "C", "V", "B", "N", "M", "SPACE"]
]

shift=False

cap = cv2.VideoCapture(0)
cap.set(3, 1280) 
cap.set(4, 720)  

detector = HandDetector(detectionCon=0.8)
finalText = ""

def draw_all(img, button_list):
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 30, y + 75),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    return img

class Button:
    def __init__(self, pos, text, size=[110, 110]):
        self.pos = pos
        self.text = text
        self.size = size

button_list = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        button_list.append(Button([120 * j + 50, 120 * i + 50], key))  

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
                    elif button.text=="SPACE":
                        finalText.text+=" "
                    elif button.text == "ENTER":
                        finalText.text == "\n"
                    elif button.text == "SHIFT":
                        shift=not shift
                    else:
                        char =button.text.upper() if shift  else button.text.lower()
                        finalText += char
                    pyautogui.press(button.text.lower()) if len(button.text) == 1 else None
                    cv2.waitKey(300)

    cv2.rectangle(img, (50, 450), (1200, 550), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 520),
                cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 6)

    cv2.namedWindow("Virtual Keyboard", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Virtual Keyboard", 1280, 720)
    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) == ord('q'):
        break
