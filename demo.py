from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.config.configuration import ConfigurationManager
from Insurance.component.data_transformation import DataTransformation
from Insurance.pipeline.pipline import Pipeline
from Insurance.constant import *
import os
def main():
    try:
        #config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(ConfigurationManager(config_filepath = CONFIG_FILE_PATH,
                                model_filepath = MODEL_FILE_PATH,
                                schema_filepath=SCHEMA_FILE_PATH,
                                    time_stamp=CURRENT_TIME_STAMP))
        #pipeline.run_pipeline()
        pipeline.start()
        logging.info("main function execution completed.")
        # # data_validation_config = Configuartion().get_data_transformation_config()
        # # print(data_validation_config)
        # schema_file_path=r"D:\Project\machine_learning_project\config\schema.yaml"
        # file_path=r"D:\Project\machine_learning_project\Insurance\artifact\data_ingestion\2022-06-27-19-13-17\ingested_data\train\Insurance.csv"

        # df= DataTransformation.load_data(file_path=file_path,schema_file_path=schema_file_path)
        # print(df.columns)
        # print(df.dtypes)

    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=="__main__":
    main()


