import cv2

# Load the image
cap = cv2.VideoCapture("../DATA/CarsInHighway_mini.mp4")
frame = None

# Define the function to capture mouse click events
def get_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button click
        print(f"{x}, {y}")

# Set up the window and bind the function to capture mouse clicks
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", get_coordinates)

h, w = frame.shape[:2]
ratio = h/w

new_w = 864
new_h = int(new_w * ratio)

ratio_update = w / new_w

print(ratio_update)

# Display the image and wait for clicks
while True:
    frame = cv2.resize(frame, (new_w, new_h)) 
    cv2.imshow("Image", frame)
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()