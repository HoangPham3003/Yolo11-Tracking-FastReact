import cv2
import base64
import numpy as np


def preprocess(img, input_shape):
    input_width = input_shape[2]
    input_height = input_shape[3]
    
    # Convert the image color space from BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize the image to match the input shape
    img = cv2.resize(img, (input_width, input_height))

    # Normalize the image data by dividing it by 255.0
    image_data = np.array(img) / 255.0

    # Transpose the image to have the channel dimension as the first dimension
    image_data = np.transpose(image_data, (2, 0, 1))  # Channel first

    # Expand the dimensions of the image data to match the expected input shape
    image_data = np.expand_dims(image_data, axis=0).astype(np.float32)

    # Return the preprocessed image data
    return image_data


def postprocess(input_image, output, factors, 
                confidence_thres, iou_thres, CLASSES, tracked_class):
    # Transpose and squeeze the output to match the expected shape
    outputs = np.transpose(np.squeeze(output[0]))

    # Get the number of rows in the outputs array
    rows = outputs.shape[0]

    # Lists to store the bounding boxes, scores, and class IDs of the detections
    boxes = []
    scores = []
    class_ids = []

    # Calculate the scaling factors for the bounding box coordinates
    x_factor, y_factor = factors

    # Iterate over each row in the outputs array
    for i in range(rows):
        # Extract the class scores from the current row
        classes_scores = outputs[i][4:]

        # Find the maximum score among the class scores
        max_score = np.amax(classes_scores)

        # If the maximum score is above the confidence threshold
        if max_score >= confidence_thres:
            # Get the class ID with the highest score
            class_id = np.argmax(classes_scores)
            
            class_name = CLASSES[class_id]
            if class_name != tracked_class:
                continue

            # Extract the bounding box coordinates from the current row
            x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]

            # Calculate the scaled coordinates of the bounding box
            left = int((x - w / 2) * x_factor)
            top = int((y - h / 2) * y_factor)
            width = int(w * x_factor)
            height = int(h * y_factor)

            # Add the class ID, score, and box coordinates to the respective lists
            class_ids.append(class_id)
            scores.append(max_score)
            boxes.append([left, top, width, height])

    # Apply non-maximum suppression to filter out overlapping bounding boxes
    indices = cv2.dnn.NMSBoxes(boxes, scores, confidence_thres, iou_thres)

    # Iterate over the selected indices after non-maximum suppression
    bbs = []
    for i in indices:
        # Get the box, score, and class ID corresponding to the index
        box = boxes[i]
        score = scores[i]
        class_id = class_ids[i]
        bbs.append([box, score, class_id])

    # Return the modified input image
    return input_image, bbs


def scale_image(image, scaled_shape):
    scaled_image = cv2.resize(image, scaled_shape)
    return scaled_image


def Img2Base64(image):
    _, image_arr = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])  # im_arr: image in Numpy one-dim array format.
    image_bytes = image_arr.tobytes()
    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    return image_b64
