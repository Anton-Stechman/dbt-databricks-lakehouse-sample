WITH  __dbt__cte__stg_sales_suppliers as (
WITH raw_data AS (
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
    FROM `samples`.`bakehouse`.`sales_suppliers`
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
    , TRUE AS is_current
    , FALSE AS is_deleted
    , TO_TIMESTAMP('19000101000000', 'yyyyMMddHHmmss') AS effective_from
    , TO_TIMESTAMP('29991231235959', 'yyyyMMddHHmmss') AS effective_to
FROM raw_data
), staging_data AS (
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
    FROM __dbt__cte__stg_sales_suppliers
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