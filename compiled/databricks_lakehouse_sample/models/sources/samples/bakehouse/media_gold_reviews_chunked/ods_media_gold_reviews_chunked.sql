WITH  __dbt__cte__stg_media_gold_reviews_chunked as (
WITH raw_data AS (
    SELECT
        franchiseid
		, review_date
		, chunked_text
		, chunk_id
		, review_uri
    FROM `samples`.`bakehouse`.`media_gold_reviews_chunked`
)

SELECT
    franchiseid
	, review_date
	, chunked_text
	, chunk_id
	, review_uri
    , TRUE AS is_current
    , FALSE AS is_deleted
    , TO_TIMESTAMP('19000101000000', 'yyyyMMddHHmmss') AS effective_from
    , TO_TIMESTAMP('29991231235959', 'yyyyMMddHHmmss') AS effective_to
FROM raw_data
), staging_data AS (
    SELECT
        franchiseid
		, review_date
		, chunked_text
		, chunk_id
		, review_uri
        , is_current
        , is_deleted
        , effective_from
        , effective_to
    FROM __dbt__cte__stg_media_gold_reviews_chunked
)

SELECT
    franchiseid
	, review_date
	, chunked_text
	, chunk_id
	, review_uri
    , is_current
    , is_deleted
    , effective_from
    , effective_to
FROM staging_data