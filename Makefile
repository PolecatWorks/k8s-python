NAME=k8s-python
TAG ?= 0.3.0
REPO ?= dockerreg.k8s:5000/polecatworks

DOCKER=docker


.ONESHELL:
docker-build:
	{ \
	$(DOCKER) build container -t $(NAME) -f Dockerfile; \
	$(DOCKER) image ls $(NAME); \
	}

docker:
	$(DOCKER)  build container -t $(NAME) -f container/Dockerfile

dockerx:
	$(DOCKER)  buildx build --push container -t $(REPO)/$(NAME):$(TAG) -f container/Dockerfile --platform linux/arm64/v8,linux/amd64
