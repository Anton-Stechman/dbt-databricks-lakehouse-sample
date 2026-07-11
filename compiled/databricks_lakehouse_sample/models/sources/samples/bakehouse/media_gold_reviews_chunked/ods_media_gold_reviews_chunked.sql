WITH staging_data AS (
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
    FROM `prod`.`bakehouse`.`stg_media_gold_reviews_chunked`
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