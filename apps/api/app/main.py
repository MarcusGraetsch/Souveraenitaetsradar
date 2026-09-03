from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .llm_bridge import build_prompt
from .method_catalog import load_questions, question_ids
from .models import Answer, Assessment, Evidence, LlmImport
from .schemas import AnswerOut, AnswerUpsert, AssessmentCreate, AssessmentOut, EvidenceOut, LlmBridgeResult, LlmImportOut
from .settings import settings

app = FastAPI(title="Souveränitäts-Radar API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
def startup() -> None:
    settings.ensure_runtime()
    Base.metadata.create_all(bind=engine)


def as_assessment(model: Assessment) -> AssessmentOut:
    return AssessmentOut.model_validate(model)


def as_answer(model: Answer) -> AnswerOut:
    return AnswerOut(id=model.id, assessment_id=model.assessment_id, question_id=model.question_id, answer_value=model.answer_value, comment=model.comment, evidence_ids=json.loads(model.evidence_ids_json or "[]"), review_state=model.review_state, updated_at=model.updated_at)


def as_evidence(model: Evidence) -> EvidenceOut:
    return EvidenceOut(id=model.id, assessment_id=model.assessment_id, title=model.title, evidence_type=model.evidence_type, description=model.description, source=model.source, source_date=model.source_date, content_excerpt=model.content_excerpt, file_name=model.file_name, created_at=model.created_at)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "sovradar-api", "method_questions": len(load_questions())}


@app.get("/api/assessments", response_model=list[AssessmentOut])
def list_assessments(db: Session = Depends(get_db)):
    rows = db.scalars(select(Assessment).order_by(Assessment.updated_at.desc())).all()
    return [as_assessment(row) for row in rows]


@app.post("/api/assessments", response_model=AssessmentOut, status_code=201)
def create_assessment(payload: AssessmentCreate, db: Session = Depends(get_db)):
    row = Assessment(id=str(uuid.uuid4()), **payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return as_assessment(row)


@app.get("/api/assessments/{assessment_id}", response_model=AssessmentOut)
def get_assessment(assessment_id: str, db: Session = Depends(get_db)):
    row = db.get(Assessment, assessment_id)
    if not row:
        raise HTTPException(404, "Assessment not found")
    return as_assessment(row)


@app.delete("/api/assessments/{assessment_id}", status_code=204)
def delete_assessment(assessment_id: str, db: Session = Depends(get_db)):
    row = db.get(Assessment, assessment_id)
    if not row:
        raise HTTPException(404, "Assessment not found")
    assessment_dir = settings.documents_dir / assessment_id
    db.delete(row)
    db.commit()
    shutil.rmtree(assessment_dir, ignore_errors=True)


@app.get("/api/method/questions")
def questions(domain: str | None = None):
    rows = load_questions()
    if domain:
        rows = [row for row in rows if row["domain"] == domain]
    return rows


@app.get("/api/assessments/{assessment_id}/answers", response_model=list[AnswerOut])
def list_answers(assessment_id: str, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    rows = db.scalars(select(Answer).where(Answer.assessment_id == assessment_id)).all()
    return [as_answer(row) for row in rows]


@app.put("/api/assessments/{assessment_id}/answers/{question_id}", response_model=AnswerOut)
def upsert_answer(assessment_id: str, question_id: str, payload: AnswerUpsert, db: Session = Depends(get_db)):
    if payload.question_id != question_id:
        raise HTTPException(400, "question_id mismatch")
    if question_id not in question_ids():
        raise HTTPException(400, "unknown question_id")
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    row = db.scalar(select(Answer).where(Answer.assessment_id == assessment_id, Answer.question_id == question_id))
    if row is None:
        row = Answer(id=str(uuid.uuid4()), assessment_id=assessment_id, question_id=question_id)
        db.add(row)
    row.answer_value = payload.answer_value
    row.comment = payload.comment
    row.evidence_ids_json = json.dumps(payload.evidence_ids)
    row.review_state = payload.review_state
    db.commit()
    db.refresh(row)
    return as_answer(row)


@app.get("/api/assessments/{assessment_id}/evidence", response_model=list[EvidenceOut])
def list_evidence(assessment_id: str, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    rows = db.scalars(select(Evidence).where(Evidence.assessment_id == assessment_id)).all()
    return [as_evidence(row) for row in rows]


@app.post("/api/assessments/{assessment_id}/evidence", response_model=EvidenceOut, status_code=201)
async def create_evidence(assessment_id: str, title: str = Form(...), evidence_type: str = Form("other"), description: str = Form(""), source: str = Form(""), source_date: str = Form(""), content_excerpt: str = Form(""), file: UploadFile | None = File(None), db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    evidence_id = str(uuid.uuid4())
    file_name = ""
    stored_name = ""
    if file and file.filename:
        file_name = Path(file.filename).name[:255]
        suffix = Path(file_name).suffix[:20]
        stored_name = f"{evidence_id}{suffix}"
        target_dir = settings.documents_dir / assessment_id
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / stored_name
        size = 0
        with target.open("wb") as handle:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > settings.max_upload_bytes:
                    handle.close()
                    target.unlink(missing_ok=True)
                    raise HTTPException(413, "file exceeds upload limit")
                handle.write(chunk)
    row = Evidence(id=evidence_id, assessment_id=assessment_id, title=title, evidence_type=evidence_type, description=description, source=source, source_date=source_date, content_excerpt=content_excerpt, file_name=file_name, stored_name=stored_name)
    db.add(row)
    db.commit()
    db.refresh(row)
    return as_evidence(row)


@app.get("/api/assessments/{assessment_id}/llm-bridge/prompt")
def llm_prompt(assessment_id: str, db: Session = Depends(get_db)):
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(404, "Assessment not found")
    answers = [as_answer(row).model_dump() for row in db.scalars(select(Answer).where(Answer.assessment_id == assessment_id)).all()]
    evidence = [as_evidence(row).model_dump() for row in db.scalars(select(Evidence).where(Evidence.assessment_id == assessment_id)).all()]
    return {"prompt": build_prompt(as_assessment(assessment).model_dump(), answers, evidence)}


@app.post("/api/assessments/{assessment_id}/llm-bridge/import", response_model=LlmImportOut)
def import_llm_result(assessment_id: str, payload: LlmBridgeResult, db: Session = Depends(get_db)):
    if payload.assessment_id != assessment_id:
        raise HTTPException(400, "assessment_id mismatch")
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    known_questions = question_ids()
    known_evidence = set(db.scalars(select(Evidence.id).where(Evidence.assessment_id == assessment_id)).all())
    for proposal in payload.proposals:
        if proposal.question_id not in known_questions:
            raise HTTPException(422, f"unknown question_id: {proposal.question_id}")
        unknown_evidence = set(proposal.evidence_ids) - known_evidence
        if unknown_evidence:
            raise HTTPException(422, f"unknown evidence id(s): {sorted(unknown_evidence)}")
    for gap in payload.evidence_gaps:
        if gap.question_id not in known_questions:
            raise HTTPException(422, f"unknown question_id: {gap.question_id}")
    row = LlmImport(id=str(uuid.uuid4()), assessment_id=assessment_id, raw_json=payload.model_dump_json(), proposals_json=json.dumps([p.model_dump() for p in payload.proposals], ensure_ascii=False), gaps_json=json.dumps([g.model_dump() for g in payload.evidence_gaps], ensure_ascii=False), warnings_json=json.dumps(payload.warnings, ensure_ascii=False), validation_status="valid")
    db.add(row)
    db.commit()
    db.refresh(row)
    return LlmImportOut(id=row.id, assessment_id=assessment_id, validation_status=row.validation_status, proposals=payload.proposals, evidence_gaps=payload.evidence_gaps, warnings=payload.warnings, created_at=row.created_at)


@app.get("/api/assessments/{assessment_id}/llm-bridge/imports", response_model=list[LlmImportOut])
def list_llm_imports(assessment_id: str, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    rows = db.scalars(select(LlmImport).where(LlmImport.assessment_id == assessment_id).order_by(LlmImport.created_at.desc())).all()
    return [LlmImportOut(id=row.id, assessment_id=row.assessment_id, validation_status=row.validation_status, proposals=json.loads(row.proposals_json), evidence_gaps=json.loads(row.gaps_json), warnings=json.loads(row.warnings_json), created_at=row.created_at) for row in rows]
