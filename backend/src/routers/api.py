import cv2
import time
import json
import asyncio
import concurrent.futures
import onnxruntime as ort
import torch
from deep_sort_realtime.deepsort_tracker import DeepSort

from ..utils import preprocess, postprocess, scale_image, Img2Base64
from ..srcconfig import srcargs


cuda = torch.cuda.is_available()
providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
weights = "./detection/det_model/yolo11n.onnx"

# Start ONNX Runtime session
ort_session = ort.InferenceSession(weights, providers=providers)
model_inputs = ort_session.get_inputs()
input_shape = model_inputs[0].shape

cap = cv2.VideoCapture("./DATA/CarsInHighway_mini.mp4")
origin_width, origin_height = int(cap.get(3)), int(cap.get(4))

scaled_width = 864
scaled_height = int(scaled_width * (origin_height / origin_width))
scaled_shape = (scaled_width, scaled_height)

x_factor = scaled_width / input_shape[2]
y_factor = scaled_height / input_shape[3]
factors = (x_factor, y_factor)


async def stream_video(cap):
    
    # Counters and tracking sets
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    
    tracker = DeepSort(max_age=srcargs.max_age)
    tracks = [] 
    
    start_time = time.time()
    fps = 0
    frame_count = 0
    detection_interval = 1
    
    def run_detection(frame):
        img_data = preprocess(img=frame, input_shape=input_shape)
        output = ort_session.run(None, {model_inputs[0].name: img_data})
        frame, bbs = postprocess(frame, output, factors, 
                                 srcargs.confidence_thres, 
                                 srcargs.iou_thres, 
                                 srcargs.CLASSES, 
                                 srcargs.tracked_class)
        return bbs
    
    # Video capture and setup for output video
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            frame = scale_image(frame, scaled_shape=scaled_shape)
            
            # Get the height and width of the input image
            if frame_count % detection_interval == 0:
                detection_future = executor.submit(run_detection, frame)
                bbs = detection_future.result()
                tracks = tracker.update_tracks(bbs, frame=frame)
            else: 
                continue

            lane1_counter, lane2_counter, lane3_counter = 0, 0, 0
            for track in tracks:
                if not track.is_confirmed():
                    continue
                
                track_id = track.track_id
            
                x1, y1, x2, y2 = map(int, track.to_ltrb())
                center = (int((x1 + x2) / 2), int((y1 + y2) / 2))

                # Zone checking logic
                check_zone = 0
                for lane_id, lane in enumerate([srcargs.lane_1, srcargs.lane_2, srcargs.lane_3], 1):
                    if any(cv2.pointPolygonTest(zone, center, False) >= 0 for zone in lane):
                        check_zone = lane_id
                        break
                if not check_zone:
                    continue
                # Update tracking set based on detected zone
                if check_zone == 1:
                    lane1_counter += 1
                elif check_zone == 2:
                    lane2_counter += 1
                elif check_zone == 3:
                    lane3_counter += 1

                # Draw bounding box and label
                label = f"{srcargs.CLASSES[track.get_det_class()]}-{track_id}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Calculate and display FPS every second
            if frame_count % 10 == 0:  # Update every 10 frames to stabilize FPS display
                end_time = time.time()
                fps = frame_count / (end_time - start_time)
                start_time = end_time  # Reset the timer
                frame_count = 0  # Reset frame count for the next interval

            # Draw lane overlays
            overlay = frame.copy()
            cv2.fillPoly(overlay, srcargs.lane_1, srcargs.color_yellow)
            cv2.fillPoly(overlay, srcargs.lane_2, srcargs.color_red)
            cv2.fillPoly(overlay, srcargs.lane_3, srcargs.color_blue)
            output = cv2.addWeighted(overlay, srcargs.overlays_alpha, frame, 1 - srcargs.overlays_alpha, 0)
            
            # Convert to base64 string
            frame_base64 = Img2Base64(output)
            
            # Prepare lane count data
            lane_counts = {
                "lane1": lane1_counter,
                "lane2": lane2_counter,
                "lane3": lane3_counter
            }

            # Prepare the JSON payload
            data = {
                "frame_base64": frame_base64,
                "fps": fps,
                "lane_counts": lane_counts
            }
            
            data = json.dumps(data)
            
            # Yield the frame in SSE format
            yield f"data: {data}\n\n"
            await asyncio.sleep(0.1)
    finally:
        cap.release()
        executor.shutdown()