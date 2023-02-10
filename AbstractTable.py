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

    def find_by_key(self, key: str, values: any, operator: str = '='):
        query = """
        SELECT *
        FROM {table_name}
        WHERE {key} {operator} ?
        """
        values = tuple(values)
        query = query.format(table_name=self.table_name, key=key, operator=operator)
 
        return self.db.execute_read_query(query, values)

    def find_by_ids(self, ids: list, key: str):
        
        query = """
        SELECT *
        FROM {table_name}
        WHERE {key} IN ({parametered_list})
        """
        values = tuple(ids)
        parametered_list = ['?' for i in range(len(ids))]
        parametered_list = ','.join(parametered_list)
        query = query.format(table_name=self.table_name, key=key, parametered_list=parametered_list)
 
        return self.db.execute_read_query(query, values)
    
    def insert_line(self, values: list, columns: list):
        query = "INSERT INTO {table_name} ({columns}) VALUES ({values_str})"
        
        values_str = ['?' for i in range(len(columns))]
        query = query.format(
            table_name = self.table_name,
            columns = ','.join(columns),
            values_str = ','.join(values_str)
        )

        return self.db.execute_query(query, tuple(values))
    
    def insert_lines(self, values: list, columns: list):
        query = "INSERT INTO {table_name} ({columns}) VALUES ({values_str})"
        
        values_str = ['?' for i in range(len(columns))]
        query = query.format(
            table_name = self.table_name,
            columns = ','.join(columns),
            values_str = ','.join(values_str)
        )

        return self.db.execute_query(query, values)
