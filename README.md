# Docker image of reference algorithm for MIDOG 2021 challenge.

Credits: F. Wilm, K. Breininger, M. Aubreville

This docker image contains a reference implementation of a domain-adversarial training based on RetinaNet, provided by Frauke Wilm (Friedrich-Alexander-Universität Erlangen-Nürnberg, Germany) for the MIDOG challenge.

The container shall serve as an example of how we (and the grand-challenge plattform) expect the outputs to look like. At the same time, it serves as a template for you to implement your own algorithm for submission at MIDOG 2021.

You will have to provide all files to run your model in a docker container. This example may be of help for this. We also provide a quick explanation of how the container works [here](https://www.youtube.com/watch?v=Zkhrwark3bg).

For reference, you may also want to read the blog post of grand-challenge.org on [how to create an algorithm](https://grand-challenge.org/blogs/create-an-algorithm/).

## Content:
1. [Prerequisites](#prerequisites)
2. [An overview of the structure of this example](#overview)
3. [Packing your algorithm into a docker container image](#todocker)
4. [Building your container](#build)
5. [Testing your container](#test)
6. [Generating the bundle for uploading your algorithm](#export)

## 1. Prerequisites <a name="prerequisites"></a>

The container is based on docker, so you need to [install docker first](https://www.docker.com/get-started). 

Second, you need to clone this repository:
```
git clone https://github.com/DeepPathology/MIDOG_reference_docker
```

You will also need evalutils (provided by grand-challenge):
```
pip install evalutils
```

Optional: If you want to have GPU support for local testing, you want to install the [NVIDIA container toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

As stated by the grand-challenge team:
>Windows tip: It is highly recommended to install [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to work with Docker on a Linux environment within Windows. Please make sure to install WSL 2 by following the instructions on the same page. In this tutorial, we have used WSL 2 with Ubuntu 18.04 LTS. Also, note that the basic version of WSL 2 does not come with GPU support. Please [watch the official tutorial by Microsoft on installing WSL 2 with GPU support](https://www.youtube.com/watch?v=PdxXlZJiuxA). The alternative is to work purely out of Ubuntu, or any other flavor of Linux.

## 2. An overview of the structure of this example <a name="overview"></a>

This example is a RetinaNet implementation, extended by a domain-adversarial branch. 
- The main processing (inference) is done in the file [detection.py](detection.py). It provides the class *MyMitosisDetection*, which loads the model and provides the method *process_image()* that takes an individual test image as numpy array as an input and returns the detections on said image.
- The main file that is executed by the container is [process.py](process.py). It imports and instanciates the model (*MyMitosisDetection*). It then loads all images that are part of the test set and processes each of them (using the *process_image()* method). As post-processing, it will also perform a final non-maxima suppression on the image, before creating the return dictionary which contains all individual detected points, which are ultimately stored in the file `/output/mitotic-figures.json`. 

The output file is a list of dictionaries (one dictionary for each input file), and has the following format:

```
[{
    "type": "Multiple points",
    "points": [
        {
            "point": [
                0.14647372756903898,
                0.1580733550628604,
                0
            ]
        },
        {
            "point": [
                0.11008273935312868,
                0.03707331924495862,
                0
            ]
        }
    ],
    "version": {
        "major": 1,
        "minor": 0
    }
}]
```

## 3. Embedding your algorithm into an algorithm docker container <a name="todocker"></a>

We encourage you to adapt this example to your needs and insert your mitosis detection solution. You can adapt the code, remove & code files as needed and adapt parameters, thresholds and other aspects. As discussed above, the main file that is executed by the container is [process.py](process.py). Here, we have marked the most relevant code lines with `TODO`.

To test this container locally without a docker container, you may set the `execute_in_docker` flag to false - this sets all paths to relative paths. Don't forget to set it back to true when you want to switch back to the docker container setting.

If you need a different base image to build your container (e.g., Tensorflow instead of Pytorch, or a different version), if you need additional libraries and to make sure that all source files (and weights) are copied to the docker container, you will have to adapt the [Dockerfile](Dockerfile) and the [requirements.txt](requirements.txt) file accordingly.

Kindly refer to the image below to identify the relevant points:
![dockerfile_img](https://user-images.githubusercontent.com/43467166/128198999-37dd613d-aeef-41a6-9875-9fdf29db4717.png)


## 4. Building your container <a name="build"></a>

To test if all dependencies are met, you should run the file `build.bat` (Windows) / `build.sh` (Linux) to build the docker container. Please note that the next step (testing the container) also runs a build, so this step is not mandatory if you are certain that everything is set up correctly.

## 5. Testing your container <a name="test"></a>

To test your container, you should run `test.bat` (on Windows) or `test.sh` (on Linux, might require sudo priviledges). This will run the test image(s) provided in the test folder through your model. It will check them against what you provide in `test/expected_output.json`. Be aware that this will, of course, initially not be equal to the demo detections we put there for testing our reference model.

## 6. Generating the bundle for uploading your algorithm <a name="export"></a>

Finally, you need to run the `export.sh` (Linux) or `export.bat` script to package your docker image. This step creates a file with the extension "tar.gz", which you can then upload to grand-challenge to submit your algorithm.

## 7. Creating an "Algorithm" on GrandChallenge and submitting your solution to the MIDOG Challenge

** Note: Submission to grand-challenge.org will open on August 15th. **

In order to submit your docker container, you first have to add an **Algorithm** entry for your docker container [here] https://grand-challenge.org/algorithms/create/.

Please enter a name for the algorithm:

![algo_title](https://user-images.githubusercontent.com/10051592/128369966-4fe08d95-e158-46c3-9f8e-3a7a320b0fdb.jpg)

And set the following properties

![createalgo2](https://user-images.githubusercontent.com/10051592/128370393-3631bede-586e-4b4e-ad87-2500b11c152e.jpg)

After saving, you can add your docker container (you can also overwrite your container here):

![uploadcontainer](https://user-images.githubusercontent.com/10051592/128370733-7445e252-a354-4c44-9155-9f232cd9f220.jpg)

Please note that it can take a while (several minutes) until the container becomes active. You can determine which one is active in the same dialog:

![containeractive](https://user-images.githubusercontent.com/10051592/128373241-83102a43-aad7-4457-b068-a6c7cc5a3b98.jpg)

You can also try out your algorithm. Please note that you will require an image that has the DPI property set in order to use this function. You can use the image test/007.tiff provided as part of this container as test image (it contains mitotic figures).

![tryout](https://user-images.githubusercontent.com/10051592/128373614-30b76cf6-2b2d-4d5d-87db-b8c67b47b64f.jpg)

Finally, you can submit your docker container to MIDOG:

![submit_container](https://user-images.githubusercontent.com/10051592/128371715-d8385754-806e-4420-ac5e-4c25cc38112a.jpg)

## General remarks
- The training is not done as part of the docker container, so please make sure that you only run inference within the container.


