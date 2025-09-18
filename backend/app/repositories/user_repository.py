# async repository using aiosqlite - encapsulated DB access (single responsibility)
import aiosqlite
from typing import Optional
from passlib.context import CryptContext
from backend.app.core.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User:
    def __init__(self, id: int, first_name: str, last_name: str, email: str, password_hash: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash

class UserRepository:
    def __init__(self, db_path: str = settings.SQLITE_DB):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );
            """)
            await db.commit()

    async def create_user(self, first_name: str, last_name: str, email: str, password: str) -> User:
        hash_ = pwd_ctx.hash(password)
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                "INSERT INTO users(first_name,last_name,email,password_hash) VALUES(?,?,?,?)",
                (first_name, last_name, email, hash_)
            )
            await db.commit()
            uid = cur.lastrowid
            return User(uid, first_name, last_name, email, hash_)

    async def find_by_email(self, email: str) -> Optional[User]:
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute("SELECT id,first_name,last_name,email,password_hash FROM users WHERE email = ?", (email,))
            row = await cur.fetchone()
            if row:
                return User(*row)
        return None

    async def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_ctx.verify(plain, hashed)
