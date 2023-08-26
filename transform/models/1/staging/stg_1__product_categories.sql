select
  prod_cat_code as product_category,
  prod_cat as product_category_desc,
  prod_sub_cat_code as product_sub_category,
  prod_subcat as product_sub_category_desc
from
  el_product_categories
order by
  product_category