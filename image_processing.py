"""
Image processing for the application. Handles all ML and processes images from video feed.
"""
import cv2
import numpy as np


class Processor:
    def __init__(self):
        print('Initializing processor...')
        # Load the model
        print('Loading model...')
        self.net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
        self.classes = []
        print('Loading coco')
        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers().flatten()]
        print('Processor initialized!')

    def process_frame(self, frame):
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        # Information to be returned
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        results = []
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                score = confidences[i]
                results.append({'box': [x, y, x + w, y + h], 'label': label, 'confidence': score})
        return results

    def prepare_image(self, frame):
        # Convert frame to RGB and resize
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))  # Resize as per the model's requirement
        frame = np.expand_dims(frame, axis=0)
        frame = frame.astype(np.float32)
        return frame

    def parse_output(self, output):
        # Extract boxes, classes, and scores (implementation depends on the model's specifics)
        boxes = output["detection_boxes"].numpy()
        classes = output["detection_classes"].numpy()
        scores = output["detection_scores"].numpy()

        results = []
        for i in range(len(scores)):
            if scores[i] > 0.5:  # Assuming a threshold of 0.5 for detection confidence
                box = boxes[i]
                class_id = classes[i]
                score = scores[i]
                results.append({'box': box, 'class_id': class_id, 'score': score})

        return results
