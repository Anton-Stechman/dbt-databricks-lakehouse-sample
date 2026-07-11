WITH  __dbt__cte__stg_media_customer_reviews as (
WITH raw_data AS (
    SELECT
        review
		, franchiseid
		, review_date
		, new_id
    FROM `samples`.`bakehouse`.`media_customer_reviews`
)

SELECT
    review
	, franchiseid
	, review_date
	, new_id
    , TRUE AS is_current
    , FALSE AS is_deleted
    , TO_TIMESTAMP('19000101000000', 'yyyyMMddHHmmss') AS effective_from
    , TO_TIMESTAMP('29991231235959', 'yyyyMMddHHmmss') AS effective_to
FROM raw_data
), staging_data AS (
    SELECT
        review
		, franchiseid
		, review_date
		, new_id
        , is_current
        , is_deleted
        , effective_from
        , effective_to
    FROM __dbt__cte__stg_media_customer_reviews
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