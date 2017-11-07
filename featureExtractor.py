from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input
from keras.models import Model
from keras.layers import Flatten

def getFeatureExtractor():
    base_resnet = ResNet50(include_top=False, weights='imagenet', input_shape=(224, 224, 3), classes=1000)
    flatFeaturesLayer = Flatten()(base_resnet.output)
    model = Model(inputs=base_resnet.input, outputs=flatFeaturesLayer)
    model.compile('sgd', 'mse')
    return model