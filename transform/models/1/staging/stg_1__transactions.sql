select
  transaction_id,
  cust_id as customer_id,
  {{format_date('tran_date')}} as transaction_date,
  prod_cat_code as product_category,
  prod_subcat_code as product_sub_category,
  qty as quantity,
  rate as conversion_rate,
  tax,
  total_amt as total_amount,
  store_type 
from
  el_transactions
order by
  transaction_date