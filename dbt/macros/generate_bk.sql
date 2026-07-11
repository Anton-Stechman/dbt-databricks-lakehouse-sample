{% macro generate_bk(columns = []) %}
CONCAT_WS('_'{% for c in columns -%}, COALESCE(CAST({{ c }} AS VARCHAR(500)), '') {% endfor -%})
{% endmacro %}
