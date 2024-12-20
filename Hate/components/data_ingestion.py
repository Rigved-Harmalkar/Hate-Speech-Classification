import os
import sys
from zipfile import ZipFile
from Hate.logger import logging
from Hate.exception import CustomException
from Hate.configuration.gcloud_syncer import GCloudSync
from Hate.entity.config_entity import (DataIngestionConfig)
from Hate.entity.artifact_entity import (DataIngestionArtifacts)


# Class to ingest data from the GCP
class DataIngestion:
    def __init__(self, data_ingestion_config : DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.gcloud = GCloudSync()
     
    # Getter Function    
    def get_data_from_gcloud(self) -> None:
        try:
            logging.info("Entered the get_data_from_gcloud method of Data ingestion class")
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)

            self.gcloud.sync_folder_from_gcloud(self.data_ingestion_config.BUCKET_NAME,
                                                self.data_ingestion_config.ZIP_FILE_NAME,
                                                self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR,
                                                )
            
            logging.info("Exited the get_data_from_gcloud method of Data ingestion class")
        
        except Exception as e:
            raise CustomException(e, sys) from e
        
    # Since the data is in a zip file, a function for unzipping the zip file.
    def unzip_and_clean(self):
        logging.info("Entered the unzip_and_clean method of Data ingestion class")
        
        try:
            # Log the current zip file path being used
            logging.info(f"Using ZIP file path: {self.data_ingestion_config.ZIP_FILE_PATH}")
            print(f"Using ZIP file path: {self.data_ingestion_config.ZIP_FILE_PATH}")  # You can print this for immediate debugging
            
            # Check if the ZIP_FILE_PATH exists
            if not os.path.exists(self.data_ingestion_config.ZIP_FILE_PATH):
                raise FileNotFoundError(f"Zip file not found at {self.data_ingestion_config.ZIP_FILE_PATH}")
            
            # Ensure the extraction directory exists
            if not os.path.exists(self.data_ingestion_config.ZIP_FILE_DIR):
                os.makedirs(self.data_ingestion_config.ZIP_FILE_DIR, exist_ok=True)
            
            # Unzip the file
            with ZipFile(self.data_ingestion_config.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.data_ingestion_config.ZIP_FILE_DIR)
            
            logging.info("Exited the unzip_and_clean method of Data ingestion class")
            print("working")
            
            return self.data_ingestion_config.DATA_ARTIFACTS_DIR, self.data_ingestion_config.NEW_DATA_ARTIFACTS_DIR
        
        except FileNotFoundError as fnf_error:
            logging.error(f"File not found error: {str(fnf_error)}")
            raise CustomException(fnf_error, sys) from fnf_error
        
        except Exception as e:
            logging.error(f"Error occurred during unzip and clean: {str(e)}")
            print("Not working")
            raise CustomException(e, sys) from e
        
    # Start the data ingestion function
    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the initiate_data_ingestion method of Data ingestion class")

        try:
            self.get_data_from_gcloud()
            logging.info("Fetched the data from gcloud bucket")
            imbalance_data_file_path, raw_data_file_path = self.unzip_and_clean()
            logging.info("Unzipped file and split into train and valid")

            data_ingestion_artifacts = DataIngestionArtifacts(
                imbalance_data_file_path= imbalance_data_file_path,
                raw_data_file_path = raw_data_file_path
            )

            logging.info("Exited the initiate_data_ingestion method of Data ingestion class")

            logging.info(f"Data ingestion artifact: {data_ingestion_artifacts}")

            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e