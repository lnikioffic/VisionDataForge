import os
from src.videoprocessor.config import UPLOAD_FOLDER
from src.videoprocessor.utils.video_handler import create_test


if __name__ == '__main__':
    dest = os.path.join(UPLOAD_FOLDER, 'n.mp4')
    print(dest)
    create_test(dest)