-- Q1: Which country has the most unique Trending chart?
-- Unique = video appears in only one country.

SELECT
    country,
    COUNT(DISTINCT video_id) AS total_videos,
    COUNT(DISTINCT CASE
        WHEN video_id IN (
            SELECT video_id
            FROM videos
            GROUP BY video_id
            HAVING COUNT(DISTINCT country) = 1
        )
        THEN video_id
    END) AS unique_videos,
    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN video_id IN (
                SELECT video_id
                FROM videos
                GROUP BY video_id
                HAVING COUNT(DISTINCT country) = 1
            )
            THEN video_id
        END) / COUNT(DISTINCT video_id),
        2
    ) AS unique_share_percent
FROM videos
GROUP BY country
ORDER BY unique_share_percent DESC;