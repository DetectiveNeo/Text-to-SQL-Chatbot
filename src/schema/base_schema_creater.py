from src.config import Config

from dataclasses import dataclass, field
from typing import List, Optional
import json


@dataclass
class ColumnSchema:
    name: str
    dtype: str
    description: Optional[str] = None   # fill later
    is_primary_key: bool = False


@dataclass
class RelationshipSchema:
    source: str        # e.g. "orders.customer_id"
    target: str        # e.g. "customers.id"


@dataclass
class TableSchema:
    name: str
    description: Optional[str] = None   # fill later
    columns: List[ColumnSchema] = field(default_factory=list)
    relationships: List[RelationshipSchema] = field(default_factory=list)


import sqlite3
from typing import List

def extract_base_schema(db_path: str) -> List[TableSchema]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """)
    tables = cursor.fetchall()

    table_schemas: List[TableSchema] = []

    for (table_name,) in tables:
        print(table_name)
        cursor.execute(f'PRAGMA table_info("{table_name}");')
        columns_info = cursor.fetchall()

        columns = []
        for col in columns_info:
            columns.append(
                ColumnSchema(
                    name=col[1],
                    dtype=col[2],
                    is_primary_key=bool(col[5])
                )
            )

        table_schemas.append(
            TableSchema(
                name=table_name,
                columns=columns
            )
        )

        # break

    conn.close()

    return table_schemas


import json
from typing import List
# from src.schema.schema_types import TableSchema


def save_schema(schema: List[TableSchema], path: str):
    with open(path, "w") as f:
        json.dump(
            [
                {
                    "table": t.name,
                    "description": t.description,
                    "columns": [
                        {"name": c.name, "type": c.dtype, "desc": c.description}
                        for c in t.columns
                    ],
                    "relationships": [
                        {"from": r.source, "to": r.target}
                        for r in t.relationships
                    ]
                }
                for t in schema
            ],
            f,
            indent=2
        )

cfg = Config()



if __name__ == "__main__":

    TableSchema = extract_base_schema(cfg.database_path)

    print(TableSchema)

    save_schema(TableSchema, cfg.schema_path)

