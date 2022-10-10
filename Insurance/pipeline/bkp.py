from collections import namedtuple
from datetime import datetime
import uuid
from Insurance.config.configuration import ConfigurationManager
from Insurance.logger import logging, get_log_file_name
from Insurance.exception import InsuranceException
from threading import Thread
from typing import List

from multiprocessing import Process
from Insurance.entity.artifact_entity import ModelPusherArtifact, DataIngestionArtifact, ModelEvaluationArtifact
from Insurance.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
from Insurance.entity.config_entity import DataIngestionConfig, ModelEvaluationConfig

from Insurance.component.data_validation import DataValidation
from Insurance.component.data_transformation import DataTransformation
from Insurance.component.model_trainer import ModelTrainer
from Insurance.component.model_evaluation import ModelEvaluation
from Insurance.component.model_pusher import ModelPusher
from Insurance.component.data_injestion import DataIngestion
import os, sys
from collections import namedtuple
from datetime import datetime
import pandas as pd
from Insurance.constant import *

try:


    config=ConfigurationManager(config_filepath = CONFIG_FILE_PATH,
                                model_filepath = MODEL_FILE_PATH,
                                schema_filepath=SCHEMA_FILE_PATH,
                                    time_stamp=CURRENT_TIME_STAMP)
     #Data Ingestion stage                              
    data_ingestion = DataIngestion(config=config.get_data_ingestion_config())
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    # Data validation stage
    data_validation = DataValidation(data_validation_config=config.get_data_validation_config(),
                                             data_ingestion_artifact=data_ingestion_artifact)
    data_validation_artifact=data_validation.initiate_data_validation() 

    #Data Transformation Stage
    data_transformation = DataTransformation(
                data_transformation_config=config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact)
    data_transformation_artifact=data_transformation.initiate_data_transformation()

    #Model Trainer
    model_trainer = ModelTrainer(model_trainer_config=config.get_model_trainer_config(),
                                         data_transformation_artifact=data_transformation_artifact)
    model_trainer_artifact=model_trainer.initiate_model_trainer() 

    #Model Evaluation
    model_eval = ModelEvaluation(
                model_evaluation_config=config.get_model_evaluation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact)
    model_evaluation_artifact = model_eval.initiate_model_evaluation() 

    #Model Pusher
    model_pusher = ModelPusher(
                model_pusher_config=config.get_model_pusher_config(),
                model_evaluation_artifact=model_evaluation_artifact)  
    model_pusher_artifact=model_pusher.initiate_model_pusher()                                                 



except Exception as e:

    raise InsuranceException(e,sys) from e






