from app.web.config import DatabaseConfig

# DATABASE_URL = f"postgresql+asyncpg://{DatabaseConfig.user}:{DatabaseConfig.password}@{DatabaseConfig.host}:{DatabaseConfig.port}/{DatabaseConfig.database}"
DATABASE_URL = "postgresql+asyncpg://kts_user:kts_pass@0.0.0.0:5432/kts"
