with country_revenue as(
  select 
    TO_CHAR(transaction_date, 'YYYY-MM') as timestamp,
    country_code,
    sum(total_amount) as revenue
  from 
    {{ref('stg_1__transactions')}} 
	join {{ref('stg_1__customers')}}using (customer_id)
	join {{ref('stg_1__cities')}} using (city_code)
  group by timestamp, country_code
  order by timestamp
)

select * from country_revenue