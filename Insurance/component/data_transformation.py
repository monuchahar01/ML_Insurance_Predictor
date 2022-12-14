from cgi import test
#from types import NoneType
from sklearn import preprocessing
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.entity.config_entity import DataTransformationConfig 
from Insurance.entity.artifact_entity import DataIngestionArtifact,\
DataValidationArtifact,DataTransformationArtifact
import sys,os
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import pandas as pd
from Insurance.constant import *
from pathlib import Path
from Insurance.utils import read_yaml,save_object,save_numpy_array_data,load_data


#   longitude: float
#   latitude: float
#   Insurance_median_age: float
#   total_rooms: float
#   total_bedrooms: float
#   population: float
#   households: float
#   median_income: float
#   median_house_value: float
#   ocean_proximity: category
#   income_cat: float


class FeatureGenerator(BaseEstimator, TransformerMixin):

    def __init__(self,columns=None):
        """
        FeatureGenerator Initialization
        add_bedrooms_per_room: bool
        total_rooms_ix: int index number of total rooms columns
        population_ix: int index number of total population columns
        households_ix: int index number of  households columns
        total_bedrooms_ix: int index number of bedrooms columns
        """
        try:
            self.columns=columns
           
        except Exception as e:
            raise InsuranceException(e, sys) from e

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return self





class DataTransformation:

    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact
                 ):
        try:
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise InsuranceException(e,sys) from e

    

    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path

            dataset_schema = read_yaml(path_to_yaml=schema_file_path)

            numerical_columns = dataset_schema.numerical_columns
            categorical_columns = dataset_schema.categorical_columns


            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy="median")),
                
                ('scaler', StandardScaler())
            ]
            )

            cat_pipeline = Pipeline(steps=[
                 ('impute', SimpleImputer(strategy="most_frequent")),
                 ('one_hot_encoder', OneHotEncoder()),
                 ('scaler', StandardScaler(with_mean=False))
            ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")


            preprocessing = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_columns),
                ('cat_pipeline', cat_pipeline, categorical_columns),
            ])
            return preprocessing

        except Exception as e:
            raise InsuranceException(e,sys) from e   


    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info(f"Obtaining preprocessing object.")
            preprocessing_obj = self.get_data_transformer_object()


            logging.info(f"Obtaining training and test file path.")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            

            schema_file_path = self.data_validation_artifact.schema_file_path
            
            logging.info(f"Loading training and test data as pandas dataframe.")
            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            schema = read_yaml(path_to_yaml=schema_file_path)

            target_column_name = schema.target_column


            logging.info(f"Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            #input_feature_train_df.to_csv("Sample.csv", index=False)
            

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)


            train_arr = np.c_[ input_feature_train_arr, np.array(target_feature_train_df)]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_file_path = Path(os.path.join(self.data_transformation_config.root_dir,
                                                    self.data_transformation_config.transformed_dir,
                                                    transformed_train_dir, train_file_name))
            transformed_test_file_path = Path(os.path.join(self.data_transformation_config.root_dir,
                                                    self.data_transformation_config.transformed_dir,
                                                    transformed_test_dir, test_file_name))

            logging.info(f"Saving transformed training and testing array.")

            
            
            save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path, array=test_arr)

            preprocessing_obj_file_path = os.path.join(self.data_transformation_config.root_dir,
                                                        self.data_transformation_config.preprocessing_dir,
                                                        self.data_transformation_config.preprocessed_object_file_name)


           
            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
            message="Data transformation successfull.",
            transformed_train_file_path=Path(transformed_train_file_path),
            transformed_test_file_path=Path(transformed_test_file_path),
            preprocessed_object_file_path=Path(preprocessing_obj_file_path)

            )
            logging.info(f"Data transformationa artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise InsuranceException(e,sys) from e

# def __del__(self):
#logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")