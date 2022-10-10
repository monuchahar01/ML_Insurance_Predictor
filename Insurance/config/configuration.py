from Insurance.constant import *
from Insurance.utils import read_yaml, create_directories
from Insurance.entity.config_entity import *
import os, sys
from Insurance.exception import InsuranceException
from Insurance.logger import logging


class ConfigurationManager:
    def __init__(
        self, 
        config_filepath = CONFIG_FILE_PATH,
        model_filepath = MODEL_FILE_PATH,
        schema_filepath=SCHEMA_FILE_PATH,
        time_stamp=CURRENT_TIME_STAMP):
        self.config = read_yaml(config_filepath)
        self.model = read_yaml(model_filepath)
        self.schema=read_yaml(schema_filepath)
        self.time_stamp=time_stamp

        create_directories([self.config.training_pipeline_config.artifact_dir])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        data_ingestion_artifact_dir=os.path.join(config.root_dir,self.time_stamp)

        create_directories([data_ingestion_artifact_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=data_ingestion_artifact_dir,
            source_data_path=config.source_data_path,
            source_file= config.source_file,
            raw_dir=os.path.join(data_ingestion_artifact_dir,config.raw_dir),
            ingested_train_dir=os.path.join(data_ingestion_artifact_dir,config.ingested_train_dir),
            ingested_test_dir=os.path.join(data_ingestion_artifact_dir,config.ingested_test_dir)
        )

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:

        try:
            config = self.config.data_validation
            data_validation_artifact_dir=os.path.join(
                config.root_dir,
                self.time_stamp)

            create_directories([data_validation_artifact_dir])    

            data_validation_config = DataValidationConfig(
                schema_file_path=self.schema,
                report_file_path=os.path.join(data_validation_artifact_dir,config.report_file_name),
                report_page_file_path=os.path.join(data_validation_artifact_dir,config.report_page_file_name)
            )
            return data_validation_config

        except Exception as e:
            raise InsuranceException(e,sys) from e   


    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            config = self.config.data_transformation_config

            data_transformation_artifact_dir=os.path.join(
                config.root_dir,
                self.time_stamp
            )
            create_directories([data_transformation_artifact_dir])

            data_transformation_config=DataTransformationConfig(
                    root_dir=data_transformation_artifact_dir,
                    transformed_dir=config.transformed_dir,
                    transformed_train_dir=config.transformed_train_dir,
                    transformed_test_dir=config.transformed_test_dir,
                    preprocessing_dir=config.preprocessing_dir,
                    preprocessed_object_file_name=config.preprocessed_object_file_name
            )

            logging.info(f"Data transformation config: {data_transformation_config}")

            return data_transformation_config
            
        except Exception as e:
            raise InsuranceException(e,sys) from e  


    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            config = self.config.model_trainer_config

            model_trainer_artifact_dir=os.path.join(
                config.root_dir,
                self.time_stamp)
            create_directories([model_trainer_artifact_dir])    
           

            model_trainer_config = ModelTrainerConfig(
                trained_model_file_path=Path(os.path.join(model_trainer_artifact_dir,config.trained_model_dir,
                                                config.model_file_name)),
                base_accuracy= config.base_accuracy,
                model_config_file_path=MODEL_FILE_PATH
            )

            logging.info(f"Model trainer config: {model_trainer_config}")
            
            return model_trainer_config
        
        except Exception as e:
            raise InsuranceException(e,sys) from e   



    def get_model_evaluation_config(self) ->ModelEvaluationConfig:
        try:
            config = self.config.model_evaluation_config

            model_evaluation_artifact_dir=config.root_dir

            create_directories([model_evaluation_artifact_dir]) 
            

            model_evaluation_file_path = os.path.join(model_evaluation_artifact_dir,
                                                    config.model_evaluation_file_name)
            response = ModelEvaluationConfig(model_evaluation_file_path=model_evaluation_file_path,
                                            time_stamp=self.time_stamp)
            
            
            logging.info(f"Model Evaluation Config: {response}.")

            return response

        except Exception as e:
            raise InsuranceException(e,sys) from e


    def get_model_pusher_config(self) -> ModelPusherConfig:
        try:
            time_stamp = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
            model_pusher_config_info = self.config.model_pusher_config
            export_dir_path = os.path.join(ROOT_DIR, model_pusher_config_info.model_export_dir,
                                           time_stamp)

            model_pusher_config = ModelPusherConfig(export_dir_path=export_dir_path)
            logging.info(f"Model pusher config {model_pusher_config}")
            return model_pusher_config

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_training_pipeline_config(self) ->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config.training_pipeline_config
            training_pipeline_artifact_dir = os.path.join(ROOT_DIR,
            
            training_pipeline_config.artifact_dir
            )

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=training_pipeline_artifact_dir)
            logging.info(f"Training pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise InsuranceException(e,sys) from e 