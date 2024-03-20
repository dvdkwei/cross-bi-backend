with transactions as (
  select * from {{ref('stg_1__transactions')}}
),

customer_over_the_years as(
  select 
    extract(year from transaction_date) as transaction_year,
    count(DISTINCT customer_id) as customers
  from 
    transactions
  group by 
    transaction_year
  order by 
    transaction_year ASC
)

select * from customer_over_the_years