# Docker image of reference algorithm for MIDOG 2021 challenge.

Credits: F. Wilm, K. Breininger, M. Aubreville

This docker image contains a reference implementation of a domain-adversarial training based on RetinaNet, provided by Frauke Wilm (Friedrich-Alexander-Universität Erlangen-Nürnberg, Germany) for the MIDOG challenge.

The container shall serve as an example of how we (and the grand-challenge plattform) expect the outputs to look like. At the same time, it serves as a template for you to implement your own algorithm for submission at MIDOG 2021.

## 1. Prerequisites

The container is based on docker, so you need to [install docker first](https://www.docker.com/get-started). 

Second, you need to clone this repository:
> git clone https://github.com/DeepPathology/MIDOG_reference_docker

You will also need evalutils (provided by grand-challenge):
> pip install evalutils

As stated by the grand-challenge team:
>Windows tip: It is highly recommended to install [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to work with Docker on a Linux environment within Windows. Please make sure to install WSL 2 by following the instructions on the same page. In this tutorial, we have used WSL 2 with Ubuntu 18.04 LTS. Also, note that the basic version of WSL 2 does not come with GPU support. Please [watch the official tutorial by Microsoft on installing WSL 2 with GPU support](https://www.youtube.com/watch?v=PdxXlZJiuxA). The alternative is to work purely out of Ubuntu, or any other flavor of Linux.

## 2. Embedding your algorithm into an algorithm docker container

You will have to provide all files to run your model in a docker container. This example may be of help for this. We also provide a quick explanation of how the container works [here](https://youtube.com).

For reference, you may also want to read the blog post of grand-challenge.org about [how to create an algorithm](https://grand-challenge.org/blogs/create-an-algorithm/)

## 3. An overview of the structure of this example

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
                644.0,
                695.0,
                0
            ]
        },
        {
            "point": [
                484.0,
                163.0,
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



## General remarks
- The training is not done as part of the docker container, so please make sure that you only run inference within the container.


