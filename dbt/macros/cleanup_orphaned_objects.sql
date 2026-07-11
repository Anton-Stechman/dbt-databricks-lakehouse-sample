{% macro cleanup_orphaned_objects() %}
  {%- if execute -%}
    {# Build the set of relations dbt currently expects to exist #}
    {%- set expected_relations = [] -%}
    {%- for node in graph.nodes.values()
        if node.resource_type in ('model', 'seed', 'snapshot') -%}
      {%- do expected_relations.append(node.schema ~ "." ~ node.alias) -%}
    {%- endfor -%}

    {%- set schemas_query -%}
      select distinct table_schema
      from {{ target.database }}.information_schema.tables
      where table_schema not in ('information_schema')
    {%- endset -%}
    {%- set schemas = run_query(schemas_query).columns[0].values() -%}

    {%- for schema in schemas -%}
      {%- set existing_query -%}
        select table_name
        from {{ target.database }}.information_schema.tables
        where table_schema = '{{ schema }}'
      {%- endset -%}
      {%- for row in run_query(existing_query).rows -%}
        {%- set full_name = schema ~ "." ~ row['table_name'] -%}
        {%- if full_name not in expected_relations -%}
          {%- do log("Dropping orphaned relation: " ~ full_name, info=true) -%}
          {%- do run_query("drop table if exists " ~ target.database ~ "." ~ full_name) -%}
        {%- endif -%}
      {%- endfor -%}
    {%- endfor -%}
  {%- endif -%}
{% endmacro %}
