import os
import numpy as np

from pathlib import Path


class SrcParams:
    def __init__(self):
        
        self.tracked_class = 'car'
        
        # Load class names
        self.CLASSES = []
        # work_dir = Path(os.getcwd()).parts[1]
        work_dir = os.getcwd()
        classes_file_path = os.path.join(work_dir, "DATA/classes.names")
        # classes_file_path = f'/{work_dir}/DATA/classes.names'
        with open(classes_file_path) as f:
            self.CLASSES = f.read().strip().split('\n')
            
        self.max_age = 60
        
        # Transparency for overlays
        self.color_yellow = (0, 255, 255)
        self.color_red = (0, 0, 255)
        self.color_blue = (255, 0, 0)
        self.color_green = (0, 255, 0) # box and text color
        self.overlays_alpha = 0.4  
        
        # Lane definitions
        yellow_zone_1 = np.array([[231, 38], [297, 35] , [339, 135], [221, 130]], np.int32).reshape((-1, 1, 2))
        yellow_zone_2 = np.array([[221, 130], [339, 135] , [318, 348], [76, 322]], np.int32).reshape((-1, 1, 2))
        red_zone_1 = np.array([[296, 31], [329, 30], [432, 142], [362, 150]], np.int32).reshape((-1, 1, 2))
        red_zone_2 = np.array([[362, 150], [432, 142], [493, 358], [359, 364]], np.int32).reshape((-1, 1, 2))
        blue_zone_1 = np.array([[856, 286], [728, 208], [630, 280], [793, 323] ], np.int32).reshape((-1, 1, 2))
        blue_zone_2 = np.array([[793, 323], [625, 280], [565, 358], [757, 401]], np.int32).reshape((-1, 1, 2))

        yellow_zone = np.vstack((yellow_zone_1, yellow_zone_2))
        red_zone = np.vstack((red_zone_1, red_zone_2))
        blue_zone = np.vstack((blue_zone_1, blue_zone_2))
        self.lane_1, self.lane_2, self.lane_3 = [yellow_zone], [red_zone], [blue_zone]

        self.confidence_thres = 0.4
        self.iou_thres = 0.5