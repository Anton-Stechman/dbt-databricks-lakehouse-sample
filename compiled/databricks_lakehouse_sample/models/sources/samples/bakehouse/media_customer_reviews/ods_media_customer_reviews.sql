WITH staging_data AS (
    SELECT
        review
		, franchiseid
		, review_date
		, new_id
        , is_current
        , is_deleted
        , effective_from
        , effective_to
    FROM `prod`.`bakehouse`.`stg_media_customer_reviews`
)

SELECT
    review
	, franchiseid
	, review_date
	, new_id
    , is_current
    , is_deleted
    , effective_from
    , effective_to
FROM staging_data