import cv2
import uuid
import shutil
from pathlib import Path

from src.videoprocessor.utils.tools.contour_detector import threshold, get_filtered_bboxes_xywh
from src.videoprocessor.config import BASE_FOLDER_DATA


class ExportObject():
    def __init__(self, mask, name_class) -> None:
        self.mask = mask
        self.name_class = name_class
        self.coordinates = []


class ExportImage():
    def __init__(self, image, objects: list[ExportObject]) -> None:
        self.image = image
        self.objects = objects


class YoloCreateFolder():
    def __init__(self, images: list[ExportImage], names_class: list[str]) -> None:
        self.images = images
        self.names_class = {}
        for i, name in enumerate(names_class):
            self.names_class[name] = i
        folder_name = ''.join(names_class)[:10] if len(''.join(names_class)) > 15 else ''.join(names_class)
        folder_name = f'{folder_name}-{uuid.uuid1()}'
        p = Path(BASE_FOLDER_DATA / folder_name)
        p.mkdir()
        self.path_folder = BASE_FOLDER_DATA / folder_name
        self.images_folder = self.path_folder / 'images'
        p = Path(self.images_folder)
        p.mkdir()
        self.lables_folder = self.path_folder / 'lables'
        p = Path(self.lables_folder)
        p.mkdir()


    def start_creation(self):
        path_image = self.images_folder / 'image_filename'
        path_txt = self.lables_folder / 'image_filename'
        for i, image in enumerate(self.images):
            cv2.imwrite(f'{path_image}{i+1}.jpg', image.image)
            YoloSaveDark.txt_frame_save(image, f'{path_txt}{i+1}', self.names_class)
        YoloSaveDark.txt_class_save(self.path_folder / 'classes', self.names_class)
        
    
    def create_preview(self):
        if len(self.images) == 0:
            return

        if len(self.images) > 3:
            image = self.images[3]
        else:
            image = self.images[1]
        
        uu = uuid.uuid4()
        first_frame = BASE_FOLDER_DATA / f'first-{uu}.jpg'
        second_frame = BASE_FOLDER_DATA / f'second-{uu}.jpg'
        cv2.imwrite(first_frame, image.image)
        for ob in image.objects: # type: ignore ExportObject
            bboxes = YoloSaveDark.getting_coordinates(ob.mask)
            for box in bboxes:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(image.image, (x, y), (x + w, y + h), (0, 0, 255), 3)
                cv2.putText(image.image, ob.name_class, (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        cv2.imwrite(second_frame, image.image)
        return first_frame, second_frame


    def create_archive(self):       
        # Укажите путь к папке, которую нужно архивировать

        # Укажите путь и имя архива

        # Создайте архив
        shutil.make_archive(self.path_folder, 'zip', self.path_folder)
        return f'{self.path_folder}.zip'


class YoloSaveDark():
    @classmethod
    def getting_coordinates(cls, image_mask):
        thresh_stags = threshold(image_mask, thresh=110, mode='direct')
        bboxes = get_filtered_bboxes_xywh(thresh_stags, min_area_ratio=0.001)
        return bboxes


    @classmethod
    def txt_class_save(cls, path: str, names_class: dict):
        with open(f'{path}.txt', 'w') as file:
            for key, value in names_class.items():
                name_class_str = [f'{value} {key} \n']

                file.writelines(name_class_str)
                

    @classmethod
    def txt_frame_save(cls, image: ExportImage, path: str, names_class: dict):

        img_height = image.image.shape[0]
        img_width = image.image.shape[1]
        with open(f'{path}.txt', 'w') as file:
            for class_box in image.objects: # type: ignore ExportObject
                class_box.coordinates = YoloSaveDark.getting_coordinates(class_box.mask)
                for box in class_box.coordinates:
                    x, y = box[0], box[1]
                    w, h = box[2], box[3]

                    x_center = x + int(w/2)
                    y_center = y + int(h/2)

                    norm_xc = x_center / img_width
                    norm_yc = y_center / img_height
                    norm_width = w / img_width
                    norm_height = h / img_height

                    yolo_annotation = [f'{names_class[class_box.name_class]} {norm_xc} {norm_yc} {norm_width} {norm_height} \n']
                    
                    file.writelines(yolo_annotation)


def save_annotations(img, boxes, path):
    img_height = img.shape[0]
    img_width = img.shape[1]
    with open(f'{path}.txt', 'w') as f:
        for box in boxes:
            if len(box) > 0:
                x, y = box[0], box[1]
                w, h = box[2], box[3]

                x_center = x + int(w/2)
                y_center = y + int(h/2)

                norm_xc = x_center / img_width
                norm_yc = y_center / img_height
                norm_width = w / img_width
                norm_height = h / img_height

                yolo_annotation = [f'0 {norm_xc} {norm_yc} {norm_width} {norm_height} \n']

                f.writelines(yolo_annotation)


def save_annotations_st(img, boxes, path):
    img_height = img.shape[0]
    img_width = img.shape[1]
    with open(f'{path}.txt', 'w') as f:
        for box in boxes:
            if len(box) > 0:
                x, y = box[0][0], box[0][1]
                w, h = box[0][2], box[0][3]

                x_center = x + int(w/2)
                y_center = y + int(h/2)

                norm_xc = x_center / img_width
                norm_yc = y_center / img_height
                norm_width = w / img_width
                norm_height = h / img_height

                yolo_annotation = [f'0 {norm_xc} {norm_yc} {norm_width} {norm_height} \n']
                
                f.writelines(yolo_annotation)

