FROM gcr.io/tensorflow/tensorflow:latest-devel

#build tensorflow from source to enable all the optimizations
RUN cd /tensorflow && bazel build --config opt --copt=-msse4.1 --copt=-msse4.2 --copt=-mavx --copt=-mavx2 --copt=-mfma //tensorflow/tools/pip_package:build_pip_package
RUN cd /tensorflow && bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
RUN pip install --force-reinstall --upgrade /tmp/tensorflow_pkg/tensorflow-1.2.1-cp27-cp27mu-linux_x86_64.whl

RUN cd /tensorflow && bazel build tensorflow/examples/image_retraining:retrain
RUN cd /tensorflow && bazel build tensorflow/python/tools:strip_unused
RUN cd /tensorflow && bazel build tensorflow/tools/quantization:quantize_graph

# install python libraries
RUN pip install pillow
RUN pip install future --upgrade

WORKDIR /app

