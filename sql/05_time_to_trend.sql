-- Q5: How many days pass between publishing and trending?
-- Time to Trend = Trending Date - Publication Date.
-- We calculate the average, median and minimum/maximum delay
-- for each country.

WITH time_to_trend AS (
    SELECT
        country,
        video_id,
        TO_DATE(trending_date, 'YY.DD.MM') AS trending_date,
        publish_time::timestamp AS publish_timestamp,
        TO_DATE(trending_date, 'YY.DD.MM')
            - publish_time::timestamp::date AS days_to_trend
    FROM videos
)

SELECT
    country,
    COUNT(*) AS videos,
    ROUND(AVG(days_to_trend)::numeric, 2) AS average_days_to_trend,
    ROUND(
        PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY days_to_trend)::numeric,
        2
    ) AS median_days_to_trend,
    MIN(days_to_trend) AS minimum_days_to_trend,
    MAX(days_to_trend) AS maximum_days_to_trend
FROM time_to_trend
WHERE days_to_trend >= 0
GROUP BY country
ORDER BY median_days_to_trend;