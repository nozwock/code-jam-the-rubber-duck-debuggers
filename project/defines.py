from importlib import resources

from . import data

EAST_TEXT_DETECTION_MODEL_PATH = resources.files(data) / "frozen_east_text_detection.pb"
assert EAST_TEXT_DETECTION_MODEL_PATH.is_file()
