Based on [https://medium.com/towards-data-science/using-docker-to-set-up-a-deep-learning-environment-on-aws-6af37a78c551]

#### Setup EC2 Ubuntu GPU

```
g2.2xlarge
us-east-1a
30 GB SSD
ssh
```

### Download SSH pem key and ssh to host

```
$ cp key.pem ~/ssh/key.pem
$ chmod 400 ~/ssh/key.pem
$ ssh-add ~/ssh/key.pem
 
$ ssh ubuntu@YOUR_HOST
```

#### Install NVIDIA Drivers
``` 
$ sudo add-apt-repository ppa:graphics-drivers/ppa -y
$ sudo apt-get update
$ sudo apt-get install -y nvidia-375 nvidia-settings nvidia-modprobe
```

#### Install Docker

```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# Verify that the key fingerprint is 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88
$ sudo apt-key fingerprint 0EBFCD88
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
$ sudo apt-get update
$ sudo apt-get install -y docker-ce
```

#### Install NVIDIA Docker
```
$ wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
$ sudo dpkg -i /tmp/nvidia-docker_1.0.1-1_amd64.deb && rm /tmp/nvidia-docker_1.0.1-1_amd64.deb
```

#### Verify installation
```
$ sudo nvidia-docker run --rm nvidia/cuda nvidia-smi
```

### Luanch TensorFlow GPU
```
? sudo nvidia-docker run --rm -v `pwd`:/app -it tensorflow/tensorflow:latest-gpu bash
```