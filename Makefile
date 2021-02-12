export NS3_TAG ?= 3.30
export SUMO_TAG ?= 1.4.0
MARVIS_TAG ?= $(shell if [ -z "`git status --porcelain`" ]; then git rev-parse --short HEAD; else echo dirty; fi)
export MARVIS_TAG := ${MARVIS_TAG}

docker_build := docker build --build-arg NS3_TAG --build-arg SUMO_TAG --build-arg MARVIS_TAG

.PHONY: latest marvis-base marvis marvis-dev docs

all: marvis-base marvis marvis-dev
	#
	# build tag ${MARVIS_TAG}
	#

git-is-clean:
ifeq '${shell git status --porcelain}' ''
	@ # git is clean
else
	${error Git status is not clean.}
endif


latest: git-is-clean all
	docker tag diselab/marvis:base-${MARVIS_TAG} diselab/marvis:base
	docker tag diselab/marvis:${MARVIS_TAG} diselab/marvis:latest
	docker tag diselab/marvis:dev-${MARVIS_TAG} diselab/marvis:dev

marvis-base:
	${docker_build} -t diselab/marvis:base-${MARVIS_TAG} docker/marvis-base

marvis:
	${docker_build} -t diselab/marvis:${MARVIS_TAG} . -f docker/Dockerfile

marvis-dev:
	${docker_build} -t diselab/marvis:dev-${MARVIS_TAG} docker/marvis-dev

pull-latest:
	docker pull diselab/marvis:base
	docker pull diselab/marvis:latest
	docker pull diselab/marvis:dev

push:
	docker push diselab/marvis:base-${MARVIS_TAG}
	docker push diselab/marvis:${MARVIS_TAG}
	docker push diselab/marvis:dev-${MARVIS_TAG}

push-latest: git-is-clean push
	docker push diselab/marvis:base
	docker push diselab/marvis:latest
	docker push diselab/marvis:dev

docs:
	$(MAKE) -C docs
