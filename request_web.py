import requests
import cv2
import os

def post_file(url):
    files ={'file':open('report.xls','rb')}
    files ={'file':('report.csv','some data to send\nanother row to send\n')}
    r = requests.post(url,files=files)
    files.clear()
    return r.text

def post_image(url,img_path):
    filename,extensionname = os.path.splitext(img_path)
    print(filename,extensionname[1:])
    img_post_descriptor ={'image':(img_path,open(img_path,'rb'),'image/jpeg')}
    res = requests.post(url,files=img_post_descriptor)
    img_post_descriptor.clear()
    return (res.text)

def post_data(url):
    data={'key1':'value1','key2':'value2'}
    r = requests.post(url,data=data)
    return r.text


def get_result(url):
    r = requests.get(url)
    return r.text

def get_result_raw(url):
    r = requests.get(url)
    return r

if __name__ == '__main__':

    ##hello
    url ='http://192.168.1.10/api/hello'
    print(get_result(url))

    ##POST image to web server
    url = 'http://192.168.1.10/api/upload/image'
    image_path = b'C:\Users\Administrator\Downloads\post_it.jpg'
    #data = open(image_path,'rb').read()
    res = post_image(url,image_path)
    print(res)




