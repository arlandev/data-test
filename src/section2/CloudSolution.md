# Cloud Storage Solution for TikTok Data in AWS

When thinking about the question of how to store TikTok video data in AWS, it's important to factor in balance rather than looking for a single "perfect" solution. Some solutions may be the most cost-efficient but lack speed in terms of retrieval.

## Understanding data storage

Let's consider that data that we are working with:

1. Raw JSON Data from TikTok videos (considered as unstructured)
2. Transformed and structured data after processing
3. Possible scenarios where data needs to be queried

According to an AWS guide to structured data (https://aws.amazon.com/what-is/structured-data/), data format can impact how data is stored and processed. Our TikTok data starts as semi-structured JSON but becomes more structured after transformation.

## Raw Data Storage: S3

S3 is the obvious starting point because of its virtually unlimited scalability and low cost. Its scalability is very much highlighted in this article: https://aws.amazon.com/solutions/case-studies/salesforce-amazons3-intelligent-tiering-case-study

When storing data, a possible optimization is using different file formats. Part of my practical experience is working with parquet files instead of CSV files since parquet files are generally more space-efficient than CSV or Excel files. It we consider this point in storing data, we can consider converting JSON data to formats like Apache Parquet to reduce storage costs (https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html).

According to many sources as well as famous discussion forums like the r/aws subreddit, a famous approach is:

1. Use S3 as the initial loading location for raw data
2. Use AWS Glue for file conversion (https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/three-aws-glue-etl-job-types-for-converting-data-to-apache-parquet.html)
3. Partition the data by date for efficient querying

## Transformation

AWS offers a lot of different tools for transforming, and the right choice depends on your specific needs. Despite this, there's never really a "best" choice since everything has its own pros and cons.

Let's take into consideration AWS Glue (https://docs.aws.amazon.com/glue/latest/dg/edit-jobs-transforms.html). Glue can do transformation methods like `Filter`, `Join`, and `Map` that can handle data manipulation without much coding. For TikTok data, this means we can efficiently transform JSON streams into analytical formats, categorize videos based on hashtags, and normalize timestamps—all crucial steps we already implemented in our Python pipeline.

Another huge advantage is Glue's crawlers. They can help detect schemas and can detect changes in them. This means, whenever TikTok's API changes the structure of data anytime, the changes are tracked properly and within reasonable time.

## Querying Data

When deciding how to query our TikTok data, we need to match the tool to how we'll use the data:

`Amazon Athena` works well for occasional analysis directly on our Parquet files in S3. It's pay-per-query and doesn't require server setup.
`Amazon Redshift` makes sense if we need to run complex queries regularly. It's more powerful but requires more management.

## Smart Storage Management

A practical approach to managing costs would be:

1. Keep recent data (3 months) in standard S3
2. Move older data to cheaper S3 Infrequent Access
3. Archive historical data to Glacier for long-term storage

## Simple Architecture

My proposed solution is straightforward:

1. Store raw TikTok JSON in S3
2. Transform to Parquet using AWS Glue
3. Query with Athena or Redshift based on needs
4. Use lifecycle policies to manage storage costs
