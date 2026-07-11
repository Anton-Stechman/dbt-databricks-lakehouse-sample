WITH raw_data AS  (
    SELECT
        customerID
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
    FROM {{ source('bakehouse', 'sales_customers') }}
)

SELECT
    customerID
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
    , TRUE AS is_current
    , FALSE AS is_deleted
    , TO_TIMESTAMP('19000101000000', 'yyyyMMddHHmmss') AS effective_from
    , TO_TIMESTAMP('29991231235959', 'yyyyMMddHHmmss') AS effective_to
FROM raw_data
