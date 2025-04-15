from sqlalchemy import create_engine
import json

class DataLoading():

    """
    Class for loading transformed TikTok data into a Neon PostgreSQL Database
    """

    def __init__(self, logger, database_url):

        """
        Initialize the DataLoading class with a logger
        """
        
        self.logger = logger
        self.database_url = database_url

    def load_dataframe_to_postgres(self, df, table_name='tiktok_videos'):
        """
        Load a DataFrame directly to an existing PostgreSQL table
        
        inputs:
            df: Pandas DataFrame with transformed data
            table_name: Name of the target table
            
        returns: Number of records loaded
            
        """
        
        try:

            # Create a copy of the DataFrame to avoid modifying the original
            df_copy = df.copy()

            # Get database connection string from environment
            db_url = self.database_url
            if not db_url:
                raise ValueError("DATABASE_URL environment variable not set")
            
            # Create SQLAlchemy engine
            engine = create_engine(db_url)
            
            # Convert Python dictionaries to JSON Strings for PostgreSQL
            if 'raw_data' in df_copy.columns:
                self.logger.info("Converting raw_data dictionaries to JSON strings")
                df_copy['raw_data'] = df_copy['raw_data'].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)

            # Convert hashtags from list to PostgreSQL array format
            # We need a string representation for sending to Postgres
            # https://www.postgresql.org/docs/current/arrays.html
            if 'hashtags' in df.columns:
                df_copy['hashtags'] = df_copy['hashtags'].apply(
                    lambda tags: '{' + ','.join(f'"{tag}"' for tag in tags) + '}'
                )
            
            # Load DataFrame to PostgreSQL table
            self.logger.info(f"Loading {len(df_copy)} rows to table {table_name}")
            df_copy.to_sql(
                name=table_name,
                con=engine,
                # if_exists='replace', # let's use replace so every run the data is replaced -- ideally, use append
                if_exists='append',  # adds onto the existing table's data
                index=False, # remove indices from the dataframe
                method='multi',  # faster for larger datasets
                chunksize=1000  # process in chunks to avoid memory issues
            )
            
            self.logger.info(f"Successfully loaded {len(df_copy)} records to table {table_name}")
            return len(df_copy)
        
        except Exception as e:
            self.logger.error(f"Database loading error: {e}")
            raise