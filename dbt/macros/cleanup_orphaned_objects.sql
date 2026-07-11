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

    {%- set dropped_tables = [] -%}
    {%- set dropped_views = [] -%}

    {%- for schema in schemas -%}
      {%- set existing_query -%}
        select table_name, table_type
        from {{ target.database }}.information_schema.tables
        where table_schema = '{{ schema }}'
      {%- endset -%}
      {%- for row in run_query(existing_query).rows -%}
        {%- set full_name = schema ~ "." ~ row['table_name'] -%}
        {%- if full_name not in expected_relations -%}
          {%- if row['table_type'] == 'VIEW' -%}
            {%- do log("Dropping orphaned view: " ~ full_name, info=true) -%}
            {%- do run_query("drop view if exists " ~ target.database ~ "." ~ full_name) -%}
            {%- do dropped_views.append(full_name) -%}
          {%- else -%}
            {%- do log("Dropping orphaned table: " ~ full_name, info=true) -%}
            {%- do run_query("drop table if exists " ~ target.database ~ "." ~ full_name) -%}
            {%- do dropped_tables.append(full_name) -%}
          {%- endif -%}
        {%- endif -%}
      {%- endfor -%}
    {%- endfor -%}

    {%- if dropped_tables | length == 0 and dropped_views | length == 0 -%}
      {%- do log("No models to drop", info=true) -%}
    {%- else -%}
      {%- if dropped_tables | length > 0 -%}
        {%- do log(dropped_tables | length ~ " orphaned table(s) dropped: " ~ dropped_tables | join(", "), info=true) -%}
      {%- endif -%}
      {%- if dropped_views | length > 0 -%}
        {%- do log(dropped_views | length ~ " orphaned view(s) dropped: " ~ dropped_views | join(", "), info=true) -%}
      {%- endif -%}
    {%- endif -%}

    {%- set dropped_schemas = [] -%}
    {%- for schema in schemas -%}
      {%- set count_query -%}
        select count(*) as cnt
        from {{ target.database }}.information_schema.tables
        where table_schema = '{{ schema }}'
      {%- endset -%}
      {%- set obj_count = run_query(count_query).columns[0].values()[0] -%}

      {%- if obj_count == 0 -%}
        {%- do log("Dropping empty schema: " ~ schema, info=true) -%}
        {%- do run_query("drop schema if exists " ~ target.database ~ "." ~ schema) -%}
        {%- do dropped_schemas.append(schema) -%}
      {%- endif -%}
    {%- endfor -%}

    {%- if dropped_schemas | length == 0 -%}
      {%- do log("No schemas to drop", info=true) -%}
    {%- else -%}
      {%- do log(dropped_schemas | length ~ " empty schema(s) dropped: " ~ dropped_schemas | join(", "), info=true) -%}
    {%- endif -%}

  {%- endif -%}
{% endmacro %}
