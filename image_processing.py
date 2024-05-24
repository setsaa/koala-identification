import cv2
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image


class Processor:
    def __init__(self):
        # Load the TensorFlow ResNet50 model
        self.model = ResNet50(weights='imagenet')
        self.model.trainable = False  # Set the model to inference mode

    def process_frame(self, frame: cv2.typing.MatLike):
        return []
        try:
            # Prepare the frame for the model
            prepared_frame = load_and_prepare_image(frame)

            # Perform inference
            predictions = self.model.predict(prepared_frame)

            # Decode the results into a list of tuples (class, description, probability)
            results = decode_predictions(predictions, top=3)[0]
            return results
        except Exception as e:
            print(f"Error processing frame: {e}")
            return []


def load_and_prepare_image(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array_expanded_dims)
