"""
    file to store the context of app
"""

from typing import Optional

from app.database import Postgres


class AppContext:
    db: Optional[Postgres]


app_context = AppContext()
