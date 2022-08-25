import cv2
from cvzone.PoseModule import PoseDetector
import pyglet.media
import os
import requests

#cap = cv2.VideoCapture('http://192.168.31.211') # esp32cam
cap = cv2.VideoCapture(0) #webcam

if not cap.isOpened():
    print("Camera can't open!!!")
    exit()

detector = PoseDetector()
sound = pyglet.media.load("alarm.wav", streaming=False)
people = False
img_count, breakcount = 0, 0

path = '/Users/animeshkumarnayak/PycharmProjects/smartcctv-main/img/' #Replace your path directory
url   = 'https://api.telegram.org/bot'
token = "5359624864:AAEvkmg7JPaeQYTUDG3kpIx8u50D3vyOkw4" #Replace Your Token Bot
chat_id = "1171288906" #Replace Your Chat ID
caption = "People Detected!!!"

while True:
    success, img = cap.read()
    img = detector.findPose(img, draw=False)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)

    img_name = f'image_{img_count}.png'

    if bboxInfo:
        cv2.rectangle(img, (120, 20), (470, 80), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "PEOPLE DETECTED!!!", (130, 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        breakcount += 1


        if breakcount >= 30:
            if people == False:
                img_count += 1
                sound.play()
                cv2.imwrite(os.path.join(path, img_name), img)
                files = {'photo': open(path + img_name, 'rb')}
                print("files:",files)
                resp = requests.post(url + token + '/sendPhoto?chat_id=' + chat_id + '&caption=' + caption + '', files=files)
                print(f'Response Code: {resp.status_code}')
                people = not people
    else:
        breakcount = 0
        if people:
            people = not people

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()

