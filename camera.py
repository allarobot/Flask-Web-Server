import cv2

class VideoCamera(object):
    def __init__(self,id=0):
        self.cap = cv2.VideoCapture(id)

    def get_frame(self,format):
        '''

        :param format: '.jpg', '.bmp'
        :return:
        '''
        ret,frame = self.cap.read()

        if ret:
            ret2,image = cv2.imencode(format,frame)

            return image.tobytes()
        else:
            return None

    def __del__(self):
        self.cap.release()
