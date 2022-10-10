from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_data_path: Path
    source_file: str
    raw_dir: str
    ingested_train_dir: Path
    ingested_test_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    schema_file_path: Path
    report_file_path: Path
    report_page_file_path: Path

@dataclass(frozen=True)
class  DataTransformationConfig:
    root_dir: Path
    transformed_dir: Path
    transformed_train_dir: str
    transformed_test_dir: str
    preprocessing_dir: str
    preprocessed_object_file_name: str

@dataclass(frozen=True)
class ModelTrainerConfig:
    trained_model_file_path: Path
    base_accuracy: int
    model_config_file_path: Path

@dataclass(frozen=True)
class ModelEvaluationConfig:
    model_evaluation_file_path: Path
    time_stamp: str
    
@dataclass(frozen=True)
class ModelPusherConfig:
    export_dir_path: Path


@dataclass(frozen=True)
class TrainingPipelineConfig:
    artifact_dir: Path







      

