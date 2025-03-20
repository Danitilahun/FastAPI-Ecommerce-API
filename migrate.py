from alembic.config import Config
from alembic import command

alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")



# find . -name "__pycache__" -type d -print0 | xargs -0 rm -rf