with monthly_revenue as (
  select 
    extract(year from transaction_date) as transaction_year,
    extract(month from transaction_date) as transaction_month,
    sum(total_amount) as monthly_revenue
  from 
    {{ref("stg_1__transactions")}}
  group by transaction_year, transaction_month
  order by transaction_year, transaction_month
)

select * from monthly_revenue