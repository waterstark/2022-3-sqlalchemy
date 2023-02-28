from app.web.config import DatabaseConfig

DATABASE_URL = f"postgresql+asyncpg://{DatabaseConfig.user}:{DatabaseConfig.password}@{DatabaseConfig.host}:{DatabaseConfig.port}/{DatabaseConfig.database}"
