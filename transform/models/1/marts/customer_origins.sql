with customer_origins as (
  select 
    count(country_code) as Customers, 
    country_code as Countries
  from 
    {{ref('stg_1__customers')}}
  join {{ref('stg_1__cities')}} using (city_code)
  group by country_code
)

select * from customer_origins