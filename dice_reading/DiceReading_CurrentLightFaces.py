import cv2
import numpy as np
from sklearn import cluster
from picamera2 import Picamera2, Preview
import time
# Sources 
# Site to help access webcam: https://www.opencvhelp.org/tutorials/advanced/how-to-access-webcam/
# Site to help read dice with webcam: https://golsteyn.com/writing/dice

# Parameters
params = cv2.SimpleBlobDetector_Params()

params.filterByInertia
params.minInertiaRatio = 0.6

detector = cv2.SimpleBlobDetector_create(params)

# Function Definitions
def get_blobs(frame):
    frame_blurred = cv2.medianBlur(frame, 7)
    frame_gray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)
    blobs = detector.detect(frame_gray)

    return blobs

def get_dice_from_blobs(blobs):
    # Get centroids of all blobs
    X = []
    for b in blobs:
        pos = b.pt

        if pos != None:
            X.append(pos)

    X = np.asarray(X)

    if len(X) > 0:
        # Important to set min_sample to 0, as a dice may only have one dot
        clustering = cluster.DBSCAN(eps=40, min_samples=1).fit(X)

        # Find the largest label assigned + 1, that's the number of dice found
        num_dice = max(clustering.labels_) + 1

        dice = []

        # Calculate centroid of each dice, the average between all a dice's dots
        for i in range(num_dice):
            X_dice = X[clustering.labels_ == i]

            centroid_dice = np.mean(X_dice, axis=0)

            dice.append([len(X_dice), *centroid_dice])

        return dice

    else:
        return []
    

def overlay_info(frame, dice, blobs):
    # Overlay blobs
    for b in blobs:
        pos = b.pt
        r = b.size / 2

        cv2.circle(frame, (int(pos[0]), int(pos[1])),
                   int(r), (255, 0, 0), 2)

    # Overlay dice number
    for d in dice:
        # Get textsize for text centering
        textsize = cv2.getTextSize(
            str(d[0]), cv2.FONT_HERSHEY_PLAIN, 3, 2)[0]

        cv2.putText(frame, str(d[0]),
                    (int(d[1] - textsize[0] / 2),
                     int(d[2] + textsize[1] / 2)),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

picam2 = Picamera2()
picam2.start()
while(True):
    # Grab the latest image from the video feed
    frame = picam2.capture_array()
    frame = (frame.astype(np.float32)) * 0.75
    frame = frame.astype(np.uint8)
    
    blobs = get_blobs(frame)
    dice = get_dice_from_blobs(blobs)
    out_frame = overlay_info(frame, dice, blobs)

    # Shows frame applet
    cv2.imshow("frame", frame)

    # 
    res = cv2.waitKey(1)

    if dice:        # Breaks the loop when a die is detected. Also works for multiple dice
        time.sleep(0.5)
        num_pips = sum(d[0] for d in dice)
        print(num_pips)
        #break
    # Stop if the user presses "q" - Will need to change exit condition for dice and the game
    if res & 0xFF == ord('q'):
        picam2.close()
        break
# Release the webcam and close the window

cv2.destroyAllWindows()

