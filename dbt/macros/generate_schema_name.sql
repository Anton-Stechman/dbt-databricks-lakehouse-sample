{% macro generate_schema_name(custom_name, node) -%}
    {%- set rel_path = node.original_file_path -%}
    {%- set dirs = rel_path.split("\\") -%}
    {%- if dirs|length >= 4 and dirs[1] == "sources" -%}
        {{ dirs[3] }}
    {%- elif dirs|length >= 3 and dirs[1] == "domains" -%}
        {{ dirs[2] }}
    {%- elif dirs|length >= 2 and dirs[1] == "helpers" -%}
        {{ dirs[1] }}
    {%- else -%}
        {%- if custom_name is not none -%}
            {{ custom_name }}
        {%- else -%}
            {{ target.schema }}
        {%- endif -%}
    {%- endif -%}
{%- endmacro %}
