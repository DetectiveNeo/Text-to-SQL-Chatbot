import os 
from pathlib import Path
from dotenv import load_dotenv
# import yaml

load_dotenv()

class Config():
    """
    Class contains all the configuration of the project.
        1) data
        2) environment variables
        3) model configurations
    """

    PROJECT_ROOT = Path(__file__).resolve().parents[1] # Go up two folders to the project root folder

    PROJECT_ROOT.with_stem

    def __init__(self):
        
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.raw_data_path = self.PROJECT_ROOT / "data/raw"
        self.database_path = self.PROJECT_ROOT / "data/database/my_database.db"
        self.schema_path = self.PROJECT_ROOT / "data/schema/base_schema.json"
        self.vectore_store_path = self.PROJECT_ROOT / "data/vector_store/schema"


if __name__ == "__main__":
    
    cfg = Config()
    print(cfg.api_key)
    print(cfg.PROJECT_ROOT)
    print(cfg.raw_data_path)
    print(cfg.vectore_store_path)

