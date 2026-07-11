WITH staging_data AS (
    SELECT
        supplierid
		, name
		, ingredient
		, continent
		, city
		, district
		, size
		, longitude
		, latitude
		, approved
        , is_current
        , is_deleted
        , effective_from
        , effective_to
    FROM `prod`.`bakehouse`.`stg_sales_suppliers`
)

SELECT
    supplierid
	, name
	, ingredient
	, continent
	, city
	, district
	, size
	, longitude
	, latitude
	, approved
    , is_current
    , is_deleted
    , effective_from
    , effective_to
FROM staging_data