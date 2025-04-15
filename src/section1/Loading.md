# Section 1: Loading

# Loading Demonstration!

https://www.loom.com/share/ea9bbc34cd324ee083eb0807858abbf1?sid=daa76ed2-c060-4089-8eea-92687fd19ce9

## Situation

The task required creating logic to load the transformed TikTok video data into an existing table. Although the task only calls for the demonstration of how the data would be loaded, I went ahead and created a Neon database for real implementation of the loading.

## My Understanding

Data loading is the final critical step that bridges transformed data to the database system. The logic should be carefully created to avoid compatibility issues and ensure that loading is done properly:

1. Connect to the PGSQL Neon database using SQLAlchemy as the bridger of code and database
2. Handle data type conversions for special fields (like lists to arrays and dictionaries to JSON)
3. Handle potential database errors gracefully

## Why This Approach

I chose this implementation for several reasons:

1. SQLAlchemy: Bridges code and PGSQL databases for efficiency
2. `DataFrame.to_sql()`: Simplifies the loading process
3. Data type conversions: Explicitly handles the complex types (dictionaries and lists) that PostgreSQL doesn't really appreciate (no support)
4. Batch Processing: Process data in chunks in the assumption that the data set grows larger and larger

## Challenges

1. Data type conversions: PGSQL doesn't like Python dictionaries so they needed to converted to fit.

## Improvements

1. Retry Logic: When loading fails, implement a retry system to make sure data is loaded eventually
2. Data Validation Logic: Maybe data loading is failing for a reason, so maybe adding a checker for the validity of the data can be a good addition. But extraction already has validity checking, so this improvement may be redundant.
