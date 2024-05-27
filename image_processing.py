"""
Image processing for the application. Handles all ML and processes images from video feed.
"""
import cv2
import torch
from PIL import Image
from torchvision import transforms

WEIGHTS_PATH = 'best.pt'
CFG_PATH = 'pipeline.config'


class Processor:
    def __init__(self):
        print('Initializing processor...')
        try:
            print('Loading model...')
            self.model = torch.hub.load(
                repo_or_dir='ultralytics/yolov5',
                model='custom',
                path='best.pt',
                source='github',
                force_reload=True
            )
            self.transform = transforms.Compose([
                transforms.Resize((256, 256)),
                transforms.ToTensor()
            ])
            self.classes = []
            print('Processor initialized!')
        except Exception as e:
            raise Exception('Error loading the model: ' + str(e))

    def process_frame(self, frame):
        # Convert the frame to PIL Image to apply transforms
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image_tensor = self.transform(pil_image).unsqueeze(0)  # Add batch dimension

        # Perform inference
        with torch.no_grad():
            outputs = self.model(image_tensor)

        # Example of handling outputs - customize this part as necessary
        results = self.parse_model_outputs(outputs, frame.shape[1], frame.shape[0])
        return results

    def parse_model_outputs(self, outputs, width, height):
        """
        Parse the model outputs into a human-readable format.
        This method needs to be implemented according to how your model's output looks like.
        """
        # Assuming 'outputs' are raw detections
        class_ids = []
        confidences = []
        boxes = []

        # This needs the output format of your model, here is a pseudo-implementation
        for output in outputs[0]:
            scores = output['scores']
            bbox = output['bbox']
            class_id = output['class_id']
            confidence = scores.max().item()

            if confidence > 0.5:
                center_x = bbox[0] * width
                center_y = bbox[1] * height
                w = bbox[2] * width
                h = bbox[3] * height
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, int(w), int(h)])
                confidences.append(confidence)
                class_ids.append(class_id)

        # You might use NMS within your model's inference or apply it here manually
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        results = []
        for i in indexes:
            x, y, w, h = boxes[i]
            label = str(class_ids[i])
            score = confidences[i]
            results.append({'box': [x, y, x + w, y + h], 'label': label, 'confidence': score})

        return results
