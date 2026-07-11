WITH staging_data AS (
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
    FROM `prod`.`default`.`stg_sales_transactions`
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