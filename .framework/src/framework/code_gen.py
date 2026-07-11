"""Module for generating dbtt script from meta data"""
import os
import json
from typing import Literal

from yaml import safe_load, safe_dump

from .utils import file_exists, dir_exists

META_PATH: str = os.path.join('.code_generation', 'meta', 'meta.json')
DEFAULT_COLUMNS: list[dict] = [
    {"name": "is_current", "description": """'{{ doc("is_current") }}'""", "data_type": "BOOLEAN"}
    , {"name": "is_deleted", "description": """'{{ doc("is_deleted") }}'""", "data_type": "BOOLEAN"}
    , {"name": "effective_from", "description": """'{{ doc("effective_from") }}'""", "data_type": "TIMESTAMP"}
    , {"name": "effective_to", "description": """'{{ doc("effective_to") }}'""", "data_type": "TIMESTAMP"}
]

def get_meta() -> dict:
    """get metadata for code gen"""
    _ = file_exists(META_PATH, on_fail="raise")
    with open(META_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def get_list_schemas(meta: dict | None = None) -> list [str]:
    """get list of available schemas"""
    meta = meta or get_meta()
    schemas: list[str] = []
    for schema in meta["schemas"]:
        if not isinstance(schema, dict):
            continue
        schema_name: str = schema["schema_name"]
        if schema_name not in schemas:
            schemas.append(schema_name)
    return schemas

def get_list_models(meta: dict | None = None, target_schema: str | None = None) -> list [str]:
    """get list of available schemas"""
    meta = meta or get_meta()
    models: list = []
    for schema in meta["schemas"]:
        if not isinstance(schema, dict):
            continue
        schema_name: str = schema["schema_name"]
        if target_schema and schema_name != target_schema:
            continue
        for model in schema["models"]:
            if not isinstance(model, dict):
                continue
            model_name = model["model_name"]
            if  model_name not in models:
                models.append(model_name)
    return models

def get_model_catalog(meta: dict | None = None) -> str:
    """get a selected model catalog"""
    meta = meta or get_meta()
    return meta["table_catalog"]

def get_model_schema(model_name: str, meta: dict | None = None) -> str:
    """get a selected model schema"""
    meta = meta or get_meta()
    for schema in meta["schemas"]:
        if not isinstance(schema, dict):
            continue
        schema_name: str = schema["schema_name"]
        for model in schema["models"]:
            if not isinstance(model, dict):
                continue
            if model_name == model["model_name"]:
                return schema_name
    raise Exception(f"Cannot find schema for model {model_name}")

def get_model_data(model_name: str, meta: dict | None = None) -> dict:
    """Get model metadata by name"""
    meta = meta or get_meta()
    for schema in meta["schemas"]:
        if not isinstance(schema, dict):
            continue
        for model in schema["models"]:
            if not isinstance(model, dict):
                continue
            if model_name == model["model_name"]:
                return model
    raise Exception(f"Cannot find data for model {model_name}")

def get_template(name: str, ftype: Literal["yml", "sql"] = "yml", replace: dict | None = None) -> str | dict:
    """Get a template sql or yaml file"""
    _content_: str = ""
    template_path: str = os.path.join(".code_generation", "templates", f"{name}.{ftype}")
    file_exists(template_path, on_fail="raise")
    with open(template_path, "r", encoding="utf-8") as temp:
        _content_: str =  temp.read()
        if replace:
            for key, val in replace.items():
                _content_ = _content_.replace(f"{{{key}}}", val)

    if ftype == "yml":
        return safe_load(_content_)
    return _content_

def generate_selected_model(model_name: str, meta: dict | None = None) -> bool:
    """Generate source and staging files from model metadata."""
    def proper(string: str) -> str:
        return string.replace("_", " ").title()

    def format_column_data(cdata: list[dict], incl_def: bool = True) -> list[dict]:
        columns: list[dict] = []
        for col in cdata:
            if not isinstance(col, dict):
                continue
            columns.append({
                "name": col["name"]
                , "description": proper(col["name"])
                , "data_type": col["data_type"]}
            )
        if incl_def:
            columns.extend(DEFAULT_COLUMNS)
        return columns

    def list_columns(cdata: list[dict]) -> list[str]:
        cnames: list[str] = []
        for col in cdata:
            if not isinstance(col, dict):
                continue
            cnames.append((col["name"]))
        return cnames

    meta = meta or get_meta()
    catalog: str = get_model_catalog(meta)
    schema: str = get_model_schema(model_name, meta)
    model_data: dict = get_model_data(model_name, meta)
    model_description: str = proper(model_name)
    column_names: list[str] = list_columns(model_data["columns"])
    columns = format_column_data(model_data["columns"])
    raw_columns = format_column_data(model_data["columns"], False)
    cte_columns: str = "\n\t\t, ".join(column_names).lower()
    final_columns: str = "\n\t, ".join(column_names).lower()

    # Create output directory
    output_dir = os.path.join("dbt", "models", "sources", catalog, schema, model_name)
    dir_exists(output_dir)

    # Generate src file
    src: dict = get_template("src", ftype="yml")
    src["sources"][0]["name"] = schema
    src["sources"][0]["database"] = catalog
    src["sources"][0]["schema"] = schema
    src["sources"][0]["tables"][0]["name"] = model_name
    src["sources"][0]["tables"][0]["columns"] = raw_columns
    src_name: str = f"{model_name}.yml"
    src_fpath: str = os.path.join(output_dir, src_name)
    with open(src_fpath, "w", encoding="utf-8") as srcfile:
        srcfile.write(safe_dump(src, sort_keys=False))

    # Generate stg file
    stg: dict = get_template("stg", ftype="yml", replace={"name": model_name, "description": model_description})
    stg["models"][0]["columns"] = columns
    stg_name: str = f"stg_{model_name}.yml"
    stg_fpath: str = os.path.join(output_dir, stg_name)
    with open(stg_fpath, "w", encoding="utf-8") as stgfile:
        stgfile.write(safe_dump(stg, sort_keys=False))

    # Generate stg file
    stgsql: str = get_template("stg", ftype="sql", replace={"name": model_name, "cte-columns": cte_columns, "columns": final_columns, "schema": schema})
    stgsqlname: str = f"stg_{model_name}.sql"
    stg_fpath: str = os.path.join(output_dir, stgsqlname)
    with open(stg_fpath, "w", encoding="utf-8") as stgfile:
        stgfile.write(stgsql)

    # Generate ods file
    ods: dict = get_template("ods", ftype="yml", replace={"name": model_name, "description": model_description})
    ods["models"][0]["columns"] = columns
    ods_name: str = f"ods_{model_name}.yml"
    ods_fpath: str = os.path.join(output_dir, ods_name)
    with open(ods_fpath, "w", encoding="utf-8") as odsfile:
        odsfile.write(safe_dump(ods, sort_keys=False))

    # Generate ods file
    odssql: str = get_template("ods", ftype="sql", replace={"name": model_name, "cte-columns": cte_columns, "columns": final_columns})
    odssqlname: str = f"ods_{model_name}.sql"
    ods_fpath: str = os.path.join(output_dir, odssqlname)
    with open(ods_fpath, "w", encoding="utf-8") as odsfile:
        odsfile.write(odssql)

    return True

if __name__== "__main__":
    print(generate_selected_model("sales_customers"))
