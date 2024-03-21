import cv2
import numpy as np
import os
# import supervision as sv
from videoprocessor.utils.tools.annotation_tool import threshold, morph_op, get_filtered_bboxes, get_filtered_bboxes_xywh

from fastsam import FastSAM, FastSAMPrompt, FastSAMPredictor
from fastsam.utils import convert_box_xywh_to_xyxy


class NewFastSAMModel():
    def __init__(self, model_path: str) -> None:
        self.device = 'cpu'
        self.model = FastSAM(model_path)
        overrides = self.model.overrides.copy()
        overrides['conf'] = 0.25
        overrides.update(device=self.device, retina_masks=True, imgsz=1024, conf=0.7, iou=0.9)
        overrides['mode'] = 'predict'
        assert overrides['mode'] in ['track', 'predict']
        overrides['save'] = False
        self.model.predictor = FastSAMPredictor(overrides=overrides)
        self.model.predictor.setup_model(model=self.model.model, verbose=False)
    
    def set_prompt(self, image: np.ndarray):
        everything_results = self.model.predictor(image)
        self.prompt_process = FastSAMPrompt(image, everything_results, device=self.device)

    def get_prompt_box(self, bbox):
        box_prompt = convert_box_xywh_to_xyxy(bbox)
        self.mask = self.prompt_process.box_prompt(box_prompt)
        image_mask = self._convert_image()
        return self._get_new_bbox(image_mask)

    def _convert_image(self):
        mask = self.mask.astype(int)
        mask = (mask[0] * 255).astype(np.uint8)
        mask = cv2.merge((mask, mask, mask))
        return mask
    
    def _get_new_bbox(self, image_mask):
        image = cv2.cvtColor(image_mask, cv2.COLOR_RGBA2GRAY)
        thresh_stags = threshold(image, thresh=110, mode='direct')
        bbox = get_filtered_bboxes_xywh(thresh_stags, min_area_ratio=0.001)
        return bbox
    
    # def annotate_image(self, image: np.ndarray) -> np.ndarray:
    #     xyxy = sv.mask_to_xyxy(masks=self.mask)
    #     detections = sv.Detections(xyxy=xyxy, mask=self.mask)
    #     mask_annotator = sv.MaskAnnotator(color=sv.Color.blue(), color_map='index')
    #     return mask_annotator.annotate(scene=image.copy(), detections=detections)
    
    def annotated_frame(self) -> np.ndarray:
        annotated_frame = self.prompt_process.plot_to_result(
                annotations=self.mask,
                withContours=False,
                better_quality=False,
            )
        return annotated_frame