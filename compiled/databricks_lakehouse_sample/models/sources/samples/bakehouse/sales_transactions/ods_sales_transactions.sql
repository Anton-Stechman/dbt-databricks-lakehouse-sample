WITH  __dbt__cte__stg_sales_transactions as (
WITH raw_data AS (
    SELECT
        transactionid
		, customerid
		, franchiseid
		, datetime
		, product
		, quantity
		, unitprice
		, totalprice
		, paymentmethod
		, cardnumber
    FROM `samples`.`bakehouse`.`sales_transactions`
)

SELECT
    transactionid
	, customerid
	, franchiseid
	, datetime
	, product
	, quantity
	, unitprice
	, totalprice
	, paymentmethod
	, cardnumber
    , TRUE AS is_current
    , FALSE AS is_deleted
    , TO_TIMESTAMP('19000101000000', 'yyyyMMddHHmmss') AS effective_from
    , TO_TIMESTAMP('29991231235959', 'yyyyMMddHHmmss') AS effective_to
FROM raw_data
), staging_data AS (
    SELECT
        transactionid
		, customerid
		, franchiseid
		, datetime
		, product
		, quantity
		, unitprice
		, totalprice
		, paymentmethod
		, cardnumber
        , is_current
        , is_deleted
        , effective_from
        , effective_to
    FROM __dbt__cte__stg_sales_transactions
)

SELECT
    transactionid
	, customerid
	, franchiseid
	, datetime
	, product
	, quantity
	, unitprice
	, totalprice
	, paymentmethod
	, cardnumber
    , is_current
    , is_deleted
    , effective_from
    , effective_to
FROM staging_data