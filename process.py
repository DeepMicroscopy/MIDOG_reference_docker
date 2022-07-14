import SimpleITK
from pathlib import Path

from pandas import DataFrame
import torch
import torchvision
from util.nms_WSI import nms

from evalutils import DetectionAlgorithm
from evalutils.validators import (
    UniquePathIndicesValidator,
    UniqueImagesValidator,
)
import evalutils

import json

from detection import MyMitosisDetection

# TODO: We have this parameter to adapt the paths between local execution and execution in docker. You can use this flag to switch between these two modes.
execute_in_docker = True

class Mitosisdetection(DetectionAlgorithm):
    def __init__(self):
        super().__init__(
            validators=dict(
                input_image=(
                    UniqueImagesValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
            input_path = Path("/input/images/histopathology-roi-cropout/") if execute_in_docker else Path("./test/"),
            output_file = Path("/output/mitotic-figures.json") if execute_in_docker else Path("./output/mitotic-figures.json")
        )
        # TODO: This path should lead to your model weights
        if execute_in_docker:
           path_model = "/opt/algorithm/checkpoints/RetinaNetDA.pth"
        else:
            path_model = "./model_weights/RetinaNetDA.pth"

        self.size = 512
        self.batchsize = 10
        self.detect_thresh = 0.64
        self.nms_thresh = 0.4
        self.level = 0
        # TODO: You may adapt this to your model/algorithm here.
        self.md = MyMitosisDetection(path_model, self.size, self.batchsize, detect_threshold=self.detect_thresh, nms_threshold=self.nms_thresh)
        load_success = self.md.load_model()
        if load_success:
            print("Successfully loaded model.")

    def save(self):
        with open(str(self._output_file), "w") as f:
            json.dump(self._case_results[0], f)

    def process_case(self, *, idx, case):
        # Load and test the image for this case
        input_image, input_image_file_path = self._load_input_image(case=case)

        # Detect and score candidates
        scored_candidates = self.predict(input_image=input_image)

        # Write resulting candidates to result.json for this case
        return dict(type="Multiple points", points=scored_candidates, version={ "major": 1, "minor": 0 })

    def predict(self, *, input_image: SimpleITK.Image) -> DataFrame:
        # Extract a numpy array with image data from the SimpleITK Image
        image_data = SimpleITK.GetArrayFromImage(input_image)

        # TODO: This is the part that you want to adapt to your submission.
        with torch.no_grad():
            result_boxes = self.md.process_image(image_data)

            # perform nms per image:
            print("All computations done, nms as a last step")
            result_boxes = nms(result_boxes, self.nms_thresh)

        candidates = list()
        for i, detection in enumerate(result_boxes):
            # our prediction returns x_1, y_1, x_2, y_2, prediction, score -> transform to center coordinates
            x_1, y_1, x_2, y_2, prediction, score = detection
            coord = tuple(((x_1 + x_2) / 2, (y_1 + y_2) / 2))

            # For the test set, we expect the coordinates in millimeters - this transformation ensures that the pixel
            # coordinates are transformed to mm - if resolution information is available in the .tiff image. If not,
            # pixel coordinates are returned.
            world_coords = input_image.TransformContinuousIndexToPhysicalPoint(
                [c for c in reversed(coord)]
            )
            candidates.append(tuple(reversed(world_coords)))

        # Note: We expect you to perform thresholding for your predictions. For evaluation, no additional thresholding
        # will be performed
        result = [{"point": [x, y, 0]} for x, y in candidates]
        return result


if __name__ == "__main__":
    # loads the image(s), applies DL detection model & saves the result
    Mitosisdetection().process()
