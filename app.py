from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
import io
import base64
from PIL import Image
import cv2
import numpy as np
from webcam_detect import sign_detection
import speech_recognition as sr
import numpy as np
from PIL import Image
import string


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app)


    
@socketio.on('image')
def image(data_image):
    
    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    
    #Detection
    frame, letter, prediction_score = sign_detection(frame) 
                                
    
    frame = cv2.putText(frame, 'CV', (480,390), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) , 2, cv2.LINE_AA)
    
     # Encode the frame as base64 string
    retval, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    
    #Dictionary to be emitted
    info = {'frame': jpg_as_text, 'letter' : letter, 'prediction_score' : prediction_score}
    
    # Emit the frame data back to JavaScript client
    socketio.emit('processed_frame', info)
    
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/stv', methods=['POST', 'GET'])
def detect():
    return render_template('index.html')

@app.route('/chatbot')
def chat():
    return render_template('chatbot.html')

@app.route('/voiceover')
def voiceover():
    return render_template('voiceover.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/imggenerator')
def imggenerator():
    return render_template('imggenerator.html')


@app.route('/land', methods=['POST', 'GET'])
def landing():
    return render_template('landing.html')

@app.route('/vts')
def index():
    return render_template('vtsl.html')

@app.route('/process_audio', methods=['GET', 'POST'])
def process_audio():
    print('Request received!')
    r = sr.Recognizer()
    isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
                'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
                'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
                'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
                'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
                 'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
                'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
                'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
                'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
                'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
                'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
                'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
                'where is the bathroom', 'where is the police station', 'you are wrong','address','agra','ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore',
                'bihar','bihar','bridge','cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile','dasara',
                'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello',
                'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango',
                'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
                'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica',
                'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
                'voice', 'wednesday', 'weight','please wait for sometime','what is your mobile number','what are you doing','are you busy']

    arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            audio = r.listen(source)
            try:
                a = r.recognize_google(audio).lower()
                print('You Said:', a)

                for c in string.punctuation:
                    a = a.replace(c, "")

                if a in isl_gif:
                    return jsonify({'type': 'gif', 'value': a})
                else:
                    return jsonify({'type': 'image', 'value': a})
            except:
                pass


if __name__ == '__main__':
    socketio.run(app, port=8080,host='127.0.0.1', debug=True)

