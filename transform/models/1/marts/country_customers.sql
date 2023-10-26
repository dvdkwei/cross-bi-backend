with country_customers as(
  select
    country_code,
    count(distinct customer_id) as customers
  from
    {{ref('stg_1__transactions')}} 
    join {{ref('stg_1__customers')}} using (customer_id)
    join {{ref('stg_1__cities')}} using (city_code)
  group by
    country_code
)
select
  *
from
  country_customers