-- macros/drop_schema.sql
{% macro drop_schema(schema) %}
  {% set drop_query %}
    DROP SCHEMA IF EXISTS {{ target.catalog }}.{{ schema }} CASCADE
  {% endset %}
  {% do run_query(drop_query) %}
  {{ log("Dropped schema " ~ target.catalog ~ "." ~ schema, info=true) }}
{% endmacro %}
