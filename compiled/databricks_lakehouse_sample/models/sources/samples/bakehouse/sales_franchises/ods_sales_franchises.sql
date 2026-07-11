WITH staging_data AS (
    SELECT
        franchiseid
		, name
		, city
		, district
		, zipcode
		, country
		, size
		, longitude
		, latitude
		, supplierid
        , is_current
        , is_deleted
        , effective_from
        , effective_to
    FROM `workspace`.`project_prod`.`stg_sales_franchises`
)

SELECT
    franchiseid
	, name
	, city
	, district
	, zipcode
	, country
	, size
	, longitude
	, latitude
	, supplierid
    , is_current
    , is_deleted
    , effective_from
    , effective_to
FROM staging_data