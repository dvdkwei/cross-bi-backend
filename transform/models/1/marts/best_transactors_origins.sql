with transactions_count as (
  select * from {{ref('int_1__transactions_count_customer')}}
  where transaction_frequency in (
    select max(transaction_frequency) 
    from int_1__transactions_count_customer
  )
  order by customer_id
),

customer_cities as (
  select customer_id, city_code from {{ref("stg_1__customers")}}
),

cities as (
  select * from {{ref("stg_1__cities")}}
),

best_contributors_origins as (
  select
    transactions_count.customer_id,
    transactions_count.transaction_frequency,
    customer_cities.city_code,
    cities.city_name,
    cities.country_code
  from transactions_count
  left join customer_cities using (customer_id)
  left join cities using (city_code)
)

select * from best_contributors_origins