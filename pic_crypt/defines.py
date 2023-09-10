from importlib import resources

from . import data

_data_files = resources.files(data)
EAST_TEXT_DETECTION_MODEL_PATH = _data_files / "frozen_east_text_detection.pb"
FONT_ANDALEMO_PATH = _data_files / "andalemo.ttf"
