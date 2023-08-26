select
  cust_id as customer_id,
  count(cust_id) as transaction_frequency
from
  el_transactions
group by
  customer_id
order by
  transaction_frequency DESC