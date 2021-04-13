# Resume - Jonathan D Kelley - jon-kelley.com

This Git repository serves two purposes:

* A) to render my resume in HTML(5) / Bootstrap / Markdown / PDF / DOCX
* B) to showcase my skills as a "Devops Engineer" by building this piece of engineering with (mostly) best practices.

# Table of Contents

   * [Resume - Jonathan D Kelley - jon-kelley.com](#resume---jonathan-d-kelley---jon-kelleycom)
      * [Introduction](#introduction)
         * [The showcase](#the-showcase)
         * [My resume](#my-resume)
         * [The premise for the project](#the-premise-for-the-project)
         * [Architecture Overview](#architecture-overview)
         * [K8s Architecture Overview](#k8s-architecture-overview)
         * [Competencies Demonstrated](#competencies-demonstrated)
      * [Quick Start Guide](#quick-start-guide)
         * [Run from docker-compose](#run-from-docker-compose)
         * [Kubernetes install](#kubernetes-install)
            * [Install Pod, PVC and Service](#install-pod-pvc-and-service)
         * [Running in minikube](#running-in-minikube)
            * [Install Pod](#install-pod)
            * [Expose Service](#expose-service)
         * [Local install](#local-install)
      * [Build and Publish using the Makefile](#build-and-publish-using-the-makefile)
      * [Contributers](#contributers)
      * [Inspiration](#inspiration)


## Introduction

### The showcase

This repository is a showcase around docker, kubernetes, python, flask, markdown, json, REST and sidecars to make a very simple app serve my resume. From `Makefile` to production you'll see how I've deployed my website, and the Flask app I wrote lives in the center of all of this. My flask app even permits [being updated](https://jon-kelley.com/resume/update) from the `resume.json` in this repository after it's been built to make dynamic updates post-deployment easier.

### My resume

See this code live on my website [Jon-Kelley.com](https://jon-kelley.com) 100% powered by Kubernetes!

### The premise for the project

For years I managed a resume in markdown and used pandoc to generate PDF/DOCX files and manually updated my website. Portability and maintainability was always a burden for me. After getting hired I'd sometimes stop paying for hosting and then the code would disappear and I'd have to set everything back up via cronjobs (and redesign my site) when job hunting resumed.

That's why this repository was born! We can dockerize anything, why not my resume? Now I just update `resume.json` and everything can be 100% automatic on top of kubernetes. This actively showcases how devops can help your company or organization focus on what really matters -- and leave the endless toil out of it.

### Architecture Overview

A simplified component diagram of this architecture is below which should give you a simplified idea of how the codebase works, even if you're not technical.

![](conceptual_architecture_small.jpg)

### K8s Architecture Overview

![](k8s-architecture.png)

### Competencies Demonstrated

I believe this project emphasizes core competenencies around writing, containerizing and deploying software.

Some core competencies proven here are:

* Docker
* docker-compose
* kubernetes (and sidecars)
* Makefile (m4 macro language)
* Docker build/publish scripts
* Docker volumes
* Python3
* Flask
* BASH
* Jinja2
* Pandoc
* HTML5, Jquery, CSS, and Bootstrap
* Software integration
* Good documentation

## Quick Start Guide

### Run from docker-compose

This is how I prefer to develop my Docker projects.

If you have docker-compose installed, you can simply run

```
docker-compose build
docker-compose up
```

Then open [127.0.0.1:5001](http://127.0.0.1:5001).

### Kubernetes install

#### Install Pod, PVC and Service

```
kubectl apply -f https://raw.githubusercontent.com/jondkelley/python_resume/master/k8s-resources/k8s-baremetal.yaml
```

### Running in minikube

#### Install Pod
```
kubectl apply -f https://raw.githubusercontent.com/jondkelley/python_resume/master/k8s-resources/k8s-minikube.yaml
```

#### Expose Service
```
kubectl expose deployment jonk-resume-app --type=NodePort
minikube service jonk-resume-app --url
```

You'll see output similar to
```
 🏃  Starting tunnel for service jonk-resume-app.
|-----------|-----------------|-------------|------------------------|
| NAMESPACE |      NAME       | TARGET PORT |          URL           |
|-----------|-----------------|-------------|------------------------|
| default   | jonk-resume-app |             | http://127.0.0.1:12345 |
|-----------|-----------------|-------------|------------------------|
```

You can visit http://127.0.0.1:12345 to use the application.

### Local install

Always an option, but the pandoc container won't work with this, so the hard-copy resume links will throw errors.

    git clone https://github.com/jondkelley/python_resume.git
    cd python_resume
    virtualenv venv
    source venv/bin/activate
    python3 setup.py install
    myresume &

Then open [127.0.0.1:5001](http://127.0.0.1:5001).

## Build and Publish using the Makefile

Quickly make and publish artifacts to dockerhub.

```
make build
make push
```

## Contributers

* 2021 Jonathan Kelley

## Inspiration

This Resume was inspired by an interactive dynamic resume created by web designer **[Pascal Van Gemert](http://pascalvangemert.nl/)** ([Github](https://github.com/pascalvgemert/resume)).

I ported his PHP / bootstrap framework over to Python / Flask / Jinja2, with my own inspiration along the way. Then I Dockerized my project and made it work on my bare metal kubernetes cluster using PVC's and MetalLB. Docker-compose is available for local development.

The container is built using a sidecar running pandoc in a bash loop, and a shared PVC to make various rendered resume formats (every 10 seconds) available to the Flask webserver.
