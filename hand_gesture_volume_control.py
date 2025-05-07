import cv2
import mediapipe as mp
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_ctrl = cast(interface, POINTER(IAudioEndpointVolume))
vol_percentage = 0
vol_bar = 400

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    lm_list = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

    if len(lm_list) >= 21:
        x1, y1 = lm_list[4]
        x2, y2 = lm_list[8]
        x3, y3 = lm_list[20]
        length = math.hypot(x2 - x1, y2 - y1)

        if y3 > lm_list[17][1]:
            volume_ctrl.SetMute(1, None)
            vol_percentage = 0
            vol_bar = 400
        else:
            volume_ctrl.SetMute(0, None)
            vol_scalar = np.interp(length, [20, 200], [0.0, 1.0])
            volume_ctrl.SetMasterVolumeLevelScalar(vol_scalar, None)
            vol_percentage = int(np.interp(length, [20, 200], [0, 100]))
            vol_bar = int(np.interp(length, [20, 200], [200, 50]))

    # Create small transparent-like bar window
    bar_img = np.zeros((250, 150, 3), dtype=np.uint8)
    cv2.rectangle(bar_img, (50, 50), (85, 200), (255, 255, 255), 2)
    cv2.rectangle(bar_img, (50, int(vol_bar)), (85, 200), (0, 255, 0), cv2.FILLED)
    cv2.putText(bar_img, f'{vol_percentage} %', (30, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Volume", bar_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
