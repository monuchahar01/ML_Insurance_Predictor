from Insurance.entity.config_entity import DataIngestionConfig
import sys,os,shutil
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.entity.artifact_entity import DataIngestionArtifact
import tarfile
import numpy as np
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        
        self.raw_data_file=os.path.join(self.config.raw_dir,self.config.source_file)

    def get_insurance_data(self)  :
        try:
            source_file_path=os.path.join(self.config.source_data_path,self.config.source_file)

            os.makedirs(os.path.dirname(self.raw_data_file), exist_ok= True)
            shutil.copy(source_file_path,self.raw_data_file)
            

        except Exception as e:
            raise InsuranceException(e,sys) from e    
        

    def test_train_spilt(self) -> DataIngestionArtifact:
        try:
            df=pd.read_csv(self.raw_data_file)
            df["exp_cat"] = pd.cut(
                    df["expenses"],
                    bins=[0.0, 1500.0, 3000.0, 10000.0, 60000.0, np.inf],
                    labels=[1,2,3,4,5]
                )

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None    

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)  

            for train_index,test_index in split.split(df, df["exp_cat"]):
                strat_train_set = df.loc[train_index].drop(["exp_cat"],axis=1)
                strat_test_set = df.loc[test_index].drop(["exp_cat"],axis=1)  

            train_file_path = os.path.join(self.config.ingested_train_dir,
                                                self.config.source_file)

            test_file_path = os.path.join(self.config.ingested_test_dir,
                                            self.config.source_file)

            if strat_train_set is not None:
                    os.makedirs(self.config.ingested_train_dir,exist_ok=True)
                    logging.info(f"Exporting training datset to file: [{train_file_path}]")
                    strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                    os.makedirs(self.config.ingested_test_dir, exist_ok= True)
                    logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                    strat_test_set.to_csv(test_file_path,index=False) 

            data_injestion_artifact=DataIngestionArtifact(
                            train_file_path= Path(train_file_path),
                            test_file_path= Path(test_file_path),
                            is_ingested= True,
                            message=f"Data Injestion stage is completed."
                            
                )                                      
            logging.info(f"Data Ingestion artifact:[{data_injestion_artifact}]")

            return data_injestion_artifact

        except Exception as e:
            raise InsuranceException(e,sys) from e  

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            self.get_insurance_data()
            return self.test_train_spilt()
        except Exception as e:
            raise InsuranceException(e,sys) from e 

'''  def __del__(self):
    logging.info(f"{ '>>' *20} Data Ingestion log completed.{ '<<' *20} \n\n")  '''                
            