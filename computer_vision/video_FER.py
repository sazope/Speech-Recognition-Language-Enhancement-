from flask import Flask, render_template, request  # import Flask and other necessary modules
import cv2  # import OpenCV module for video capture
import time  # import time module for time calculations
import collections  # import collections module for counting emotions
from deepface import DeepFace  # import DeepFace module for emotion detection

app = Flask(__name__)  # create Flask application instance

@app.route('/')  # set up route for the main page
def index():
    return render_template('index.html')  # render HTML template for the main page

@app.route('/start_detection', methods=['POST'])  # set up route for emotion detection
def start_detection():
    global emotion_list, cap  # use global variables for the emotion list and video capture object
    cap = cv2.VideoCapture(0)  # create a video capture object with the default camera
    capture_duration = 10  # set the duration for capturing video frames
    start_time = int(time.time())  # get the start time for capturing video frames
    emotion_list = []  # initialize the emotion list
    while int(time.time()) - start_time < capture_duration:  # loop until the capture duration is over
        try:
            ret, frame = cap.read()  # read a frame from the video capture object
            if not ret:
                raise Exception("Error reading frame")  # raise an exception if there's an error reading the frame
        except Exception as e:
            print("Error reading frame:", e)  # print an error message if there's an exception
            time.sleep(0.1)  # wait for 0.1 seconds and continue to the next iteration of the loop
            continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert the frame from BGR to RGB color format
        try:
            emotions = DeepFace.analyze(rgb_frame, actions=['emotion'])  # analyze the emotions in the frame using the DeepFace module
        except Exception as e:
            print("Error analyzing frame:", e)  # print an error message if there's an exception
            time.sleep(0.1)  # wait for 0.1 seconds and continue to the next iteration of the loop
            continue
        dominant_emotion = emotions[0]['dominant_emotion']  # get the dominant emotion from the analysis results
        emotion_list.append(dominant_emotion)  # add the dominant emotion to the emotion list
        cv2.imshow('frame', frame)  # show the current frame in a window named 'frame'
        cv2.waitKey(1)  # wait for 1 millisecond for a key press
        time.sleep(0.1)  # wait for 0.1 seconds before processing the next frame
    cap.release()  # release the video capture object
    cv2.destroyAllWindows()  # destroy all windows

    # count the frequency of each emotion in the emotion list
    if emotion_list:
        counter = collections.Counter(emotion_list)
        dominant_emotion = counter.most_common(1)[0][0]  # get the most frequent emotion in the emotion list
        return dominant_emotion  # return the most frequent emotion
    else:
        return "No emotions detected in the video"  # if no emotions were detected, return a message

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
# This releases the video capture device used in the emotion detection process
global cap
cap.release()
# This closes all open windows used for displaying the captured video frames
cv2.destroyAllWindows()
# This returns a message indicating that the emotion detection process has been stopped
return "Emotion detection stopped"

This checks if the script is being run as the main program
if name == 'main':
# This sets the port number to be used for the Flask app, either using the value of the PORT environment variable or the default value of 5000
port = int(os.environ.get('PORT', 5000))
# This starts the Flask app and listens for incoming requests on the specified host and port, with debugging enabled
app.run(debug=True, host='0.0.0.0', port=port)