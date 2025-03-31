from pydantic import BaseModel


class Sentry(BaseModel):
    dsn: str


class Postgres(BaseModel):
    user: str
    password: str
    db: str
    host: str
    port: str

    provider: str = "postgresql+asyncpg"

    @property
    def url(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def url_localhost(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@localhost:{self.port}/{self.db}"


class Runner(BaseModel):
    workers: int


class Server(BaseModel):
    port: int
    workers: int
    root_path: str


class JWT(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30