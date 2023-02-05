"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database

class AbstractTable:

    _table_name = None

    def __init__(self, db: Database) -> None:
        self.table_name = self._table_name
        self.db = db

    def all(self):
        query = """
        SELECT *
        FROM {table_name}
        """

        query = query.format(table_name=self.table_name)

        return self.db.execute_read_query(query)
