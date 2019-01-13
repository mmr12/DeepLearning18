import tensorflow as tf
import os
import sys

# To import from sibling directory ../utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from data_loader.faster_rcnn_loader import DataGenerator
from models.faster_rcnn_model import FasterRcnnModel
from trainers.faster_rcnn_trainer import FasterRcnnTrainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.logger import Logger
from utils.utils import get_args


def main():
    config = process_config("configs/faster_rcnn.json")
    print("we're in business")
    # create the experiments dirs
    create_dirs([config.summary_dir, config.checkpoint_dir])
    # create tensorflow session
    sess = tf.Session()
    # create your data generator
    print('Starting Data Gen')
    data = DataGenerator(config)
    # create an instance of the model you want
    model = FasterRcnnModel(config)
    # create tensorboard logger
    logger = Logger(sess, config)
    # create trainer and pass all the previous components to it
    trainer = FasterRcnnTrainer(sess, model, data, config, logger)
    #load model if exists
    model.load(sess)
    # print("Model exists already, if you want to retrain it delete it first!")
    #here you train your model
    if config.debug == 0:
        trainer.train()

    #TESTING
    #load model if exists
    #model.load(sess)



if __name__ == '__main__':
    main()
