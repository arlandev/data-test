# Query 1: Find the top 10 most viewed videos in the "animals" category uploaded in the last month.

```
SELECT
  video_id,
  upload_date,
  description,
  view_count,
  like_count,
  comment_count
FROM tiktok_videos
WHERE
  video_category = 'animals'
  AND upload_date >= date_trunc('month', current_date - interval '1 month')
  AND upload_date < date_trunc('month', current_date)
ORDER BY view_count DESC
LIMIT 10;
```

## Approach

Selected Columns: To practice efficiency, only select the columns that you actually need. The selected columns are what I assume are needed so that this data is viable for Machine Learning input data or AI learning.

# Query 2: Calculate the average like count for videos in each category.

```
SELECT
  video_category,
  AVG(like_count) AS average_likes
FROM
  tiktok_videos
WHERE
  like_count IS NOT NULL
GROUP BY
  video_category
ORDER BY
  average_likes DESC;
```

## Approach

Data Cleaning: Using `WHERE like_count IS NOT NULL` ensures that only the videos with recorded like counts are included in the calculation to prevent NULL values from skewing the averages. While a recorded 0 `like_count` value can affect the averaging, it is a realistic scenario so it should be included for analysis.

# Query 3: Find the author with the most videos uploaded.

```
SELECT
  author_id,
  COUNT(video_id) AS video_count
FROM
  tiktok_videos
GROUP BY
  author_id
ORDER BY
  video_count DESC
LIMIT 1;
```

## Approach

`LIMIT 1`: This clause focuses on making the query efficient as it only selects the first result from a window of results.
Tie-Breaking: In case of ties, this query will only return one result. A case of improvement would be to add logic to break ties between authors with the same number of videos uploaded.
Analytics: Adding their averages (like count, view count, etc.) can help improve the analytics of this query.
