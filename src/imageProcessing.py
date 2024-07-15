from torch import cuda
from ultralytics import YOLO

class objectDetection:
    def __init__(self, model, confThresh):
        self.confThresh = confThresh
        self.nmsThreshold = 0.1
        self.model = YOLO(model, task='detect')
        self.classname = self.model.names
        if cuda.is_available():
            # If pytorch is built with GPU backend, it will run on Nvidia GPU
            self.proc = '0'
        else:
            self.proc = 'cpu'      

    def inference(self, frame):
        results = self.model.predict(frame, conf = self.confThresh, iou=self.nmsThreshold, 
                                     device = self.proc, verbose = False)

        classes = [self.classname[int(i)] for i in results[0].boxes.cls]
        scores = results[0].boxes.conf.tolist()
        boxes = [[int(i) for i in j] for j in results[0].boxes.xyxy]
        return classes, scores, boxes
