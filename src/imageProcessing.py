import cv2
from torch import cuda
from ultralytics import YOLO


class objectDetection:
    def __init__(self, model, confThresh):
        self.model = model
        self.confThresh = confThresh
        self.nmsThreshold = 0.3

    def load(self):
        self.model = YOLO(self.model, task='detect')
        if cuda.is_available():
            self.proc = '0'
        else:
            self.proc = 'cpu'

    def inference(self, frame):
        results = self.model.predict(frame, conf = self.confThresh, iou=self.nmsThreshold, 
                                     device = self.proc, verbose = False)

        classes = [int(i) for i in results[0].boxes.cls]
        scores = results[0].boxes.conf.tolist()
        boxes = [[int(i) for i in j] for j in results[0].boxes.xyxy]

        return classes, scores, boxes

