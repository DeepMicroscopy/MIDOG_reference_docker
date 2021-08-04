# Docker image of reference algorithm for MIDOG 2021 challenge.

Credits: F. Wilm, K. Breininger, M. Aubreville

This docker image contains a reference implementation of a domain-adversarial training based on RetinaNet, provided by Frauke Wilm (Friedrich-Alexander-Universität Erlangen-Nürnberg, Germany) for the MIDOG challenge.

The container shall serve as an example of how we (and the grand-challenge plattform) expect the outputs to look like. At the same time, it serves as a template for you to implement your own algorithm for submission at MIDOG 2021.

## 1. Prerequisites

The container is based on docker, so you need to [install docker first](https://www.docker.com/get-started). 

Second, you need to clone this repository:
> git clone https://github.com/DeepPathology/MIDOG_reference_docker

As stated by the grand-challenge team:
>Windows tip: It is highly recommended to install [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to work with Docker on a Linux environment within Windows. Please make sure to install WSL 2 by following the instructions on the same page. In this tutorial, we have used WSL 2 with Ubuntu 18.04 LTS. Also, note that the basic version of WSL 2 does not come with GPU support. Please [watch the official tutorial by Microsoft on installing WSL 2 with GPU support](https://www.youtube.com/watch?v=PdxXlZJiuxA). The alternative is to work purely out of Ubuntu, or any other flavor of Linux.

## 2. Embedding your algorithm into an algorithm docker container

You will have to provide all files to run your model in a docker container. This example may be of help for this. We also provide a quick explanation of how the container works [here](https://youtube.com).

For reference, you may also want to read the blog post of grand-challenge.org about [how to create an algorithm](https://grand-challenge.org/blogs/create-an-algorithm/)

## 3. An overview of the structure of this example




