import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        CURSOR.execute(
            "INSERT INTO dogs (name, breed) VALUES (?, ?)",
            (self.name, self.breed),
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self
    
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        if row is None:
            return None
        id, name, breed = row
        return cls(name=name, breed=breed, id=id)
    
    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM dogs").fetchall()
        return [cls.new_from_db(r) for r in rows]
    
    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute(
            "SELECT * FROM dogs WHERE name = ? LIMIT 1",
            (name,),
        ).fetchone()
        return cls.new_from_db(row)
    
    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute(
            "SELECT * FROM dogs WHERE id = ? LIMIT 1",
            (id,),
        ).fetchone()
        return cls.new_from_db(row)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        row = CURSOR.execute(
            "SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1",
            (name, breed),
        ).fetchone()
        if row:
            return cls.new_from_db(row)
        return cls.create(name, breed)
    
    def update(self):
        CURSOR.execute(
            "UPDATE dogs SET name = ?, breed = ? WHERE id = ?",
            (self.name, self.breed, self.id),
        )
        CONN.commit()
    