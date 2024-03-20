with transactions as (
  select * from {{ref('stg_1__transactions')}}
),

customers as (
  select
    extract(year from transaction_date) as year,
    count(distinct customer_id) as customers_total
  from transactions
  where
    extract(year from transaction_date) in (2012,2013)
  group by
    year
),

customer_growth as (
  select round(((c2_total - c1_total)/c1_total) * 100.0, 2) as growth 
  from(
    select 
      (c1.customers_total * 1.0) as c1_total, 
      (c2.customers_total * 1.0) as c2_total
    from 
      customers as c1, customers as c2
    WHERE
      c1.year = 2012
      AND 
      c2.year = 2013
  ) as g
)

select * from customer_growth