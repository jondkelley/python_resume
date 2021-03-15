Resume - Jonathan D Kelley
=====================================================

I build this code to serve as an interactive resume on my website [jon-kelley.com](https://jon-kelley.com).

This is designed to run on Kubernetes and runs in a Python3 container.

## Quick Start

Execute this:

    git clone https://github.com/jondkelley/resume.git
    cd resume
    virtualenv venv
    source venv/bin/activate
    python3 setup.py install
    resume &

Then open [127.0.0.1:5001](http://127.0.0.1:5001).

## Running in docker-compose

If you have docker-compose installed, you can simply run

```
docker-compose build
docker-compose up
```

Then open [127.0.0.1:5001](http://127.0.0.1:5001).

## Running as Docker container

The provided `Dockerfile` can be used to create the according image. The `Makefile` contains example commands to build the image and run a container from the image.

When running the image, make sure to get your links right. For example, if your redis server is running in a container named `myredis`, start your rebrow container like this:

```
docker run --rm -ti -p 5001:5001 jondkelley/resume:latest
```

Then access resume via `http://<your-docker-ip>:5001/` and set the host name in the login screen to `redis` or your Redis instance if it's something else..

## Contributers

* 2020 Jonathan Kelley

## License

Copyleft, but please buy me a beer if you use this code for your own self-promotion.

Paypal: jonkelley@gmail.com

## Inspired by

This Resume was inspired by a PHP driven dynamic resume created by designer **Pascal Van Gemert**.

I ported his PHP / Laravel code straight over to Python / Flask / Jinja2 and made changes to suit my needs.
Finally I dockerized this project for Kubernetes deployment.

# http://pascalvangemert.nl/
# https://github.com/pascalvgemert/resume
