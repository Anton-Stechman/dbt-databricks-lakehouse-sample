WITH staging_data AS  (
    SELECT
        {cte-columns}
        , is_current
        , is_deleted
        , effective_from
        , effective_to
    FROM {{ ref('stg_{name}') }}
)

SELECT
    {columns}
    , is_current
    , is_deleted
    , effective_from
    , effective_to
FROM staging_data
