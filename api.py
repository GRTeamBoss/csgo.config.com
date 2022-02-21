import sqlite3


def insert(data: str, table: str, column=False) -> None:
    db = sqlite3.connect("./data/api.db")
    if column:
        db.execute(f"insert into {table} ({column}) values ({data})")
    else:
        db.execute(f"insert into {table} values ({data})")
    db.commit()
    db.close()


def update(data: str, table: str, condition=False) -> None:
    db = sqlite3.connect("./data/api.db")
    if condition:
        db.execute(f"update {table} set {data} where {condition}")
    else:
        db.execute(f"update {table} set {data}")
    db.commit()
    db.close()


def delete(table: str, condition=False) -> None:
    db = sqlite3.connect("./data/api.db")
    if condition:
        db.execute(f"delete from {table} where {condition}")
    else:
        db.execute(f"delete from {table}")
    db.commit()
    db.close()


def select(table: str, column="*", condition=False) -> list:
    """
    :param column: str
    """
    db = sqlite3.connect("./data/api.db")
    if condition:
        response = list(db.execute(f"select {column} from {table} where {condition}"))
    else:
        response = list(db.execute(f"select {column} from {table}"))
    db.close()
    return response
