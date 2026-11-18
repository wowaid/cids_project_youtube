-- Q3: What is the most dramatic trending video?
-- DramaScore = comments per 1,000 views.
-- Only videos with at least 100,000 views are included.
-- Each video appears only once, using its highest observed DramaScore.

WITH video_scores AS (
    SELECT
        video_id,
        country,
        title,
        channel_title,
        views,
        comment_count,
        ROUND(
            1000.0 * comment_count / NULLIF(views, 0),
            2
        ) AS drama_score
    FROM videos
    WHERE views >= 100000
),

ranked_videos AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY video_id
            ORDER BY drama_score DESC
        ) AS video_rank
    FROM video_scores
)

SELECT
    video_id,
    country,
    title,
    channel_title,
    views,
    comment_count,
    drama_score
FROM ranked_videos
WHERE video_rank = 1
ORDER BY drama_score DESC
LIMIT 20;