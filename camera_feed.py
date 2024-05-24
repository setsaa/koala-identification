import threading
from queue import Queue

import cv2

from image_processing import Processor

frame_queue = Queue()
results_queue = Queue()
processor = Processor()

tracking_thread = None
tracking_active = False  # Global variable to track the tracking state


def set_tracking(active: bool):
    global tracking_active
    tracking_active = active

    if active and tracking_thread is None:
        start_tracking()
    elif not active and tracking_thread is not None:
        stop_tracking()


def start_tracking():
    print('Starting tracking...')
    global tracking_thread, tracking_active
    if not tracking_active:
        tracking_active = True
        tracking_thread = threading.Thread(target=frame_processor, args=(processor,))
        tracking_thread.start()


def stop_tracking():
    print('Stopping tracking...')
    global tracking_active

    tracking_active = False
    if tracking_thread is not None:
        tracking_thread.join()  # type:ignore # Wait for the thread to finish


def generate_frames(stream_index=2):
    """ Generate frames from the camera feed.

    :param stream_index:
    :return:
    """
    print('Starting video feed...')
    camera = cv2.VideoCapture(stream_index)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            if tracking_active:
                # Add frame to processing queue
                frame_queue.put(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Concatenate frame and yield for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def frame_processor(image_processor: Processor):
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            results = image_processor.process_frame(frame)
            results_queue.put(results)


# Start the frame processing in a separate thread
thread = threading.Thread(target=frame_processor, kwargs={'image_processor': processor}, daemon=True)
thread.start()
