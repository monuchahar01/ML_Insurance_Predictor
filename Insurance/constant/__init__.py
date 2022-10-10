from pathlib import Path
from datetime import datetime
import os

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

ROOT_DIR = os.getcwd()  #to get current working directory
CONFIG_FILE_PATH = Path("configs/config.yaml")
MODEL_FILE_PATH = Path("configs/model.yaml")
SCHEMA_FILE_PATH = Path("configs/schema.yaml")

CURRENT_TIME_STAMP = get_current_time_stamp()

BEST_MODEL_KEY = "best_model"
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"

EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"
