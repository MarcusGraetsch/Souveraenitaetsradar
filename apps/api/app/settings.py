from __future__ import annotations

import os
from pathlib import Path


class Settings:
    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./.runtime/sovradar.db")
        self.runtime_dir = Path(os.getenv("SOVRADAR_RUNTIME_DIR", ".runtime")).resolve()
        self.documents_dir = self.runtime_dir / "documents"
        self.method_dir = Path(os.getenv("SOVRADAR_METHOD_DIR", "data/method")).resolve()
        self.max_upload_bytes = int(os.getenv("SOVRADAR_MAX_UPLOAD_BYTES", str(50 * 1024 * 1024)))

    def ensure_runtime(self) -> None:
        self.runtime_dir.mkdir(parents=True, exist_ok=True)
        self.documents_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
