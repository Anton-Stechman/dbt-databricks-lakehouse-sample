WITH raw_data AS (
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
    FROM `samples`.`bakehouse`.`sales_franchises`
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
    , TRUE AS is_current
    , FALSE AS is_deleted
    , TO_TIMESTAMP('19000101000000', 'yyyyMMddHHmmss') AS effective_from
    , TO_TIMESTAMP('29991231235959', 'yyyyMMddHHmmss') AS effective_to
FROM raw_data