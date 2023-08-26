{% macro format_date(column_name) %}
  (to_date({{ column_name }}, 'DD-MM-YYYY'))
{% endmacro %}