run:
	docker-compose up

test:
	docker-compose up -d; \
	export UPDATE_SECRET=`grep UPDATE_SECRET docker-compose.yml  | head -1 | awk '{ print $2 }' | cut -d'=' -f2`; \
	pytest --docker-compose-no-build --use-running-containers; \
	docker-compose down

build:
	docker build -t local-resume/python_resume .
	docker build -t local-resume/pandoc_resume -f pandoc-sidecar/Dockerfile  pandoc-sidecar/
	@$(eval python_resume=`docker images local-resume/python_resume  --format "{{.ID}}"`)
	docker tag $(python_resume) jondkelley/python_resume:latest
	@$(eval pandoc_resume=`docker images local-resume/pandoc_resume  --format "{{.ID}}"`)
	docker tag $(pandoc_resume) jondkelley/pandoc_resume:latest

push:
	docker push jondkelley/python_resume:latest
	docker push jondkelley/pandoc_resume:latest
