# import sys
# import os
# sys.path.insert(1, os.path.join(sys.path[0], '..'))


import numpy as np
import cv2
import aiofiles
import os
from fastapi import UploadFile
from .tracker import TrackersClasses, create_Trackers
from ..schemas import BoundingBoxesObject, FrameData
from .farme_handler import NewFastSAMModel
from videoprocessor.config import UPLOAD_FOLDER, DEFAULT_CHUNK_SIZE


async def get_fps_hendler(path: str, video: UploadFile):
    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    os.remove(path)
    return fps


async def save_video(video: UploadFile):
    # Генерируем уникальное имя файла
    # file_extension = os.path.splitext(video_file.filename)[-1]
    # unique_filename = f"{uuid.uuid4()}{file_extension}"

    # Создаем путь до директории для сохранения файла
    file_path = os.path.join(UPLOAD_FOLDER, video.filename)

    # Сохраняем файл в директорию
    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await video.read(DEFAULT_CHUNK_SIZE):
            await f.write(chunk)

    # Возвращаем путь до сохраненного файла
    return file_path


async def coordinate_adaptation(path: str, frame_data: FrameData):
    video = cv2.VideoCapture(path)
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_data.current_frame)


    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    ratio_width = frame_width / round(frame_data.frame_width, 2)
    ratio_height = frame_height / round(frame_data.frame_height, 2)
    for bbox_obj in frame_data.bboxes_objects:
        bboxes = bbox_obj.bboxes
        for bbox in bboxes:
            bbox[0] = round(bbox[0] * ratio_height)
            bbox[1] = round(bbox[1] * ratio_width)
            bbox[2] = round(bbox[2] * ratio_height)
            bbox[3] = round(bbox[3] * ratio_width)    


async def start_processing(path: str, frame_data: FrameData):
    video = cv2.VideoCapture(path)
    ret, frame = video.read()
    trackers_classes = create_Trackers(frame, frame_data.bboxes_objects)
    video.release()
    frames = play_video(path, trackers_classes, frame_data.current_frame)

    fastSAM = NewFastSAMModel('models/FastSAM-s.pt')

    for frame in frames:
        fastSAM.set_prompt(frame.frame)
        fr_cop = frame.frame.copy()
        for cl in frame.names_classes:
            cl.set_new_ROI(fastSAM)
            for box in cl.ROIs:
                (x, y, w, h) = [v for v in box[0]]
                cv2.rectangle(fr_cop, (x, y), (x + w, y + h), (0, 0, 255), 3)
                cv2.putText(fr_cop, cl.name, (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.imshow("test", fr_cop)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    print(len(frames))


class ROIsObject:
    def __init__(self, ROIs: list[list[int]], name: str):
        self.name = name
        self.ROIs = ROIs

    def set_new_ROI(self, sam):
        self.ROIs[:] = [sam.get_prompt_box(box) for box in self.ROIs]


class Frame:
    def __init__(self, frame: np.array, names_classes: list[ROIsObject]):
        self.frame = frame
        self.names_classes = names_classes


def rectangle(frame, x, y, w, h):
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)


def play_video(path: str, trackers_classes: list[TrackersClasses], frame: int = 0) -> list[Frame]:
    video = cv2.VideoCapture(path)

    l = 0
    k = 0
    frames = []
    video.set(cv2.CAP_PROP_POS_FRAMES, frame)
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        fr_cop = frame.copy()
        dl = []
        if l == 0:
            for trackers in trackers_classes:
                bboxes = []
                for tracker in trackers.trackers:
                    ret, box = tracker.update(frame)
                    bboxes.append(box)
                d = {'name': trackers.class_name, 'bboxes': bboxes}
                dl.append(d)
                for box in bboxes:
                    (x, y, w, h) = [int(v) for v in box]
                    cv2.rectangle(fr_cop, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(fr_cop, trackers.class_name, (x, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
            cv2.imshow("test", fr_cop)
        l += 1
        l &= 2
        if k == 0:
            roi = []
            for i in dl:
                roi.append(ROIsObject(name=i['name'], ROIs=i['bboxes']))
            frames.append(Frame(frame, roi))
        k += 1
        k %= 30
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    video.release()
    return frames


def create_test(path):
    video = cv2.VideoCapture(path)
    ret, frame = video.read()
    frame_cop = frame.copy()
    video.release()
    name_classes = ['Каска', 'sd']

    data = []
    for name in name_classes:
        bboxes = []
        for _ in range(1):
            bbox = cv2.selectROI(frame_cop)
            rectangle(frame_cop, bbox[0], bbox[1], bbox[2], bbox[3])
            bboxes.append(bbox)
        data.append(BoundingBoxesObject(name_class=name, bboxes=bboxes))
    cv2.destroyAllWindows()
    trackers_classes = create_Trackers(frame, data)
    frames = play_video(path, trackers_classes)

    fastSAM = NewFastSAMModel('models/FastSAM-s.pt')
    # # name_dir = os.path.splitext(path)
    # # os.mkdir(name_dir[0])
    # # path_im = name_dir[0]
    # for frame in frames:
    #     fastSAM.set_prompt(frame.farme)
    #     fr_cop = frame.farme.copy()
    #     for cl in frame.names_classes:
    #         cl.set_new_ROI(fastSAM)
    #         for box in cl.ROIs:
    #             (x, y, w, h) = [v for v in box[0]]
    #             cv2.rectangle(fr_cop, (x, y), (x + w, y + h), (0, 0, 255), 3)
    #             cv2.putText(fr_cop, cl.name, (x, y), 
    #                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
    #     cv2.imshow("test", fr_cop)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    # cv2.destroyAllWindows()
    # print(len(frames))


if __name__ == '__main__':
    path = 'VisionDataForge/data/video/n.mp4'
    video = cv2.VideoCapture(path)
    ret, frame = video.read()
    frame_cop = frame.copy()
    video.release()
    name_classes = ['Каска', 'sd']

    data = []
    for name in name_classes:
        bboxes = []
        for _ in range(1):
            bbox = cv2.selectROI(frame_cop)
            rectangle(frame_cop, bbox[0], bbox[1], bbox[2], bbox[3])
            bboxes.append(bbox)
        data.append(BoundingBoxesObject(name_class=name, bboxes=bboxes))
    cv2.destroyAllWindows()
    trackers_classes = create_Trackers(frame, data)
    frames = play_video(path, trackers_classes)


    # fastSAM = NewFastSAMModel('models/FastSAM-s.pt')
    # name_dir = os.path.splitext(path)
    # os.mkdir(name_dir[0])
    # path_im = name_dir[0]
    # for frame in frames:
    #     fastSAM.set_prompt(frame.farme)
    #     fr_cop = frame.farme.copy()
    #     for cl in frame.names_classes:
    #         cl.set_new_ROI(fastSAM)
    #         for box in cl.ROIs:
    #             (x, y, w, h) = [v for v in box[0]]
    #             cv2.rectangle(fr_cop, (x, y), (x + w, y + h), (0, 0, 255), 3)
    #             cv2.putText(fr_cop, cl.name, (x, y), 
    #                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
    #     cv2.imshow("test", fr_cop)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    # cv2.destroyAllWindows()
    # print(len(frames))