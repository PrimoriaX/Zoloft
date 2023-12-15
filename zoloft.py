import os, sys
import win32api, win32con
import pyautogui
import cv2
import math
import mss
import numpy as np
import time
import torch
import win32api
import contextlib
import threading

#Settings
CameraSize = 256
ShowCamera = True
ModelConfidence = 0.40
X_SPEED = 2
Y_SPEED = 2
AIM_KEY = 0x02

class Zoloft:
    def __init__(self):
        print("\nLoading Model...")
        self.monitor_size = pyautogui.size()
        self.camera_size = CameraSize
        self.capture = mss.mss()
        
        if torch.cuda.is_available():
            with open(os.devnull, 'w') as devnull:
                with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                    self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.onnx', force_reload=False)
                    self.model.half()
                    self.model.conf = ModelConfidence
                    self.model.iou = 0.50
        else:
            print("Cuda is not available, exiting...")
            time.sleep(5)
            exit()
        
    def move_crosshair(self, x, y):
        CenterDifX = x - (self.monitor_size.width // 2)
        CenterDifY = y - (self.monitor_size.height // 2)
        MouseMovementX = round(CenterDifX * X_SPEED)
        MouseMovementY = round(CenterDifY * Y_SPEED)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, MouseMovementX, MouseMovementY)

    def analyze_frame(self, captured_frame, capture_area):
        detections = self.model(captured_frame, size=self.camera_size)
        optimal_target = None
        min_distance_to_crosshair = None

        for *bounding_box, confidence, _ in detections.xyxy[0]:
            top_left, bottom_right = [int(coord.item()) for coord in bounding_box[:2]], [int(coord.item()) for coord in bounding_box[2:]]
            target_height = bottom_right[1] - top_left[1]
            head_position = (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2 - target_height / 2.7))
            distance = math.dist(head_position, (self.camera_size / 2, self.camera_size / 2))

            if min_distance_to_crosshair is None or distance <= min_distance_to_crosshair:
                min_distance_to_crosshair = distance
                optimal_target = {"top_left": top_left, "bottom_right": bottom_right, "head_position": head_position, "confidence": confidence}

            self.display_detection(captured_frame, top_left, bottom_right, confidence)

        if optimal_target and win32api.GetAsyncKeyState(AIM_KEY) < 0:
            absolute_head = (optimal_target["head_position"][0] + capture_area['left'], optimal_target["head_position"][1] + capture_area['top'])
            threading.Thread(target=lambda: self.move_crosshair(*absolute_head)).start()

        return captured_frame

    def display_detection(self, frame, top_left, bottom_right, confidence):
        confidence_percentage = (confidence.item() if isinstance(confidence, torch.Tensor) else confidence) * 100
        confidence_text = f"{int(confidence_percentage)}%"
        cv2.rectangle(frame, top_left, bottom_right, (255, 100, 100), 2)
        cv2.putText(frame, confidence_text, top_left, cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 100, 100), 2)

    def start(self):
        print("Model loaded successfully.")
        center_x, center_y = self.monitor_size.width // 2, self.monitor_size.height // 2
        capture_area = {'left': int(center_x - self.camera_size // 2),
                        'top': int(center_y - self.camera_size // 2),
                        'width': self.camera_size,
                        'height': self.camera_size}

        while True:
            frame_start_time = time.perf_counter()
            current_frame = np.array(self.capture.grab(capture_area))
            current_frame = self.analyze_frame(current_frame, capture_area)
            
            if ShowCamera:
                fps_display = f"FPS: {int(1 / (time.perf_counter() - frame_start_time))}"
                cv2.putText(current_frame, fps_display, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 2)
                cv2.imshow("Camera", current_frame)

                if cv2.waitKey(1) & 0xFF == ord('0'):
                    break
