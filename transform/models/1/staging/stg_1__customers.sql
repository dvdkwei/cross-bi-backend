select
  customer_id,
  {{format_date('dob')}} as date_of_birth,
  CASE gender
    WHEN 'M' THEN 'Male'
    WHEN 'F' THEN 'Female'
    ELSE 'Diverse'
  END gender_description,
  -- age demographics?
  city_code
from
  el_customers
order by
  customer_id