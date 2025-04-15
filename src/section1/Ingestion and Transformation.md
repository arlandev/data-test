# Section 1: Ingestion and Transformation

## Data Ingestion

### Situation

The task required me to create the Extraction part of the ETL process featuring JSON Data for each TikTok video. The extraction needed to be complete with relevant fields while also handling errors with grace.

### My own understanding and approach

In the ETL projects that I have done, the extraction process is always the most critical and most carefully traversed step. It requires meticulous planning and great understanding of what type of data you're trying to extract. In the scenario given in the data assessment, the type of data is already provided but in real-life production applications, this can't be farther from the truth. I managed to narrow down the necessary steps to the following:

- Read the data from a JSON file with the assumption that we can download data from a source.
- Let's assume that there are a LOT of noise in the data, hence we only need to extract the necessary fields for analyses (provided already by the Section).
- Only consider data from our source object that has the COMPLETE fields that we require.

### Code Implementation

I implemented ingestion using the `DataIngestion` class for a cleaner, modular approach with two methods:

1. `extract_data()` - The "extractor" method which checks each dictionary for complete fields and only returns an extracted version if all fields are present and valid.
2. `read_json_file()` - The "builder" method which leverages the "extractor" method for each dictionary inside the file. It reads a JSON file and processess all records inside.

### Why this approach?

1. Class-based Design: Helps with organizing our codebase and leverages concepts of OOP for cleaner, simpler code.
2. Validation: Assures data integrity from the start by checking if required fields are complete per object.
3. Default Values: None-required fields have default values to prevent unnecessary process stoppages when met with null values.
4. Detailed Logging: Helps with debugging and monitoring the pipeline.

### Improvements

1. Supporting additional formatting, but that depends on the data source.
2. When deployed in production, cloud-saving logic can be added to implement a disaster-recovery plan for the data.

## Data Transformation

### Situation

The task required enhancing the script to perform specific transformations on the ingested data:

- Convert upload_date to a consistent datetime format
- Create a new field called video_category based on hashtags
- Store the transformed data in a structured format for database loading

### My own understanding and approach

The transformation step of the ETL process helps make sense of the raw data we just extracted. It's what gives raw data value and prepares the data for analysis and reporting. This is highlighted in the creation of another column, which helps us make sense of the nature of a video. Depending on the business context, logic, and usage, other transformations will also happen.

### Code Implementation

I implemented the `DataTransformation` class with the main method `transform_json_data()` that:

1. Converts the list of dictionaries to a dataframe
2. Transforms the upload_date to a consistent format
3. Creates and populates the video_category field based on hashtag content

### Why This Approach

I chose this implementation for several reasons:

1. Pandas DataFrame: A lot of available methods for manipulating content and also is a step towards database loading
2. Row-by-row processing: Helps maintain data integrity by carefully processing each row
