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
        self.cap.release()

    def get_jpeg(self):
        ret, frame = self.cap.read()
        ret2,jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_bmp(self):
        ret, frame = self.cap.read()
        ret2,bmp = cv2.imencode('.bmp', frame)
        return bmp.tobytes()

@app.route('/api/hello', methods=['GET'])
def start():
  return json.dumps({
    'code': 'hello world'
  })

def gen(camera):
    while True:
        frame = camera.get_jpeg()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/get_video')
def video_stream():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_image')
def image_stream():
    return Response(VideoCamera().get_bmp(),mimetype='image/jpg')

@app.route('/')
def index():
    '''
    image web page with video in it
    :return:
    '''
    return render_template('index.html')


@app.route('/image')
def image():
    '''
    image web page with image in it
    :return:
    '''
    return render_template('image.html')


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
