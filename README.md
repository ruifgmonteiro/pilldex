# Pilldex

**Pilldex:** A pill recognition REST API using Convolutional Neural Networks.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

- Clone this repo 
- Install requirements
- Train the model
- Run the script
- Check http://localhost:5000

### Prerequisites

- OpenCV
- Keras
- Python 3.6
- Sqlite3
- CUDA
- Flask

## Local Installation

### Clone the repo
```shell
$ git clone https://github.com/ruifgmonteiro/pilldex.git
```

### Install requirements

```shell
$ pip install -r requirements.txt
```

Make sure you have the following installed:
- tensorflow
- keras
- flask
- pillow
- h5py
- gevent
- sqlite3

### Run with Python

Python 2.7 or 3.5+ are supported and tested.

#### Train the network.

```shell
$ python train.py --dataset dataset --model pilldex.model --labelbin lb.pickle
```

#### Check training progress in Tensorboard.

```shell
$ tensorboard --logdir=logs/ --port=8101
```

#### Run the webapp.

```shell
$ python app.py
```

## Deployment

Soon: Deploying webapp in Heroku.

## Built With

* [OpenCV](https://github.com/opencv/opencv) - Computer Vision Library
* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework used
* [Keras](https://keras.io/) - Python high level deep learning library
* [Tensorflow](https://www.tensorflow.org/) - An open source machine learning library for research and production.
* [Sqlite3](https://www.sqlite.org/docs.html) - Database engine

## Authors

* **Rui Monteiro** - *Initial work* - [rfgm6](https://github.com/rfgm6)

See also the list of [contributors](https://github.com/pilldex/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Adrian Rosebrock from PyImageSearch

## More resources

[Building a simple Keras + deep learning REST API](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)
[Deploy Keras Model with Flask as Web App in 10 Minutes] (https://github.com/mtobeiyf/keras-flask-deploy-webapp)

