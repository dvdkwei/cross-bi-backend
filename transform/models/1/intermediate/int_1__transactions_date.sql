select
  transaction_id,
  cust_id as customer_id,
  {{format_date('tran_date')}} as transaction_date
from
  el_transactions
order by
  transaction_date