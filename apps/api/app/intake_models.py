from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base
from .models import utcnow


class AssessmentIntakeContext(Base):
    __tablename__ = "assessment_intake_contexts"

    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"), primary_key=True
    )
    context_json: Mapped[str] = mapped_column(Text)
    pre_assessment_json: Mapped[str] = mapped_column(Text)
    schema_version: Mapped[str] = mapped_column(Text, default="0.5")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
