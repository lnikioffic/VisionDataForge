import numpy as np
import cv2
import aiofiles
import os
from fastapi import UploadFile

from src.videoprocessor.utils.tracker import TrackersClasses, create_Trackers
from src.videoprocessor.schemas import (
    BoundingBoxesObject,
    FrameData,
    MetaDataVideo,
    ROIsObject,
    Frame,
)
from src.videoprocessor.utils.frame_handler import FastSAMModel
from src.videoprocessor.config import UPLOAD_FOLDER, DEFAULT_CHUNK_SIZE
from src.videoprocessor.utils.tools.data_exporter import (
    ExportImage,
    ExportObject,
    get_type,
    AnnotationSave,
)


async def get_fps_hendler(path: str) -> MetaDataVideo:
    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    total_num_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    video.release()
    os.remove(path)
    count = total_num_frames / 30
    return MetaDataVideo(fps=fps, count_frames=int(count))


async def save_video(video: UploadFile):
    # Генерируем уникальное имя файла
    # file_extension = os.path.splitext(video_file.filename)[-1]
    # unique_filename = f'{uuid.uuid4()}{file_extension}'

    file_path = os.path.join(UPLOAD_FOLDER, video.filename)

    async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await video.read(DEFAULT_CHUNK_SIZE):
            await f.write(chunk)

    # Возвращаем путь до сохраненного файла
    return file_path


class VideoHandler:
    def __init__(self, path: str, frame_data: FrameData) -> None:
        self.path: str = path
        self.frame_data: FrameData = frame_data

    async def coordinate_adaptation(self):
        video = cv2.VideoCapture(self.path)
        video.set(cv2.CAP_PROP_POS_FRAMES, self.frame_data.current_frame)

        frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        ratio_width = frame_width / round(self.frame_data.frame_width, 2)
        ratio_height = frame_height / round(self.frame_data.frame_height, 2)
        for bbox_obj in self.frame_data.bboxes_objects:
            bboxes = bbox_obj.bboxes
            for bbox in bboxes:
                bbox[0] = round(bbox[0] * ratio_width)
                bbox[1] = round(bbox[1] * ratio_height)
                bbox[2] = round(bbox[2] * ratio_width)
                bbox[3] = round(bbox[3] * ratio_height)

    def start_processing(self):
        video = cv2.VideoCapture(self.path)
        video.set(cv2.CAP_PROP_POS_FRAMES, self.frame_data.current_frame)
        ret, frame = video.read()
        video.release()
        trackers_classes = create_Trackers(frame, self.frame_data.bboxes_objects)
        frames = self.frame_selection(trackers_classes, self.frame_data.current_frame)

        images = self.frame_processing(frames)

        os.remove(self.path)
        return images
        # return start_annotation(images, self.frame_data.names_class)

    def frame_processing(self, frames: list[Frame]) -> list[ExportImage]:
        fastSAM = FastSAMModel('models/FastSAM-s.pt')

        images = []
        for frame in frames:  # ignore type:  Frame
            fastSAM.set_prompt(frame.frame)
            objects = []
            for cl in frame.names_classes:  # ignore type: ROIsObject
                mask = fastSAM.get_mask_by_box_prompt(cl.ROIs)
                objects.append(ExportObject(mask, cl.name_class))
            images.append(ExportImage(frame.frame, objects))

        return images

    def frame_selection(
        self, trackers_classes: list[TrackersClasses], frame: int = 0
    ) -> list[Frame]:
        video = cv2.VideoCapture(self.path)

        second_frame_view = 0
        number_frame_save = 0
        frames = []
        video.set(cv2.CAP_PROP_POS_FRAMES, frame)
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            list_rois = []
            if second_frame_view == 0:
                for trackers in trackers_classes:
                    bboxes = []
                    for tracker in trackers.trackers:
                        ret, box = tracker.update(frame)
                        bboxes.append(box)
                    rois_object = {'name': trackers.class_name, 'bboxes': bboxes}
                    list_rois.append(rois_object)

            print(1)
            second_frame_view += 1
            second_frame_view &= 2

            if number_frame_save == 0:
                roi = []
                for i in list_rois:
                    roi.append(ROIsObject(name_class=i['name'], ROIs=i['bboxes']))
                frames.append(Frame(frame, roi))
            number_frame_save += 1
            number_frame_save %= 30

        video.release()
        return frames


async def start_annotation(
    images: list[ExportImage], name_classes: dict, type_save: str = 'yolo_dark'
):
    type_save_proces = get_type(images, name_classes, type_save)
    type_save_proces.start_creation()
    archive = type_save_proces.create_archive()
    first_frame, second_frame = type_save_proces.create_preview()
    return archive, first_frame, second_frame


def rectangle(frame, x, y, w, h):
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)


def play_video(
    path: str, trackers_classes: list[TrackersClasses], frame: int = 0
) -> list[Frame]:
    video = cv2.VideoCapture(path)

    second_frame_view = 0
    number_frame_save = 0
    frames = []
    video.set(cv2.CAP_PROP_POS_FRAMES, frame)
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        fr_cop = frame.copy()

        list_rois = []
        if second_frame_view == 0:
            for trackers in trackers_classes:
                bboxes = []
                for tracker in trackers.trackers:
                    ret, box = tracker.update(frame)
                    bboxes.append(box)
                rois_object = {'name': trackers.class_name, 'bboxes': bboxes}
                list_rois.append(rois_object)

                for box in bboxes:
                    (x, y, w, h) = [int(v) for v in box]
                    cv2.rectangle(fr_cop, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(
                        fr_cop,
                        trackers.class_name,
                        (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 255),
                        2,
                    )
            cv2.imshow('test', fr_cop)

        second_frame_view += 1
        second_frame_view &= 2

        if number_frame_save == 0:
            roi = []
            for i in list_rois:
                roi.append(ROIsObject(name_class=i['name'], ROIs=i['bboxes']))
            frames.append(Frame(frame, roi))
        number_frame_save += 1
        number_frame_save %= 30

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
    name_classes = ['Helmet', 'xy']

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

    fastSAM = FastSAMModel('models/FastSAM-s.pt')

    images = []  # type: ignore list[ExportImage]
    for frame in frames:  # ignore type:  Frame
        fastSAM.set_prompt(frame.frame)
        fr_cop = frame.frame.copy()
        objects = []
        for cl in frame.names_classes:  # ignore type: ROIsObject
            mask = fastSAM.get_prompt_box(cl.ROIs)
            objects.append(ExportObject(mask, cl.name_class))
            # a = fastSAM.annotated_frame()
            # cv2.imshow('as', mask)
            # cv2.waitKey(0)
            for box in AnnotationSave.getting_coordinates(mask):
                (x, y, w, h) = [v for v in box]
                cv2.rectangle(fr_cop, (x, y), (x + w, y + h), (0, 0, 255), 3)
                cv2.putText(
                    fr_cop,
                    cl.name_class,
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2,
                )
        cv2.imshow('test', fr_cop)
        images.append(ExportImage(frame.frame, objects))  # type: ignore ExportImage
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
