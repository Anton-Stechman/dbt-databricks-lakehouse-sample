{% macro generate_pk(columns = []) %}
MD5(CONCAT_WS('_'{% for c in columns -%}, COALESCE(CAST({{ c }} AS VARCHAR(500)), 'Unknown') {% endfor -%}))
{% endmacro %}
