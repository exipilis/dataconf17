import tornado
import os
import json
import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
import tornado.httpserver
from tornado.options import define, options
from featureExtractor import  getFeatureExtractor
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from annoy import AnnoyIndex
import numpy as np
import logging

reload(logging)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def load_img(path,target_size=None):
    from PIL import Image
    res = np.zeros((target_size[1], target_size[0], 3))
    try:
        img = Image.open(path)
        res = img.convert('RGB')
        if target_size:
            res = res.resize((target_size[1], target_size[0]))
    except:
        print('bad image file : '+str(path))
    return res

rootpath = os.path.dirname(os.path.abspath(__file__))

define("port", default=4244, help="run on the given port", type=int)

curPath = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
pathToImages = 'dataset/'

lalafoEncoder = getFeatureExtractor()

Paths = []
with open('dataset.txt', 'r')as inputfile:
    for l in inputfile:
        Paths.append(l.replace('\n',''))

n_trees = 256
vector_size = 2048
idx = AnnoyIndex(vector_size, metric='angular')
#idx.build(n_trees=n_trees)
idx.load('resnet_256.idx')


imgCount = len(Paths)

def findNearest(imgvector, topN):
    searchRes = idx.get_nns_by_vector(imgvector[0], topN, include_distances=True)

    imgPaths = [Paths[searchRes[0][i]] for i in range(0, len(searchRes[0]))]

    res = []
    for i in range(0,topN):
        dist = round(float(searchRes[1][i]), 3)
        url = 'files/' + imgPaths[i]
        res.append({'dist':dist,
                    'url':url})
    return {'nearestProducts': res}


class imageUploadHandler(tornado.web.RequestHandler):

    def post(self):
        file1 = self.request.files['file'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        final_filename = fname+extension

        output_file = open(curPath +"/inputimages/" + final_filename, 'w')
        output_file.write(file1['body'])
        output_file.close()

        imgurl = curPath+"/inputimages/" + final_filename

        img = load_img(imgurl, target_size=(224, 224))
        x = np.array([image.img_to_array(img)])
        x = preprocess_input(x)
        imgVectors = lalafoEncoder.predict(x, batch_size=1)
        print('visual features extracted')
        res = findNearest(imgVectors, 50)
        print('found nearest neibs')
        self.write(json.dumps(res))
        self.finish()

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", imageUploadHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': curPath+'/static/'}),
            (r'/files/(.*)', tornado.web.StaticFileHandler, {'path': pathToImages})
        ]
        tornado.web.Application.__init__(self, handlers)

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
