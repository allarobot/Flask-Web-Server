from flask import Flask,render_template,send_file,send_from_directory
from flask import request
import cv2
from flask import redirect
from flask import jsonify
import json
app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def start():
  return json.dumps({
    'code': 'hello world'
  })
@app.route('/api/image_web', methods=['GET'])
def image():
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
    return send_from_directory('static','image_1.jpg') #send_file('static/image_1.jpg',mimetype='image/jpg')

@app.route('/login',methods=['GET','POST'])
def login():
    '''
    try POST function
    :return:
    '''
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        msg = 'POST:{0}'.format(data)
    else:
        msg = '{GET}'
    return msg
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
