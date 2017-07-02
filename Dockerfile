FROM gcr.io/tensorflow/tensorflow:latest-devel

#update tensorflow
RUN cd /tensorflow && git pull

# install python libraries
RUN pip install pillow

