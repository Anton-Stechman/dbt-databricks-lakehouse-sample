WITH source_data AS (
    SELECT
        header_a AS id
        , header_b AS description
        , header_c AS is_enabled
    FROM {{ ref("test_data") }}
)

SELECT
    id
    , description
    , is_enabled
    , TRUE AS is_current
    , FALSE AS is_deleted
    , TO_DATE('19000101', 'yyyyMMdd') AS effective_from
    , TO_DATE('29991231', 'yyyyMMdd') AS effective_to
FROM source_data
