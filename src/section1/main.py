import logging
import os

from dotenv import load_dotenv

from ingestion_transformation import DataIngestion, DataTransformation
from loading import DataLoading

load_dotenv()

# set up a simple logger for the entire pipeline
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tiktok_pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('tiktok_data_ingestion')

def generate_sample_data():
    """
    As fall back, generate sample data when json file is not found
    """

    logger.info("Generating sample TikTok data for testing")
    return [
        {
            "video_id": "abc123xyz",
            "author_id": "user456",
            "upload_date": "2024-07-26T10:00:00Z",
            "description": "Funny cat video!",
            "hashtags": ["#cats", "#funny", "#tiktok"],
            "view_count": 150000,
            "like_count": 10000,
            "comment_count": 500,
            "video_url": "https://www.tiktok.com/@user456/video/abc123xyz",
            "raw_data": {
                "some_key": "some_value"
            }
        },
        {
            "video_id": "def456uvw",
            "author_id": "user789",
            "upload_date": "2024-07-25T15:30:00Z",
            "description": "Dog tricks compilation",
            "hashtags": ["#dogs", "#animals", "#tricks"],
            "view_count": 250000,
            "like_count": 20000,
            "comment_count": 1200,
            "video_url": "https://www.tiktok.com/@user789/video/def456uvw",
            "raw_data": {
                "breed": "Golden Retriever",
                "location": "Austin, TX"
            }
        },
        {
            "video_id": "ghi789rst",
            "author_id": "user123",
            "upload_date": "2024-07-24T08:45:00Z",
            "description": "Morning routine 2024",
            "hashtags": ["#routine", "#morning", "#2024"],
            "view_count": 75000,
            "like_count": 5000,
            "comment_count": 300,
            "video_url": "https://www.tiktok.com/@user123/video/ghi789rst",
            "raw_data": {
                "extra_key": "extra_value"
            }
        }
    ]

def main():
    
    """
    Demonstration of Data Ingestion & Transformation
    """

    # initiate variables from environment variables
    json_path = os.getenv("JSON_DATA")
    print(json_path)
    database_url = os.getenv("DATABASE_URL")

    # create DataIngestion and DataTransformation objects
    data_ingestion = DataIngestion(logger)
    data_transformation = DataTransformation(logger)
    data_loading = DataLoading(logger, database_url)

    # initialize variable
    extracted_data = None

    if json_path:
        try:
            extracted_data = data_ingestion.read_json_file(json_path)
            if extracted_data and len(extracted_data) > 0:
                logger.info(f"Extracted {len(extracted_data)} records from {json_path}")
            else:
                logger.warning(f"No valid data extracted from {json_path}")
                extracted_data = None
        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            extracted_data = None

    # use sample data if no data was extracted
    if not extracted_data:
        logger.info("Using sample data instead")
        extracted_data = generate_sample_data()
        
    if extracted_data:
        try:
            formatted_tiktokdata_df = data_transformation.transform_json_data(extracted_data)
            
            if formatted_tiktokdata_df is not None:
                len_upload = data_loading.load_dataframe_to_postgres(
                    formatted_tiktokdata_df, 
                    table_name="tiktok_videos"
                )
                if len_upload:
                    logger.info(f"Upload successful. Added {len_upload} rows.")
                else:
                    logger.error(f"No rows added.")
            else:
                logger.error("Transformation returned None")
        except Exception as e:
            logger.error(f"Error in transformation or loading: {e}")
    else:
        logger.error("No data available for processing")

if __name__ == "__main__":
    main()