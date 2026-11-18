-- Q4: Which video stayed on the Trending chart the longest?
-- Observed Trending Duration = last observed Trending date
-- minus first observed Trending date.
-- Because the compact dataset is sampled, this measures the
-- observed time span rather than continuous days on Trending.
-- We also count how many countries featured the video.

WITH video_history AS (
    SELECT
        video_id,
        title,
        MIN(
            TO_DATE(trending_date, 'YY.DD.MM')
        ) AS first_trending_date,
        MAX(
            TO_DATE(trending_date, 'YY.DD.MM')
        ) AS last_trending_date,
        COUNT(DISTINCT country) AS countries
    FROM videos
    GROUP BY video_id, title
)

SELECT
    video_id,
    title,
    first_trending_date,
    last_trending_date,
    last_trending_date - first_trending_date AS trending_duration_days,
    countries
FROM video_history
ORDER BY trending_duration_days DESC
LIMIT 20;