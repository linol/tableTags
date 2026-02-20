IMAGE_NAME ?= tabletag_img
CONTAINER_NAME ?= tabletag_ctn
SOURCE_PATH ?= .
PORT ?= 5000
## list of commands
help:		## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)
 
build:  	## build image
	sudo docker build --tag ${IMAGE_NAME} .
rebuild: 	## build image no cache
	sudo docker build --no-cache --tag ${IMAGE_NAME} .
run: 		## run container in mount volume
	sudo docker run -d --name ${CONTAINER_NAME} --mount type=bind,src=${SOURCE_PATH},dst=/app -p ${PORT}:5000 ${IMAGE_NAME}
stop: 		## stop container
	sudo docker stop ${CONTAINER_NAME}
rm: 		## remove container
	sudo docker rm ${CONTAINER_NAME}
