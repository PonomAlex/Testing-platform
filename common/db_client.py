from typing import Dict, List, Optional, Tuple

import allure
import psycopg2
from psycopg2.extras import RealDictCursor

from common.allure_attach import attach_sql_result, attach_text


class DatabaseClient:
    def __init__(
        self,
        host: str = "localhost",
        database: str = "testdb",
        user: str = "testuser",
        password: str = "testpass",
        port: int = 5432,
    ):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port,
            cursor_factory=RealDictCursor,
        )
        self.conn.autocommit = False
        self.cur = self.conn.cursor()

    @allure.step("Execute SQL: {query}")
    def execute(self, query: str, params: Optional[Tuple] = None) -> List[Dict]:
        self.cur.execute(query, params)
        rows = []
        if self.cur.description:
            rows = [dict(row) for row in self.cur.fetchall()]
            attach_sql_result(query, rows)
        else:
            attach_text("Executed SQL", query)
        return rows

    def commit(self) -> None:
        self.conn.commit()

    def rollback(self) -> None:
        self.conn.rollback()

    def close(self) -> None:
        self.cur.close()
        self.conn.close()
