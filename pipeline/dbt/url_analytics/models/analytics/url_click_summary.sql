{{ config(materialized='table') }}

SELECT
    short_code,
    original_url,
    total_clicks,
    to_timestamp(first_click) AS first_click,
    to_timestamp(last_click) AS last_click,
    CAST(((last_click - first_click) / 3600) AS numeric(10,2)) AS hours_active
FROM {{ source('public', 'url_analytics') }}
WHERE total_clicks > 0