-- Q2: Which countries are the most music-obsessed and gaming-obsessed?
-- Measure the share of Music and Gaming videos among all Trending videos.

SELECT
    v.country,
    COUNT(*) AS total_videos,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE c.category_name = 'Music'
        ) / COUNT(*),
        2
    ) AS music_share_percent,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE c.category_name = 'Gaming'
        ) / COUNT(*),
        2
    ) AS gaming_share_percent

FROM videos v
JOIN categories c
    ON v.category_id = c.category_id

GROUP BY v.country
ORDER BY music_share_percent DESC;