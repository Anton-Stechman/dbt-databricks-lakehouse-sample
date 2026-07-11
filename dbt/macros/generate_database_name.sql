{% macro generate_database_name(custom_name, node) -%}
{%- if custom_name is not none -%}
    {{ custom_name }}
{%- else  -%}
    {{ target.database }}
{%- endif -%}
{%- endmacro %}
