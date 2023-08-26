with transactions as (
  select * from {{ref('stg_1__transactions')}}
),

annual_revenue as(
  select 
    extract(year from transaction_date) as transaction_year,
    sum(total_amount) as total_revenue
  from 
    transactions
  group by 
    transaction_year
  order by 
    transaction_year ASC
)

select * from annual_revenue