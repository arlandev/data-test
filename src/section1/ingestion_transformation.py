import json
import os
from pathlib import Path
import pandas as pd

class DataIngestion:

    """
    A class for ingesting TikTok video data from JSON files
    """

    def __init__(self, logger):
        
        """
        Initialize DataIngestion class with logger object
        """

        self.logger = logger
    
    
    def extract_data(self,json_obj):
        """
        Let's first create a method that helps us extract the necessary details from each dictionary from our JSON

        input: JSON Dictionary Object

        returns: Dictionary with extracted fields or None if required fields are missing

        """
        try:

            required_fields = ["video_id", "author_id", "upload_date"]
            if not all(field in json_obj for field in required_fields):
                self.logger.warning(f"Missing required fields.")
                return None
                # we deem the 3 headers as absolutely necessary
                # if not all are present, json object is invalid: return an empty object

            return {
                "video_id": json_obj.get("video_id"),
                "author_id": json_obj.get("author_id"),
                "upload_date": json_obj.get("upload_date"),
                "description": json_obj.get("description", "N/A"),
                "hashtags": json_obj.get("hashtags", []),
                "view_count": json_obj.get("view_count", 0),
                "like_count": json_obj.get("like_count", 0),
                "comment_count": json_obj.get("comment_count", 0),
                "video_url": json_obj.get("video_url", ""),
                "raw_data": json_obj.get("raw_data", {})

                # only video id, author id, and upload dates dont have default values
                # because they are absolutely necessary
            }
            
        except Exception as e:
            self.logger.error(f"Something bad happened: {e}")
            return None

    # reads a json file and returns a list of parsed objects
    def read_json_file(self, filename: str):
        """
        Leveraging the extractor method, let's build a list of extracted information from our JSON file

        input: File name

        returns: List of dictionary objects of extracted fields

        """
        json_data = []

        # combine the relative path with the file name
        parent_dir = Path(__file__).resolve().parent.parent.parent
        json_file_name = os.path.join(parent_dir,filename)
        
        try:
            if os.path.exists(json_file_name): # additional checking of json file path
                print(f"JSON Data File exists. Proceeding with extraction.")
                
                with open(json_file_name, 'r') as file:
                    data = json.load(file)
                    
                    # check if file contains multiple entries
                    if isinstance(data, list): 
                        for item in data:
                            json_data.append(self.extract_data(item))

                    # only 1 data entry in the json data file
                    else:
                        json_data.append(self.extract_data(data))

                self.logger.info(f"Completed reading JSON data file.")
                return json_data
            else:
                raise FileNotFoundError

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")
            self.logger.error(f"Error parsing JSON data: {e}")
            return json_data # return the json_data object as there may have been valid data parsed
        
        except FileNotFoundError:
            print("JSON Data File not found. Returning an empty list.")
            self.logger.error("JSON Data File not found. Returning an empty list.")
            return [] # return an empty list since file was not found

        except Exception as e:
            print(f"Something bad happened: {e}")
            self.logger.error(f"Something bad happened: {e}")
            return json_data

class DataTransformation:


    """
    Class for data transformation methods for TikTok video metadata
    """

    def __init__(self, logger):

        """
        Initialize DataTransformation class with logger object
        """

        self.logger = logger

    def transform_json_data(self, json_data_list):

        """
        A method that converts our list of dictionaries into a pandas DataFrame which we'll transform further

        input: List of dictionaries

        returns: Formatted Pandas DataFrame
        """

        try:
            # convert the list of dictionaries into a pandas dataframe
            json_data_df = pd.DataFrame(json_data_list)

            # convert the upload_date to a consistent datetime format
            json_data_df["upload_date"] = pd.to_datetime(json_data_df["upload_date"])

            # default the new column value to "others"
            json_data_df["video_category"] = "other" 

            # convert video category respectively
            for index, row in json_data_df.iterrows():

                # create a string that combines all the hashtags
                hashtag_content = ":".join(row["hashtags"]).lower()

                # check for relevant hashtag in hashtags list
                if "dogs" in hashtag_content or "pets" in hashtag_content or "animals" in hashtag_content or "pets" in hashtag_content:
                    json_data_df.at[index, "video_category"] = "animals" # convert video category

            return json_data_df
        
        except Exception as e:
            print(f"Something bad happened: {e}")
            self.logger.error(f"Something bad happened: {e}")