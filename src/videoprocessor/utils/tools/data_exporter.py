from src.videoprocessor.utils.video_handler import Frame, ROIsObject


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


def save_yolo(frame: Frame, path: str, names_class: list[str]):
    nc = {}
    for i in range(len(names_class)):
        nc[names_class] = i

    img_height = frame.frame.shape[0]
    img_width = frame.frame.shape[1]
    with open(f'{path}.txt', 'w') as file:
        for class_box in frame.names_classes:
            for box in class_box.ROIs:
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