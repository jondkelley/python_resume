Resume - Jonathan D Kelley - jon-kelley.com
=====================================================

This Git repository serves two purposes:

* A) to render my resume in HTML(5) / Bootstrap / Markdown / PDF / DOCX
* B) to showcase my skills as a "Devops Engineer" by building this piece of engineering.

##### The showcase.

Browse this repository to see my skills in Python, Flask, Markdown, and file conversions as well as my resume itself. This also builds cleanly into a `Dockerfile` and can be deployed via `docker-compose` and Kubernetes! This code could be better at mimicking an MIT graduate, but hey I wrote the bulk of this on a Sunday afternoon. C'mon!

##### My resume.

See the interactive live version of this [Jon-Kelley.com](https://jon-kelley.com) powered by Kubernetes!

##### The premise for this project.

I wrote this because I was tired of directly maintaining a markdown resume and converting it to DOCX/PDF for recruiters. I figured why not build something that makes my life easier -- the same reason Devops models exist in the firts place?


##### The architecture

A simplified component diagram of this architecture is below which should give you a simplified idea of how the codebase works, even if you're not technical.

![](conceptual_architecture_small.jpg)

## Quick Start

## Running in docker-compose

This is how I prefer to develop my Docker projects.

If you have docker-compose installed, you can simply run

```
docker-compose build
docker-compose up
```

Then open [127.0.0.1:5001](http://127.0.0.1:5001).

### Local install

    git clone https://github.com/jondkelley/resume.git
    cd resume
    virtualenv venv
    source venv/bin/activate
    python3 setup.py install
    resume &

Then open [127.0.0.1:5001](http://127.0.0.1:5001).

### Kubernetes install

#### Generate Service

Install the loadbalancer:

```
kubectl apply -f https://raw.githubusercontent.com/jondkelley/python_resume/master/k8s-resources/clusterip.yaml
```

or install a service IP

```
kubectl apply -f https://raw.githubusercontent.com/jondkelley/python_resume/master/k8s-resources/loadbalancer.yaml
```

#### Install Pods and PVC

```
kubectl apply -f https://raw.githubusercontent.com/jondkelley/python_resume/master/k8s-resources/k8s.yaml
```

## Running as a single container

The provided `Dockerfile` can be used to create the according image. The `Makefile` contains example commands to build the image and run a container from the image.

When running the image, make sure to get your links right. For example, if your redis server is running in a container named `myredis`, start your rebrow container like this:

```
docker run --rm -ti -p 5001:5001 jondkelley/python_resume:latest
```

Then access resume via `http://<your-docker-ip>:5001/` and set the host name in the login screen to `redis` or your Redis instance if it's something else..

## Contributers

* 2021 Jonathan Kelley

## Inspiration

This Resume was inspired by an interactive dynamic resume created by web designer **[Pascal Van Gemert](http://pascalvangemert.nl/)** ([Github](https://github.com/pascalvgemert/resume)).

I ported his PHP / bootstrap framework over to Python / Flask / Jinja2, with my own inspiration along the way. Then I Dockerized my project and made it work on my bare metal kubernetes cluster using PVC's and MetalLB. Docker-compose is available for local development. The container is built using a sidecar running pandoc in a bash loop, and a shared PVC to make various rendered resume formats (every 10 seconds) available to the Flask webserver.
