from src.videoprocessor.utils.tools.contour_detector import threshold, get_filtered_bboxes_xywh


class ExportObject():
    def __init__(self, mask, name_class) -> None:
        self.mask = mask
        self.name_class = name_class
        self.coordinates = []


class ExportImage():
    def __init__(self, image, objects: list[ExportObject]) -> None:
        self.image = image
        self.objects = objects



class YoloSave():
    @classmethod
    def getting_coordinates(cls, image_mask):
        thresh_stags = threshold(image_mask, thresh=110, mode='direct')
        bboxes = get_filtered_bboxes_xywh(thresh_stags, min_area_ratio=0.001)
        return bboxes


    @classmethod
    def txt_class_save(cls):
        pass


    @classmethod
    def txt_frame_save(cls, image: ExportImage, path: str, names_class: list[str]):
        nc = {}
        for i in range(len(names_class)):
            nc[names_class] = i

        img_height = image.image.shape[0]
        img_width = image.image.shape[1]
        with open(f'{path}.txt', 'w') as file:
            for class_box in image.objects: # ignore type: ExportObject
                for box in class_box.coordinates:
                    x, y = box[0][0], box[0][1]
                    w, h = box[0][2], box[0][3]

                    x_center = x + int(w/2)
                    y_center = y + int(h/2)

                    norm_xc = x_center / img_width
                    norm_yc = y_center / img_height
                    norm_width = w / img_width
                    norm_height = h / img_height

                    yolo_annotation = [f'{nc[names_class]} {norm_xc} {norm_yc} {norm_width} {norm_height} \n']
                    
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


