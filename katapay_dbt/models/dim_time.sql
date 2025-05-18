SELECT DISTINCT
    timestamp,
    DATE(timestamp) AS date,
    EXTRACT(HOUR FROM timestamp) AS hour,
    TO_CHAR(timestamp, 'Day') AS day_of_week
FROM {{ ref('fact_transactions') }}