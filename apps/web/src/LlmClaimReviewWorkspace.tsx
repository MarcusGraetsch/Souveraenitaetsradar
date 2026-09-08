import { useEffect, useMemo, useState } from 'react'
import { api } from './api'
import { getGateUi } from './consultantTerminology'
import type {
  Assessment,
  Evidence,
  EvidenceReview,
  GateDefinition,
  LlmClaimImport,
  LlmClaimProposal,
  LlmClaimProposalReview,
  Question,
} from './types'

type ProposalRef={
  importRow:LlmClaimImport
  proposal:LlmClaimProposal
  proposalIndex:number
  review?:LlmClaimProposalReview
}

const reviewLabel=(review:LlmClaimProposalReview)=>{
  if(review.decision==='accepted')return 'übernommen'
  if(review.decision==='edited')return 'bearbeitet übernommen'
  return 'abgelehnt'
}

const evidenceReady=(review?:EvidenceReview)=>review?.review_status==='reviewed'||review?.review_status==='approved'

function FindingReviewCard({
  assessment,
  refRow,
  evidence,
  evidenceReviews,
  questions,
  gates,
  onChanged,
}:{
  assessment:Assessment
  refRow:ProposalRef
  evidence:Map<string,Evidence>
  evidenceReviews:Map<string,EvidenceReview>
  questions:Question[]
  gates:GateDefinition[]
  onChanged:()=>Promise<void>
}){
  const{importRow,proposal,proposalIndex,review}=refRow
  const[editing,setEditing]=useState(false)
  const[editedGate,setEditedGate]=useState(proposal.gate_id)
  const[editedStatement,setEditedStatement]=useState(proposal.statement)
  const[editedCapability,setEditedCapability]=useState(proposal.capability_level===null?'':String(proposal.capability_level))
  const[selectedEvidence,setSelectedEvidence]=useState<string[]>(proposal.evidence_ids)
  const[selectedQuestions,setSelectedQuestions]=useState<string[]>(proposal.question_ids)
  const[note,setNote]=useState('')
  const[busy,setBusy]=useState(false)
  const[message,setMessage]=useState('')

  useEffect(()=>{
    setEditing(false)
    setEditedGate(proposal.gate_id)
    setEditedStatement(proposal.statement)
    setEditedCapability(proposal.capability_level===null?'':String(proposal.capability_level))
    setSelectedEvidence(proposal.evidence_ids)
    setSelectedQuestions(proposal.question_ids)
    setNote('')
    setMessage('')
  },[importRow.id,proposalIndex,proposal])

  const originalGate=gates.find(item=>item.gate_id===proposal.gate_id)
  const editedGateDefinition=gates.find(item=>item.gate_id===editedGate)
  const gateUi=getGateUi(proposal.gate_id,originalGate?.name||proposal.gate_id,originalGate?.subject||'')
  const proposedLevelText=proposal.capability_level===null
    ?'nur Feststellung / noch kein Erfüllungsgrad'
    :originalGate?.capability_levels[proposal.capability_level]||`Stufe ${proposal.capability_level}`
  const unreviewedProposalEvidence=proposal.evidence_ids.filter(id=>!evidenceReady(evidenceReviews.get(id)))
  const selectedEvidenceReady=selectedEvidence.length>0&&selectedEvidence.every(id=>evidenceReady(evidenceReviews.get(id)))
  const canAccept=!review&&unreviewedProposalEvidence.length===0
  const canSaveEdit=!review&&editedStatement.trim().length>0&&selectedEvidenceReady&&selectedQuestions.length>0

  const toggleEvidence=(id:string)=>setSelectedEvidence(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id])
  const selectQuestions=(values:string[])=>setSelectedQuestions(values)

  const submit=async(decision:'accepted'|'edited'|'rejected')=>{
    setBusy(true);setMessage('')
    try{
      await api.reviewLlmClaimProposal(assessment.id,importRow.id,proposalIndex,decision==='edited'?{
        decision,
        gate_id:editedGate,
        statement:editedStatement,
        capability_level:editedCapability===''?null:Number(editedCapability),
        evidence_ids:selectedEvidence,
        question_ids:selectedQuestions,
        reviewer_note:note,
      }:{decision,reviewer_note:note})
      setMessage(decision==='rejected'?'Feststellungsvorschlag abgelehnt ✓':'Feststellung geprüft und gespeichert ✓')
      await onChanged()
    }catch(error){setMessage(`Prüfung fehlgeschlagen: ${String(error)}`)}finally{setBusy(false)}
  }

  return <article className="panel proposal-review-card">
    <div className="row-between">
      <div><div className="qid">{proposal.gate_id} · Import {importRow.id} · Vorschlag #{proposalIndex}</div><h3>{gateUi.name}</h3></div>
      {review?<span className={`badge badge-${review.decision==='rejected'?'needs_review':'applicable'}`}>{reviewLabel(review)}</span>:<span className="badge badge-needs_review">Prüfung offen</span>}
    </div>
    <div className="notice"><b>Vorgeschlagene Feststellung:</b> {proposal.statement}</div>
    <p><b>Vorgeschlagener Erfüllungsgrad:</b> {proposal.capability_level===null?'noch offen':`Stufe ${proposal.capability_level}`} · {proposedLevelText}</p>
    <p><b>Begründung des Modells:</b> {proposal.rationale}</p>
    <p className="muted"><b>Modell-Selbsteinschätzung:</b> {Math.round(proposal.confidence*100)} % · Diese Zahl ist keine Belegstärke und kein Radar-Trust.</p>

    <h4>Referenzierte Nachweise</h4>
    {proposal.evidence_ids.map(id=>{const item=evidence.get(id);const evidenceReview=evidenceReviews.get(id);return <div className="evidence-request" key={id}><b>{item?.title||'Unbekannter Nachweis'}</b><p>{item?.description||'—'}</p><small>{evidenceReady(evidenceReview)?`geprüft · Belegstärke ${evidenceReview?.effective_trust??0}`:`noch nicht geprüft/freigegeben`} · {id}</small></div>})}
    {unreviewedProposalEvidence.length>0&&!review&&<div className="warning">Direkte Übernahme ist gesperrt. Bitte zuerst die referenzierten Nachweise unter „Nachweise“ prüfen oder den Vorschlag bearbeiten und nur bereits geprüfte Nachweise verwenden.</div>}

    <h4>Verknüpfte Fragen</h4>
    <ul>{proposal.question_ids.map(id=>{const question=questions.find(item=>item.id===id);return <li key={id}><b>{id}</b> – {question?.question||'Frage nicht gefunden'}</li>})}</ul>

    {review?<>
      <p><b>Prüfergebnis:</b> {reviewLabel(review)}</p>
      {review.final_statement&&<p><b>Gespeicherte Feststellung:</b> {review.final_statement}</p>}
      {review.final_capability_level!==null&&<p><b>Gespeicherter Erfüllungsgrad:</b> Stufe {review.final_capability_level}</p>}
      {review.claim_id&&<p className="muted">Feststellungs-ID {review.claim_id}</p>}
      {review.reviewer_note&&<p><b>Prüfnotiz:</b> {review.reviewer_note}</p>}
    </>:<>
      {editing&&<section className="claim-edit-workspace">
        <label>K.O.-Kriterium<select value={editedGate} onChange={event=>{setEditedGate(event.target.value);setEditedCapability('')}}>{gates.map(gate=>{const ui=getGateUi(gate.gate_id,gate.name,gate.subject);return <option key={gate.gate_id} value={gate.gate_id}>{gate.gate_id} – {ui.name}</option>})}</select></label>
        <label>Bearbeitete Feststellung<textarea value={editedStatement} onChange={event=>setEditedStatement(event.target.value)}/></label>
        <label>Erfüllungsgrad<select value={editedCapability} onChange={event=>setEditedCapability(event.target.value)}><option value="">nur Feststellung / noch kein Erfüllungsgrad</option>{[0,1,2,3,4].map(level=><option key={level} value={level}>Stufe {level} – {editedGateDefinition?.capability_levels[level]||'Methodenbeschreibung nicht verfügbar'}</option>)}</select></label>
        <label>Verknüpfte Fragen<select multiple size={6} value={selectedQuestions} onChange={event=>selectQuestions(Array.from(event.currentTarget.selectedOptions).map(option=>option.value))}>{questions.filter(question=>question.applicability_status!=='not_applicable'||proposal.question_ids.includes(question.id)).map(question=><option key={question.id} value={question.id}>{question.id} – {question.question}</option>)}</select><small>Mehrfachauswahl mit Strg/Cmd. Die Fragetexte sind führend; IDs bleiben nur für die Auditspur sichtbar.</small></label>
        <fieldset><legend>Stützende, bereits geprüfte Nachweise</legend>{Array.from(evidence.values()).map(item=>{const evidenceReview=evidenceReviews.get(item.id);const ready=evidenceReady(evidenceReview);return <label className="check-row" key={item.id}><input type="checkbox" disabled={!ready} checked={selectedEvidence.includes(item.id)} onChange={()=>toggleEvidence(item.id)}/><span><b>{item.title}</b><small>{ready?`geprüft · Belegstärke ${evidenceReview?.effective_trust??0}`:'noch nicht geprüft – nicht auswählbar'}</small></span></label>})}</fieldset>
        {!selectedEvidenceReady&&<div className="warning">Mindestens ein geprüfter/freigegebener Nachweis ist erforderlich.</div>}
      </section>}
      <label>Prüfnotiz (optional)<textarea value={note} onChange={event=>setNote(event.target.value)} placeholder="Warum wurde übernommen, geändert oder abgelehnt?"/></label>
      <div className="action-row">
        <button className="primary" disabled={!canAccept||busy} onClick={()=>void submit('accepted')}>Übernehmen</button>
        <button disabled={busy} onClick={()=>setEditing(value=>!value)}>{editing?'Bearbeiten schließen':'Bearbeiten'}</button>
        {editing&&<button className="primary" disabled={!canSaveEdit||busy} onClick={()=>void submit('edited')}>Bearbeitet übernehmen</button>}
        <button className="danger-button" disabled={busy} onClick={()=>void submit('rejected')}>Ablehnen</button>
      </div>
    </>}
    {message&&<p className={message.startsWith('Prüfung fehlgeschlagen')?'warning':'save-message'}>{message}</p>}
  </article>
}

export function LlmClaimReviewWorkspace({assessment}:{assessment:Assessment}){
  const[prompt,setPrompt]=useState('')
  const[raw,setRaw]=useState('')
  const[imports,setImports]=useState<LlmClaimImport[]>([])
  const[reviews,setReviews]=useState<LlmClaimProposalReview[]>([])
  const[evidence,setEvidence]=useState<Evidence[]>([])
  const[evidenceReviews,setEvidenceReviews]=useState<EvidenceReview[]>([])
  const[questions,setQuestions]=useState<Question[]>([])
  const[gates,setGates]=useState<GateDefinition[]>([])
  const[message,setMessage]=useState('')
  const[loading,setLoading]=useState(true)

  const load=async()=>{
    setLoading(true)
    try{
      const[i,r,e,er,q,g]=await Promise.all([
        api.llmClaimImports(assessment.id),
        api.llmClaimProposalReviews(assessment.id),
        api.evidence(assessment.id),
        api.evidenceReviews(assessment.id),
        api.assessmentQuestions(assessment.id,'all'),
        api.hardGates(),
      ])
      setImports(i);setReviews(r);setEvidence(e);setEvidenceReviews(er);setQuestions(q);setGates(g)
    }finally{setLoading(false)}
  }
  useEffect(()=>{void load()},[assessment.id])

  const reviewMap=useMemo(()=>new Map(reviews.map(review=>[`${review.llm_claim_import_id}:${review.proposal_index}`,review])),[reviews])
  const evidenceMap=useMemo(()=>new Map(evidence.map(item=>[item.id,item])),[evidence])
  const evidenceReviewMap=useMemo(()=>new Map(evidenceReviews.map(item=>[item.evidence_id,item])),[evidenceReviews])
  const proposalRows=useMemo(()=>imports.flatMap(importRow=>importRow.proposals.map((proposal,proposalIndex)=>({importRow,proposal,proposalIndex,review:reviewMap.get(`${importRow.id}:${proposalIndex}`)}))),[imports,reviewMap])
  const pending=proposalRows.filter(row=>!row.review).length

  const generate=async()=>{const result=await api.claimPrompt(assessment.id);setPrompt(result.prompt);setMessage(`Feststellungs-Prompt ${result.prompt_version} erzeugt ✓`)}
  const copy=async()=>{await navigator.clipboard.writeText(prompt);setMessage('Feststellungs-Prompt kopiert ✓')}
  const importResult=async()=>{try{await api.importLlmClaims(assessment.id,raw);setRaw('');setMessage('LLM-Feststellungsvorschläge validiert und gespeichert ✓');await load()}catch(error){setMessage(`Import abgelehnt: ${String(error)}`)}}

  const gaps=imports.flatMap(item=>item.evidence_gaps.map(gap=>({importId:item.id,...gap})))
  const warnings=imports.flatMap(item=>item.warnings.map(warning=>({importId:item.id,warning})))

  return <section className="llm-claim-review-workspace">
    <div className="row-between"><div><h2>KI-Feststellungsvorschläge prüfen</h2><p className="muted">Die KI bereitet mögliche geprüfte Feststellungen für K.O.-Kriterien vor. Ein Import allein verändert keine Feststellung und kein Gate. Erst „Übernehmen“ oder „Bearbeitet übernehmen“ erzeugt eine human-geprüfte Feststellung.</p></div><span className="status">{pending} offen</span></div>
    <div className="two-col">
      <section className="panel"><h3>1. Feststellungs-Prompt</h3><button className="primary" onClick={()=>void generate()}>Feststellungs-Prompt erzeugen</button>{prompt&&<><textarea className="codebox" readOnly value={prompt}/><button onClick={()=>void copy()}>In Zwischenablage kopieren</button></>}</section>
      <section className="panel"><h3>2. LLM JSON für Feststellungen importieren</h3><textarea className="codebox" value={raw} onChange={event=>setRaw(event.target.value)} placeholder='{"assessment_id":"...","prompt_version":"claim-proposals-v1","method_version":"1.0","proposals":[]}'/><button className="primary" disabled={!raw.trim()} onClick={()=>void importResult()}>Validieren & als Feststellungsvorschläge speichern</button></section>
    </div>
    {message&&<p className={message.startsWith('Import abgelehnt')?'warning':'save-message'}>{message}</p>}
    {loading&&<p className="muted">Feststellungsvorschläge werden geladen…</p>}
    {!loading&&proposalRows.length===0&&<div className="notice">Noch keine importierten Feststellungsvorschläge vorhanden.</div>}
    {proposalRows.map(row=><FindingReviewCard key={`${row.importRow.id}:${row.proposalIndex}`} assessment={assessment} refRow={row} evidence={evidenceMap} evidenceReviews={evidenceReviewMap} questions={questions} gates={gates} onChanged={load}/>) }
    {gaps.length>0&&<section className="panel"><h3>Vom Modell erkannte Nachweislücken</h3>{gaps.map((gap,index)=>{const gate=gates.find(item=>item.gate_id===gap.gate_id);const ui=getGateUi(gap.gate_id,gate?.name||gap.gate_id,gate?.subject||'');return <div className="evidence-request" key={`${gap.importId}:${index}`}><b>{gap.gate_id} · {ui.name}</b><p>{gap.missing}</p><small>Verknüpfte Fragen: {gap.question_ids.map(id=>questions.find(item=>item.id===id)?.question||id).join(' · ')||'keine'}</small></div>})}</section>}
    {warnings.length>0&&<section className="panel"><h3>Hinweise des Modells</h3>{warnings.map((item,index)=><p className="warning" key={`${item.importId}:${index}`}>⚠ {item.warning}</p>)}</section>}
  </section>
}
