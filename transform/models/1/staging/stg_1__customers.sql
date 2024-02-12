SELECT
  customer_id,
  {{format_date('dob')}} as date_of_birth,
  CASE gender
    WHEN 'M' THEN 'Male'
    WHEN 'F' THEN 'Female'
    ELSE 'Diverse'
  END gender_description,
  -- age demographics?
  city_code
FROM
  el_customers
ORDER BY
  customer_id