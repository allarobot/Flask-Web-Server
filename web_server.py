from flask import Flask,render_template,send_file,send_from_directory
from flask import request,Response
import cv2
from flask import redirect
from flask import jsonify
import json
app = Flask(__name__)
class VideoCamera():
    def __init__(self,device=0):
        self.cap = cv2.VideoCapture(device)

    def __del__(self):
        cv2.release(self.cap)

    def get_frame(self):
        ret, frame = self.cap.read()
        ret2,jpeg = frame.imencode('.jpg', frame)
        return jpeg.tobytes()

@app.route('/api/hello', methods=['GET'])
def start():
  return json.dumps({
    'code': 'hello world'
  })

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_stream')
def video_stream():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    '''
    image web page with image in it
    :return:
    '''
    return render_template('index.html')

@app.route('/api/get_image', methods=['GET'])
def get_image():
    '''
    image file will be downloaded by client
    :return:
    '''
    img = cv2.imread('static/image_1.jpg')
    return send_from_directory('static','image_1.jpg') #
    #return send_file('static/image_1.jpg',mimetype='image/jpg')

@app.route('/api/echo',methods=['GET','POST'])
def login():
    '''
    try POST function
    :return:
    '''
    if request.method == 'POST':
        data = request.form
        print(data)
        msg = 'POST:{0}'.format(data)
    else:
        msg = '{GET}'
    return msg


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
