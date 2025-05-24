import cv2
from cvzone.HandTrackingModule import HandDetector
import time


keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", "⌫"],
    ["SHIFT","Z", "X", "C", "V", "B", "N", "M", "ENTER"],
    [ "SPACE"]
]


shift = False
finalText = ""
last_click_time = 0


cap = cv2.VideoCapture(0)
cap.set(3, 1600)
cap.set(4, 900)
detector = HandDetector(detectionCon=0.8)


class Button:
    def __init__(self, pos, text, size=[110, 80]):
        self.pos = pos
        self.text = text
        self.size = size


def draw_all(img, button_list):
    for button in button_list:
        x, y = button.pos
        w, h = button.size


        if button.text == "SHIFT" and shift:
            color = (0, 200, 200)  
        else:
            color = (180, 0, 180)  

        cv2.rectangle(img, button.pos, (x + w, y + h), color, cv2.FILLED)

        font_scale = 4
        offset_x = 20
        if button.text in ["ENTER", "SHIFT", "SPACE"]:
            font_scale = 3
            offset_x = 10

        cv2.putText(img, button.text, (x + offset_x, y + 55),
                    cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 255, 255), 4)
    return img



button_list = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        width = 110
        if key == "SPACE":
            width = 500
        elif key in ["ENTER", "SHIFT"]:
            width = 160
        button_list.append(Button([120 * j + 40, 100 * i + 40], key, size=[width, 80]))


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
                cv2.putText(img, button.text, (x + 20, y + 55),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l, _, _ = detector.findDistance(index_finger[:2], middle_finger[:2], img)
                current_time = time.time()
                if l < 45 and current_time - last_click_time > 0.4:
                    last_click_time = current_time
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


    cursor_visible = int(time.time() * 2) % 2 == 0
    display_text = finalText + ("|" if cursor_visible else "")


    cv2.rectangle(img, (50, 550), (1550, 720), (175, 0, 175), cv2.FILLED)
    lines = display_text.split("\n")
    y_offset = 600
    for line in lines:
        cv2.putText(img, line, (60, y_offset), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 6)
        y_offset += 60

    cv2.namedWindow("Virtual Keyboard", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Virtual Keyboard", 1600, 900)
    cv2.imshow("Virtual Keyboard", img)

    if cv2.waitKey(1) == ord('q'):
        break
