import json
from typing import Any, Iterable

import allure


def attach_json(name: str, payload: Any) -> None:
    allure.attach(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_text(name: str, text: str) -> None:
    allure.attach(text, name=name, attachment_type=allure.attachment_type.TEXT)


def attach_sql_result(query: str, rows: Iterable[dict]) -> None:
    formatted = {
        "query": query,
        "rows": list(rows),
    }
    attach_json("SQL result", formatted)
