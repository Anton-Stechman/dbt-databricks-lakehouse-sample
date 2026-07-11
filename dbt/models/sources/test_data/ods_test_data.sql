WITH stg_data AS (
    SELECT
        id
        , description
        , is_enabled
        , is_current
        , is_deleted
        , effective_from
        , effective_to
    FROM {{ ref ("stg_test_data") }}
    WHERE is_current
        AND NOT is_deleted
)

SELECT
    id
    , description
    , is_enabled
    , is_current
    , is_deleted
    , effective_from
    , effective_to
FROM stg_data
