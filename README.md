#### Install Tensorflow
Based on: https://www.tensorflow.org/install/pip
```
$ cd data
$ sudo pip3 install -U virtualenv
$ virtualenv --system-site-packages -p python3 ./venv
$ source ./venv/bin/activate
$ pip install --upgrade pip
$ pip install --upgrade tensorflow==1.12.0
$ pip install --upgrade tensorflow-hub==40.6.2
$ pip install --upgrade requests
$ pip install --upgrade pillow


$ deactivate # run when finished
```

#### Download pictures from Pola
```
$ cd data
$ python get_ai_pics.py $SHARED_SECRET Pola_ai
```

#### Retrain MobileNet v2 model
# https://raw.githubusercontent.com/tensorflow/hub/master/examples/image_retraining/retrain.py
```
$ rm -rf model bottleneck pola_retrained.pb pola_retrained_labels.txt pola_retrained.tflite

python retrain.py \
  --bottleneck_dir=bottleneck \
  --how_many_training_steps=500000 \
  --model_dir=model \
  --output_graph=pola_retrained.pb \
  --output_labels=pola_retrained_labels.txt \
  --tfhub_module=https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2 \       --image_dir=Pola_ai \
  --validation_percentage=15

# test retrained model  
$ python label_image.py \
  --graph=pola_retrained.pb \
  --labels=pola_retrained_labels.txt \
  --image=ludwik.jpg
```

#### Convert model to tflite
```
toco \
  --graph_def_file=pola_retrained.pb \
  --input_format=TENSORFLOW_GRAPHDEF \
  --output_format=TFLITE \
  --output_file=pola_retrained.tflite \
  --inference_type=FLOAT \
  --input_type=FLOAT \
  --input_arrays=Placeholder \
  --output_arrays=final_result \
  --input_shapes=1,224,224,3

$ python lite_label_image.py \
  -m pola_retrained.tflite \
  -l pola_retrained_labels.txt \
  -i ludwik.jpg
```

#### Copy retrained model and labels to iOS and Android app
```
$ cd data
$ cp pola_retrained.tflite pola_retrained_labels.txt ../ios_camera/data
$ cp pola_retrained.tflite pola_retrained_labels.txt ../android_camera/app/src/main/assets
```
