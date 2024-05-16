import numpy as np
import cv2
from ..schemas import BoundingBoxesObject


class Tracker:
    def __init__(self, type_tracer: str = 'csrt'):
        self.tracker = cv2.legacy.TrackerCSRT_create()

    def tracker_init(self, frame, bbox):
        self.tracker.init(frame, bbox)


class TrackersClasses:
    def __init__(self, class_name: str, trackers: list[Tracker]) -> None:
        self.class_name = class_name
        self.trackers = trackers


async def create_Trackers(frame: np.array, data: list[BoundingBoxesObject]) -> list[TrackersClasses]:
    trackers_classes = []
    for c in data:
        trackers = []
        for d in c.bboxes:
            track = Tracker()
            trackers.append(track.tracker)
            track.tracker_init(frame, d)
        trackers_classes.append(TrackersClasses(c.name_class, trackers))
    return trackers_classes