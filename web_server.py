from flask import Flask,render_template, send_file, send_from_directory
from flask import Response, request,redirect,jsonify,url_for
#form flask_uploads import UploadSet, IMAGES, configure
import cv2,os
import json

app = Flask(__name__)

class VideoCamera():
    '''
    access camera image or video
    '''
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

@app.route('/api/v1/part', methods=['GET'])
def start():
  return json.dumps({
    'status': 'part count service works in internet'
  })

@app.route('/api/v1/part/images', methods=['POST'])
def images():
    n = 666
    if request.method == 'POST' and 'image' in request.files:
        image_file = request.files['image']
        image_path = os.path.join('static', image_file.filename)
        image_path = os.path.abspath(image_path)
        image_file.save(image_path)
    return json.dumps({
    'Count': '{}'.format(n) })

def gen(camera):
    while True:
        frame = camera.get_jpeg()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/get_video')
def video_stream():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_image')
def image_stream():
    return Response(VideoCamera().get_bmp(), mimetype='image/bmp')

@app.route('/')
def index():
    '''
    image web page with video in it
    :return:
    '''
    return render_template('index.html')

@app.route('/video')
def video():
    '''
    image web page with video in it
    :return:
    '''
    return render_template('video.html')

@app.route('/image')
def image():
    '''
    image web page with image in it
    :return:
    '''
    return render_template('image.html')


@app.route('/api/upload/image',methods=['GET','POST'])
def upload():
    '''
    upload image and show it
    :return:
    '''
    if request.method == 'POST' and 'image' in request.files:
        image_file = request.files['image']
        image_path = os.path.join('static',image_file.filename)
        image_path = os.path.abspath(image_path)
        image_file.save(image_path)
        print('POST: /api/upload/image --> {}'.format(image_path))
        image_url = url_for('static',filename=image_file.filename)
        return render_template('show.html',image=image_url)
    else:
        return render_template('upload.html')


@app.route('/api/echo/<file>',methods=['GET','POST'])
def echo(file):
    '''
    echo cmd to client
    :return:
    '''
    msg =''
    if request.method == 'POST':

        msg = 'POST:/api/echo/{}'.format(file)
    else:
        msg = 'GET:/api/echo/{}'.format(file)
    print(msg)
    return msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8094)
