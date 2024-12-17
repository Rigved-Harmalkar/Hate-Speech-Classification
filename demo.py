from Hate.logger import logging
from Hate.exception import CustomException
import sys
from Hate.configuration.gcloud_syncer import GCloudSync


obj = GCloudSync()
obj.sync_folder_from_gcloud("hate_speech_rig","dataset.zip","dataset.zip")
