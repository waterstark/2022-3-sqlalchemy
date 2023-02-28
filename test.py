import yaml
import os
from app.store.database.sqlalchemy_base import db
from app.web.config import Config, DatabaseConfig

with open(
    os.path(/Users/waterstark/code/hw-backend-summer-2022-3-sqlalchemy./config.yml)
) as fh:
    cfg = yaml.safe_load(fh)
    app_config = Config(database=DatabaseConfig(**cfg["database"]))

print(app_config)
