from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    customer: Mapped[str] = mapped_column(String(255), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    workload_type: Mapped[str] = mapped_column(String(64), default="other")
    criticality: Mapped[str] = mapped_column(String(32), default="medium")
    confidentiality: Mapped[str] = mapped_column(String(32), default="medium")
    integrity: Mapped[str] = mapped_column(String(32), default="medium")
    availability: Mapped[str] = mapped_column(String(32), default="medium")
    control_region: Mapped[str] = mapped_column(String(128), default="EU/EWR")
    regulatory_context: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    profile: Mapped[AssessmentProfile | None] = relationship(
        back_populates="assessment", cascade="all, delete-orphan", uselist=False
    )
    answers: Mapped[list[Answer]] = relationship(back_populates="assessment", cascade="all, delete-orphan")
    evidence: Mapped[list[Evidence]] = relationship(back_populates="assessment", cascade="all, delete-orphan")
    llm_imports: Mapped[list[LlmImport]] = relationship(back_populates="assessment", cascade="all, delete-orphan")
    llm_proposal_reviews: Mapped[list[LlmProposalReview]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )
    claims: Mapped[list[AssessmentClaim]] = relationship(back_populates="assessment", cascade="all, delete-orphan")
    gate_requirements: Mapped[list[GateRequirement]] = relationship(back_populates="assessment", cascade="all, delete-orphan")
    evidence_reviews: Mapped[list[EvidenceReview]] = relationship(back_populates="assessment", cascade="all, delete-orphan")


class AssessmentProfile(Base):
    __tablename__ = "assessment_profiles"

    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"), primary_key=True
    )
    profile_json: Mapped[str] = mapped_column(Text, default="{}")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    assessment: Mapped[Assessment] = relationship(back_populates="profile")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id", ondelete="CASCADE"), index=True)
    question_id: Mapped[str] = mapped_column(String(64), index=True)
    answer_value: Mapped[str] = mapped_column(Text, default="")
    comment: Mapped[str] = mapped_column(Text, default="")
    evidence_ids_json: Mapped[str] = mapped_column(Text, default="[]")
    review_state: Mapped[str] = mapped_column(String(32), default="draft")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    assessment: Mapped[Assessment] = relationship(back_populates="answers")


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    evidence_type: Mapped[str] = mapped_column(String(64), default="other")
    description: Mapped[str] = mapped_column(Text, default="")
    source: Mapped[str] = mapped_column(Text, default="")
    source_date: Mapped[str] = mapped_column(String(64), default="")
    content_excerpt: Mapped[str] = mapped_column(Text, default="")
    file_name: Mapped[str] = mapped_column(String(255), default="")
    stored_name: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    assessment: Mapped[Assessment] = relationship(back_populates="evidence")


class EvidenceReview(Base):
    __tablename__ = "evidence_reviews"

    evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence.id", ondelete="CASCADE"), primary_key=True)
    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id", ondelete="CASCADE"), index=True)
    applied_state: Mapped[str] = mapped_column(String(32), default="asserted")
    base_trust: Mapped[int] = mapped_column(Integer, default=0)
    scope_fit: Mapped[int] = mapped_column(Integer, default=0)
    freshness_fit: Mapped[int] = mapped_column(Integer, default=0)
    review_status: Mapped[str] = mapped_column(String(32), default="raw")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    assessment: Mapped[Assessment] = relationship(back_populates="evidence_reviews")


class AssessmentClaim(Base):
    __tablename__ = "assessment_claims"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id", ondelete="CASCADE"), index=True)
    gate_id: Mapped[str] = mapped_column(String(16), index=True)
    statement: Mapped[str] = mapped_column(Text)
    review_status: Mapped[str] = mapped_column(String(32), default="draft")
    capability_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    evidence_ids_json: Mapped[str] = mapped_column(Text, default="[]")
    question_ids_json: Mapped[str] = mapped_column(Text, default="[]")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    assessment: Mapped[Assessment] = relationship(back_populates="claims")


class GateRequirement(Base):
    __tablename__ = "gate_requirements"

    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id", ondelete="CASCADE"), primary_key=True)
    gate_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    requirement_level: Mapped[int] = mapped_column(Integer)
    source: Mapped[str] = mapped_column(String(64), default="criticality-template")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    assessment: Mapped[Assessment] = relationship(back_populates="gate_requirements")


class LlmImport(Base):
    __tablename__ = "llm_imports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id", ondelete="CASCADE"), index=True)
    raw_json: Mapped[str] = mapped_column(Text)
    proposals_json: Mapped[str] = mapped_column(Text, default="[]")
    gaps_json: Mapped[str] = mapped_column(Text, default="[]")
    warnings_json: Mapped[str] = mapped_column(Text, default="[]")
    validation_status: Mapped[str] = mapped_column(String(32), default="valid")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    assessment: Mapped[Assessment] = relationship(back_populates="llm_imports")


class LlmProposalReview(Base):
    __tablename__ = "llm_proposal_reviews"
    __table_args__ = (
        UniqueConstraint("llm_import_id", "proposal_index", name="uq_llm_proposal_review_once"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    assessment_id: Mapped[str] = mapped_column(ForeignKey("assessments.id", ondelete="CASCADE"), index=True)
    llm_import_id: Mapped[str] = mapped_column(ForeignKey("llm_imports.id", ondelete="CASCADE"), index=True)
    proposal_index: Mapped[int] = mapped_column(Integer)
    question_id: Mapped[str] = mapped_column(String(64), index=True)
    decision: Mapped[str] = mapped_column(String(32))
    final_answer_value: Mapped[str] = mapped_column(Text, default="")
    evidence_ids_json: Mapped[str] = mapped_column(Text, default="[]")
    answer_id: Mapped[str] = mapped_column(String(36), default="")
    reviewer_note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    assessment: Mapped[Assessment] = relationship(back_populates="llm_proposal_reviews")
