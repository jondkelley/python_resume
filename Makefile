docker-build:
	# Building the docker image "resume"
	docker build -t resume .

docker-testrun:
	# Running the docker image, linked to a redis container
	docker run --rm -ti -p 5001:5001 -e "SECRET_KEY=abc123" resume
