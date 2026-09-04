import { useEffect, useMemo, useState } from 'react'
import { api } from './api'
import { LlmClaimReviewWorkspace } from './LlmClaimReviewWorkspace'
import type {
  Assessment,
  Evidence,
  LlmImport,
  LlmProposal,
  LlmProposalReview,
  Question,
} from './types'

type ProposalRef={
  importRow:LlmImport
  proposal:LlmProposal
  proposalIndex:number
  question?:Question
  review?:LlmProposalReview
}

const applicabilityLabel=(question?:Question)=>{
  if(!question)return 'Frage nicht gefunden'
  if(question.applicability_status==='applicable')return 'anwendbar'
  if(question.applicability_status==='not_applicable')return 'nicht anwendbar'
  return 'Anwendbarkeit klären'
}

const reviewLabel=(review:LlmProposalReview)=>{
  if(review.decision==='accepted')return 'übernommen'
  if(review.decision==='edited')return 'bearbeitet übernommen'
  return 'abgelehnt'
}

function validForQuestion(question:Question|undefined,value:string){
  if(!question||!value.trim())return false
  const control=question.answer_control
  if(control.kind==='single_select')return control.options.some(option=>option.value===value)
  if(control.kind==='date')return /^\d{4}-\d{2}-\d{2}$/.test(value)
  return true
}

function ReviewAnswerInput({question,value,onChange}:{question:Question;value:string;onChange:(value:string)=>void}){
  const control=question.answer_control
  if(control.kind==='single_select')return <select value={value} onChange={event=>onChange(event.target.value)}><option value="">— auswählen —</option>{control.options.map(option=><option key={option.value} value={option.value}>{option.label}</option>)}</select>
  if(control.kind==='date')return <input type="date" value={value} onChange={event=>onChange(event.target.value)}/>
  return <textarea value={value} onChange={event=>onChange(event.target.value)} placeholder={control.placeholder||'Bearbeitete Antwort eingeben'}/>
}

function ProposalReviewCard({assessment,refRow,evidence,onChanged}:{assessment:Assessment;refRow:ProposalRef;evidence:Map<string,Evidence>;onChanged:()=>Promise<void>}){
  const{importRow,proposal,proposalIndex,question,review}=refRow
  const[editing,setEditing]=useState(false)
  const[editedValue,setEditedValue]=useState(proposal.proposed_answer)
  const[selectedEvidence,setSelectedEvidence]=useState<string[]>(proposal.evidence_ids)
  const[note,setNote]=useState('')
  const[busy,setBusy]=useState(false)
  const[message,setMessage]=useState('')
  useEffect(()=>{setEditedValue(proposal.proposed_answer);setSelectedEvidence(proposal.evidence_ids);setNote('');setEditing(false)},[importRow.id,proposalIndex,proposal.proposed_answer,proposal.evidence_ids])
  const applicabilityResolved=question?.applicability_status==='applicable'
  const originalFormatValid=validForQuestion(question,proposal.proposed_answer)
  const editedFormatValid=validForQuestion(question,editedValue)
  const canAccept=applicabilityResolved&&!review&&originalFormatValid
  const canEdit=applicabilityResolved&&!review
  const toggleEvidence=(id:string)=>setSelectedEvidence(prev=>prev.includes(id)?prev.filter(x=>x!==id):[...prev,id])
  const submit=async(decision:'accepted'|'edited'|'rejected')=>{
    setBusy(true);setMessage('')
    try{
      await api.reviewLlmProposal(assessment.id,importRow.id,proposalIndex,{
        decision,
        answer_value:decision==='edited'?editedValue:undefined,
        evidence_ids:decision==='rejected'?undefined:selectedEvidence,
        reviewer_note:note,
      })
      setMessage(decision==='rejected'?'Vorschlag abgelehnt ✓':'Vorschlag geprüft und als Radar-Antwort gespeichert ✓')
      await onChanged()
    }catch(error){setMessage(`Prüfung fehlgeschlagen: ${String(error)}`)}finally{setBusy(false)}
  }
  return <article className="panel proposal-review-card">
    <div className="row-between"><div><div className="qid">{proposal.question_id} · {question?.domain||'Unbekannte Domäne'}</div><h3>{question?.question||'Fragetext nicht verfügbar'}</h3></div>{review?<span className={`badge badge-${review.decision==='rejected'?'needs_review':'applicable'}`}>{reviewLabel(review)}</span>:<span className={`badge badge-${question?.applicability_status==='applicable'?'applicable':'needs_review'}`}>{applicabilityLabel(question)}</span>}</div>
    <div className="notice"><b>KI-Vorschlag:</b> {proposal.proposed_answer}</div>
    <p><b>Begründung des Modells:</b> {proposal.rationale||'—'}</p>
    <p className="muted"><b>Modell-Selbsteinschätzung:</b> {Math.round(proposal.confidence*100)} % · Diese Zahl ist keine Belegstärke und kein Radar-Trust.</p>
    <fieldset><legend>Vom Modell referenzierte Nachweise</legend>{proposal.evidence_ids.map(id=>{const item=evidence.get(id);return <label className="check-row" key={id}><input type="checkbox" disabled={!!review||busy} checked={selectedEvidence.includes(id)} onChange={()=>toggleEvidence(id)}/><span><b>{item?.title||'Nachweis'}</b><small>{id}</small></span></label>})}</fieldset>
    {question?.applicability_status!=='applicable'&&!review&&<div className="warning">Die Anwendbarkeit dieser Frage ist noch nicht positiv geklärt. Übernehmen ist deshalb gesperrt. Bitte zuerst das Relevanzprofil bzw. die Anwendbarkeit klären. Ablehnen bleibt möglich.</div>}
    {question&&applicabilityResolved&&!originalFormatValid&&!review&&<div className="warning">Der KI-Vorschlag passt nicht zum Antwortformat „{question.answer_type}“. Eine direkte Übernahme ist gesperrt. Bitte „Bearbeiten“ wählen und einen gültigen Wert festlegen.</div>}
    {review?<><p><b>Prüfergebnis:</b> {reviewLabel(review)}</p>{review.final_answer_value&&<p><b>Gespeicherte Radar-Antwort:</b> {review.final_answer_value}</p>}{review.reviewer_note&&<p><b>Prüfnotiz:</b> {review.reviewer_note}</p>}<p className="muted">Review-ID {review.id} · Import {review.llm_import_id} · Proposal #{review.proposal_index}</p></>:<>
      {editing&&question&&<label>Bearbeitete Antwort<ReviewAnswerInput question={question} value={editedValue} onChange={setEditedValue}/></label>}
      <label>Prüfnotiz (optional)<textarea value={note} onChange={event=>setNote(event.target.value)} placeholder="Warum wurde übernommen, geändert oder abgelehnt?" /></label>
      <div className="action-row"><button className="primary" disabled={!canAccept||busy} onClick={()=>void submit('accepted')}>Übernehmen</button><button disabled={!canEdit||busy} onClick={()=>setEditing(value=>!value)}>{editing?'Bearbeiten schließen':'Bearbeiten'}</button>{editing&&<button className="primary" disabled={!canEdit||busy||!editedFormatValid} onClick={()=>void submit('edited')}>Bearbeitet übernehmen</button>}<button className="danger-button" disabled={busy} onClick={()=>void submit('rejected')}>Ablehnen</button></div>
    </>}
    {message&&<p className={message.startsWith('Prüfung fehlgeschlagen')?'warning':'save-message'}>{message}</p>}
  </article>
}

export function LlmReviewWorkspace({assessment}:{assessment:Assessment}){
  const[imports,setImports]=useState<LlmImport[]>([])
  const[reviews,setReviews]=useState<LlmProposalReview[]>([])
  const[questions,setQuestions]=useState<Question[]>([])
  const[evidence,setEvidence]=useState<Evidence[]>([])
  const[loading,setLoading]=useState(true)
  const[error,setError]=useState('')
  const load=async()=>{setLoading(true);try{const[i,r,q,e]=await Promise.all([api.llmImports(assessment.id),api.llmProposalReviews(assessment.id),api.assessmentQuestions(assessment.id,'all'),api.evidence(assessment.id)]);setImports(i);setReviews(r);setQuestions(q);setEvidence(e);setError('')}catch(err){setError(String(err))}finally{setLoading(false)}}
  useEffect(()=>{void load()},[assessment.id])
  const questionMap=useMemo(()=>new Map(questions.map(question=>[question.id,question])),[questions])
  const evidenceMap=useMemo(()=>new Map(evidence.map(item=>[item.id,item])),[evidence])
  const reviewMap=useMemo(()=>new Map(reviews.map(review=>[`${review.llm_import_id}:${review.proposal_index}`,review])),[reviews])
  const proposalRows=useMemo(()=>imports.flatMap(importRow=>importRow.proposals.map((proposal,proposalIndex)=>({importRow,proposal,proposalIndex,question:questionMap.get(proposal.question_id),review:reviewMap.get(`${importRow.id}:${proposalIndex}`)}))),[imports,questionMap,reviewMap])
  const pending=proposalRows.filter(row=>!row.review).length
  return <>
    <section><div className="row-between"><div><h2>KI-Antwortvorschläge prüfen</h2><p className="muted">LLM-Vorschläge werden erst durch Ihre Prüfung zu Radar-Antworten. Die ursprüngliche LLM-Ausgabe bleibt unverändert auditierbar.</p></div><span className="status">{pending} offen</span></div>{loading&&<p className="muted">Vorschläge werden geladen…</p>}{error&&<div className="error">{error}</div>}{!loading&&proposalRows.length===0&&<div className="notice">Noch keine importierten Antwortvorschläge vorhanden.</div>}{proposalRows.map(row=><ProposalReviewCard key={`${row.importRow.id}:${row.proposalIndex}`} assessment={assessment} refRow={row} evidence={evidenceMap} onChanged={load}/>)}</section>
    <LlmClaimReviewWorkspace assessment={assessment}/>
  </>
}
