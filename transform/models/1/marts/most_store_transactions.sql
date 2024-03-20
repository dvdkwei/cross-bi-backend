with transactions as (
  select * from {{ref('stg_1__transactions')}}
),

most_store_transactions as (
  select store_type from (
    select store_type, count(store_type) as store_trs 
    from transactions 
    group by store_type
  ) as h
  where store_trs in (
    select max(store_transactions) from(
      select count(store_type) as store_transactions, store_type 
      from transactions 
      group by store_Type
    ) as g
  )
  group by store_type
)

select * from most_store_transactions