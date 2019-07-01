import requests
import cv2

def post_file(url):
    files ={'file':open('report.xls','rb')}
    files ={'file':('report.csv','some data to send\nanother row to send\n')}
    r = requests.post(url,files=files)
    return r.text


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
    import matplotlib.pyplot as plt
    url ='http://192.168.1.11/api/hello'
    print(get_result(url))

    url = 'http://192.168.1.11/api/get_image'
    image = get_result_raw(url)
    plt.figure()
    plt.imshow(image)

    url = 'http://192.168.1.11/login'
    out = post_data(url)
    print(out)

