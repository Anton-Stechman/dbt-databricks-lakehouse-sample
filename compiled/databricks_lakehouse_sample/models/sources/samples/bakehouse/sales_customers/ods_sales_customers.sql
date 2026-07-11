WITH staging_data AS (
    SELECT
        customerid
		, first_name
		, last_name
		, email_address
		, phone_number
		, address
		, city
		, state
		, country
		, continent
		, postal_zip_code
		, gender
        , is_current
        , is_deleted
        , effective_from
        , effective_to
    FROM `workspace`.`project_prod`.`stg_sales_customers`
)

SELECT
    customerid
	, first_name
	, last_name
	, email_address
	, phone_number
	, address
	, city
	, state
	, country
	, continent
	, postal_zip_code
	, gender
    , is_current
    , is_deleted
    , effective_from
    , effective_to
FROM staging_data