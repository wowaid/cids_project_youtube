-- Q6: Do shouty titles get more views?
-- We measure:
-- 1. Uppercase letter ratio
-- 2. Number of exclamation marks
-- 3. Views
--
-- A title is considered "shouty" if:
-- uppercase ratio >= 0.70 OR it contains at least 2 exclamation marks.

WITH title_metrics AS (
    SELECT
        video_id,
        country,
        title,
        views,

        LENGTH(
            REGEXP_REPLACE(title, '[^[:alpha:]]', '', 'g')
        ) AS alphabetic_letters,

        LENGTH(
            REGEXP_REPLACE(title, '[^[:upper:]]', '', 'g')
        ) AS uppercase_letters,

        LENGTH(title) - LENGTH(REPLACE(title, '!', ''))
            AS exclamation_count

    FROM videos
),

shoutiness AS (
    SELECT
        video_id,
        country,
        title,
        views,

        ROUND(
            CASE
                WHEN alphabetic_letters > 0
                THEN uppercase_letters::numeric / alphabetic_letters
                ELSE 0
            END,
            2
        ) AS uppercase_ratio,

        exclamation_count,

        CASE
            WHEN
                (
                    CASE
                        WHEN alphabetic_letters > 0
                        THEN uppercase_letters::numeric / alphabetic_letters
                        ELSE 0
                    END
                ) >= 0.70
                OR exclamation_count >= 2
            THEN 'Shouty'
            ELSE 'Normal'
        END AS title_type

    FROM title_metrics
)

SELECT
    country,
    title_type,
    COUNT(*) AS videos,

    ROUND(
        AVG(views)::numeric,
        0
    ) AS average_views,

    ROUND(
        PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY views)::numeric,
        0
    ) AS median_views,

    ROUND(
        AVG(uppercase_ratio)::numeric,
        2
    ) AS avg_uppercase_ratio,

    ROUND(
        AVG(exclamation_count)::numeric,
        2
    ) AS avg_exclamation_count

FROM shoutiness

GROUP BY
    country,
    title_type

ORDER BY
    country,
    title_type;