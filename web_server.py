from flask import Flask,render_template, send_file, send_from_directory
from flask import Response, request,redirect,jsonify,url_for
import json,os
from camera import VideoCamera

app = Flask(__name__)

video_camera = None
global_frame = None


def video_stream():
    global video_camera
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame('.jpg')

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


@app.route('/api/v1/part', methods=['GET'])
def start():
  return json.dumps({
    'Status': 'part count service works in internet'
  })


@app.route('/api/v1/part/images', methods=['POST'])
def images():
    n = 666
    if request.method == 'POST' and 'image' in request.files:
        image_file = request.files['image']
        image_path = os.path.join('static', image_file.filename)
        image_path = os.path.abspath(image_path)
        image_file.save(image_path)
    return json.dumps({'Count': '{}'.format(n)})


@app.route('/get_video')
def get_video():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_image')
def get_image():
    return Response(VideoCamera().get_frame('.bmp'),
                    mimetype='image/bmp')


@app.route('/')
def index():
    '''
    image web page with video in it
    :return:
    '''
    return render_template('index.html')


@app.route('/web_video')
def video():
    '''
    image web page with video in it
    :return:
    '''
    return render_template('video.html')

@app.route('/web_image')
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

@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
  return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8094)
