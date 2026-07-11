WITH staging_data AS  (
    SELECT
        {columns}
        , is_current
        , is_deleted
        , effective_from
        , effective_to
    FROM {{ source('{schema}', '{table}') }}
)

SELECT
    {columns}
    , is_current
    , is_deleted
    , effective_from
    , effective_to
FROM staging_data
