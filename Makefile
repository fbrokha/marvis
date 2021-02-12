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
	docker tag osmhpi/marvis:base-${MARVIS_TAG} osmhpi/marvis:base
	docker tag osmhpi/marvis:${MARVIS_TAG} osmhpi/marvis:latest
	docker tag osmhpi/marvis:dev-${MARVIS_TAG} osmhpi/marvis:dev

marvis-base:
	${docker_build} -t osmhpi/marvis:base-${MARVIS_TAG} docker/marvis-base

marvis:
	${docker_build} -t osmhpi/marvis:${MARVIS_TAG} . -f docker/Dockerfile

marvis-dev:
	${docker_build} -t osmhpi/marvis:dev-${MARVIS_TAG} docker/marvis-dev

pull-latest:
	docker pull osmhpi/marvis:base
	docker pull osmhpi/marvis:latest
	docker pull osmhpi/marvis:dev

push:
	docker push osmhpi/marvis:base-${MARVIS_TAG}
	docker push osmhpi/marvis:${MARVIS_TAG}
	docker push osmhpi/marvis:dev-${MARVIS_TAG}

push-latest: git-is-clean push
	docker push osmhpi/marvis:base
	docker push osmhpi/marvis:latest
	docker push osmhpi/marvis:dev

docs:
	$(MAKE) -C docs
