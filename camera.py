import cv2


class VideoCamera(object):
    def __init__(self,id=0,resolution=(640,480)):
        width, height = resolution
        try:
            self.cap = cv2.VideoCapture(id)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
            print(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
              self.cap.get(cv2.CAP_PROP_FPS))
        except:
            print("video camera can not be found!")

    def get_frame(self,format):
        '''

        :param format: '.jpg', '.bmp'
        :return:
        '''
        ret, frame = self.cap.read()

        if ret:
            ret2, image = cv2.imencode(format, frame)

            return image.tobytes()
        else:
            return None

    def __del__(self):
        self.cap.release()
