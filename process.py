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

import json

from detection import MyMitosisDetection

class Mitosisdetection(DetectionAlgorithm):
    def __init__(self):
        super().__init__(
            validators=dict(
                input_image=(
                    UniqueImagesValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
            output_file = Path("/output/mitotic-figures.json") 
        )

        path_model = "/opt/algorithm/checkpoints/RetinaNetDA.pth" 
        self.size = 512
        self.batchsize = 10
        self.detect_thresh = 0.62
        self.nms_thresh = 0.4
        self.level = 0
        self.md = MyMitosisDetection(path_model, self.size, self.batchsize, detect_threshold=self.detect_thresh, nms_threshold=self.nms_thresh)
        load_success = self.md.load_model()
        if load_success:
            print("Successfully loaded model.")

    def save(self):
        print(">>>>>>>>", flush=True)
        print(self._output_file, flush=True)
        print(self._case_results)
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

        with torch.no_grad():
            result_boxes = self.md.process_image(image_data)

            # perform nms per image:
            print("All computations done, nms as a last step")
            result_boxes = nms(result_boxes, self.nms_thresh)

        candidates = list()
        candidate_scores = list()
        for i, detection in enumerate(result_boxes):
            # our prediction returns x_1, y_1, x_2, y_2, prediction, score -> transform to center coordinates
            x_1, y_1, x_2, y_2, prediction, score = detection
            candidates.append(tuple(((x_1 + x_2) / 2, (y_1 + y_2) / 2)))
            candidate_scores.append(score)


        result = [{"point": [x, y, 0]} for x, y in candidates]
        # Convert serialized candidates to a pandas.DataFrame
        return result


if __name__ == "__main__":
    print(torchvision.__version__)
    Mitosisdetection().process()
