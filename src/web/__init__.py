from flask import Flask
from sklearn.feature_extraction.text import TfidfVectorizer

from ..ml.conf import FEATURES_NUMBER
from ..ml.utils import getTextFeats

appInstance = Flask(__name__)

enc_text = TfidfVectorizer(max_features=FEATURES_NUMBER - 2)
getTextFeats(enc=enc_text)

from . import routes  # это срока должна быть внизу во избежание циклических импортирований
