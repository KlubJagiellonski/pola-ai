#### Buid Docker image

```
$ cd docker 
$ docker build -t pola-ai-image-tensorflow-latest-cpu .
```

#### Run Docker container

```
$ cd data
$ docker run --rm -it -v `pwd`:/app pola-ai-image-tensorflow-latest-cpu
```

#### Retrain Inception v3 model for mobile inside Docker container 

```
$ cd /app
$ rm -rf bottleneck inc_v3 pola_retrained.pb pola_retrained_labels.txt q_stripped_pola_retrained.pb stripped_pola_retrained.pb
$ /tensorflow/bazel-bin/tensorflow/examples/image_retraining/retrain --model_dir=inc_v3 --output_graph=pola_retrained.pb --output_labels=pola_retrained_labels.txt --image_dir=Pola_jpg --bottleneck_dir=bottleneck
$ /tensorflow/bazel-bin/tensorflow/python/tools/strip_unused --input_graph=pola_retrained.pb --output_graph=stripped_pola_retrained.pb --input_node_names=Mul --output_node_names=final_result --input_binary=true
$ /tensorflow/bazel-bin/tensorflow/tools/quantization/quantize_graph --input=stripped_pola_retrained.pb --output_node_names=final_result --output=q_stripped_pola_retrained.pb --mode=weights
```

#### Copy retrained model and labels to iOS app
```
$ cd data
$ cp q_stripped_pola_retrained.pb pola_retrained_labels.txt ../ios_camera/data
```