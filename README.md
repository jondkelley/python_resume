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

Browse this repository to see my skills in Python, Flask, Markdown, and file conversions as well as my resume itself. This also builds cleanly into a `Dockerfile` and can be deployed via `docker-compose` and Kubernetes! This code could be better at mimicking an MIT graduate, but hey I wrote the bulk of this on a Sunday afternoon. C'mon!

### My resume

See the interactive live version of this [Jon-Kelley.com](https://jon-kelley.com) powered by Kubernetes!

### The premise for the project

I wrote this because I was tired of directly maintaining a markdown resume and converting it to DOCX/PDF for recruiters. I figured why not build something that makes my life easier -- the same reason Devops models exist in the first place. I decided to showcase some of my skills in devops while I was at it. Who could ask for a better resume?

### Architecture Overview

A simplified component diagram of this architecture is below which should give you a simplified idea of how the codebase works, even if you're not technical.

![](conceptual_architecture_small.jpg)

### K8s Architecture Overview

![](k8s-architecture.png)

### Competencies Demonstrated

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
