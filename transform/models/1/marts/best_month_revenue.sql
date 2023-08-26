with highest_revenue_month as(
  select 
	transaction_year,
	transaction_month,
	monthly_revenue as revenue
FROM  
	{{ref("int_1__monthly_revenue")}}
where
	monthly_revenue in(
		select max(monthly_revenue) as monthly_revenue
		from {{ref("int_1__monthly_revenue")}}
		group by transaction_year
	)
)

select * from highest_revenue_month