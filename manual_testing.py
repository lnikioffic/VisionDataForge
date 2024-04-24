import os
from src.videoprocessor.config import UPLOAD_FOLDER_TESTING
from src.videoprocessor.utils.video_handler import create_test


if __name__ == '__main__':
    dest = os.path.join(UPLOAD_FOLDER_TESTING, 'n.mp4')
    create_test(dest)