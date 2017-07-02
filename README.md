####Buid Docker image

`docker build -t pola-ai-image-cpu .`

####Run Docker container

`docker run --rm -it -v `pwd`:/app pola-ai-image-cpu bash`

####Build Pola images dataset

`rm Pola_dataset/.DS_Store Pola_dataset/*.tfrecord`

`python create_tfrecord.py --dataset_dir=Pola_dataset --validation_size=0.15 --tfrecord_filename=pola --num_shards=1`

####Train Xception network
`python python train_pola.py`
