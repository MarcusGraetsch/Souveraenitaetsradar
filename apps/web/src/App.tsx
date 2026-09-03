import { FormEvent, useEffect, useMemo, useState } from 'react'
import { api } from './api'
import type {
  Answer,
  Assessment,
  Evidence,
  LlmImport,
  Question,
  RelevanceProfile,
} from './types'

const tabs = ['Übersicht', 'Relevanzprofil', 'Fragen', 'Evidence', 'LLM Bridge', 'Ergebnis'] as const
type Tab = typeof tabs[number]

export function App(){
  const [assessments,setAssessments]=useState<Assessment[]>([])
  const [selected,setSelected]=useState<Assessment|null>(null)
  const [tab,setTab]=useState<Tab>('Übersicht')
  const [error,setError]=useState('')

  const refresh=async()=>{
    try{
      setAssessments(await api.assessments())
      setError('')
    }catch(e){
      setError(String(e))
    }
  }
  useEffect(()=>{void refresh()},[])

  if(!selected){
    return <Dashboard assessments={assessments} refresh={refresh} select={setSelected} error={error}/>
  }

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand">Souveränitäts-Radar</div>
      <button className="back" onClick={()=>setSelected(null)}>← Assessments</button>
      <div className="assessment-title">{selected.name}</div>
      <div className="muted">{selected.customer||'Kein Kunde'}</div>
      <nav>
        {tabs.map(item=>
          <button key={item} className={tab===item?'active':''} onClick={()=>setTab(item)}>
            {item}
          </button>
        )}
      </nav>
    </aside>
    <main className="content">
      {tab==='Übersicht'&&<Overview assessment={selected}/>} 
      {tab==='Relevanzprofil'&&<RelevanceProfileTab assessment={selected}/>} 
      {tab==='Fragen'&&<Questions assessment={selected}/>} 
      {tab==='Evidence'&&<EvidenceTab assessment={selected}/>} 
      {tab==='LLM Bridge'&&<LlmBridge assessment={selected}/>} 
      {tab==='Ergebnis'&&<Result assessment={selected}/>} 
    </main>
  </div>
}

function Dashboard({assessments,refresh,select,error}:{assessments:Assessment[];refresh:()=>Promise<void>;select:(a:Assessment)=>void;error:string}){
  const [showForm,setShowForm]=useState(false)
  return <main className="dashboard">
    <div className="hero">
      <div>
        <h1>Souveränitäts-Radar</h1>
        <p>Cloud-agnostisches Beratungswerkzeug für nachvollziehbare Souveränitäts-Assessments.</p>
      </div>
      <button className="primary" onClick={()=>setShowForm(!showForm)}>+ Neues Assessment</button>
    </div>
    {error&&<div className="error">{error}</div>}
    {showForm&&<AssessmentForm onCreated={async()=>{setShowForm(false);await refresh()}}/>}
    <section className="panel">
      <h2>Assessments</h2>
      {assessments.length===0
        ? <p className="muted">Noch kein Assessment angelegt.</p>
        : <div className="cards">{assessments.map(a=><button className="assessment-card" key={a.id} onClick={()=>select(a)}><strong>{a.name}</strong><span>{a.customer||'—'}</span><span>{a.workload_type} · {a.criticality}</span><span className="status">{a.status}</span></button>)}</div>}
    </section>
  </main>
}

function AssessmentForm({onCreated}:{onCreated:()=>Promise<void>}){
  const [form,setForm]=useState({name:'',customer:'',description:'',workload_type:'saas',criticality:'medium',confidentiality:'medium',integrity:'medium',availability:'medium',control_region:'EU/EWR',regulatory_context:''})
  const submit=async(e:FormEvent)=>{e.preventDefault();await api.createAssessment(form);await onCreated()}
  return <form className="panel form-grid" onSubmit={submit}>
    <h2>Neues Assessment</h2>
    <label>Name<input required value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/></label>
    <label>Kunde<input value={form.customer} onChange={e=>setForm({...form,customer:e.target.value})}/></label>
    <label className="wide">Beschreibung<textarea value={form.description} onChange={e=>setForm({...form,description:e.target.value})}/></label>
    <label>Workload<select value={form.workload_type} onChange={e=>setForm({...form,workload_type:e.target.value})}><option value="application">Anwendung</option><option value="saas">SaaS</option><option value="cloud-platform">Cloud-Plattform</option><option value="ai-system">KI-System</option><option value="ai-agent">KI-Agent</option><option value="infrastructure">Infrastruktur</option><option value="other">Sonstiges</option></select></label>
    <SelectLabel label="Kritikalität" value={form.criticality} onChange={v=>setForm({...form,criticality:v})}/>
    <SelectLabel label="Vertraulichkeit" value={form.confidentiality} onChange={v=>setForm({...form,confidentiality:v})}/>
    <SelectLabel label="Integrität" value={form.integrity} onChange={v=>setForm({...form,integrity:v})}/>
    <SelectLabel label="Verfügbarkeit" value={form.availability} onChange={v=>setForm({...form,availability:v})}/>
    <label>Ziel-Kontrollraum<input value={form.control_region} onChange={e=>setForm({...form,control_region:e.target.value})}/></label>
    <label className="wide">Regulatorischer Kontext<input placeholder="z. B. NIS2, DSGVO" value={form.regulatory_context} onChange={e=>setForm({...form,regulatory_context:e.target.value})}/></label>
    <div className="wide"><button className="primary" type="submit">Assessment anlegen</button></div>
  </form>
}

function SelectLabel({label,value,onChange}:{label:string;value:string;onChange:(v:string)=>void}){
  return <label>{label}<select value={value} onChange={e=>onChange(e.target.value)}><option value="low">niedrig</option><option value="medium">mittel</option><option value="high">hoch</option><option value="critical">kritisch</option></select></label>
}

function Metric({label,value}:{label:string;value:string}){
  return <div className="metric"><span>{label}</span><strong>{value}</strong></div>
}

function Overview({assessment}:{assessment:Assessment}){
  return <><h1>{assessment.name}</h1><p className="lead">Assessment-Scope</p><div className="metric-grid"><Metric label="Kunde" value={assessment.customer||'—'}/><Metric label="Workload" value={assessment.workload_type}/><Metric label="Kritikalität" value={assessment.criticality}/><Metric label="Kontrollraum" value={assessment.control_region}/></div><section className="panel"><h2>Schutzbedarf</h2><p>C: <b>{assessment.confidentiality}</b> · I: <b>{assessment.integrity}</b> · A: <b>{assessment.availability}</b></p><p>{assessment.description||'Noch keine Beschreibung.'}</p><p className="muted">{assessment.regulatory_context||'Kein regulatorischer Kontext erfasst.'}</p></section><section className="notice"><b>Empfohlener nächster Schritt:</b> Relevanzprofil prüfen. Daraus erzeugt der Radar einen konservativen Fragenpfad. Unklare Bedingungen bleiben sichtbar und werden nicht automatisch weggefiltert.</section></>
}

function TriStateSelect({label,value,onChange,help}:{label:string;value:boolean|null;onChange:(value:boolean|null)=>void;help?:string}){
  const encoded=value===null?'unknown':value?'yes':'no'
  return <label>{label}<select value={encoded} onChange={e=>onChange(e.target.value==='unknown'?null:e.target.value==='yes')}><option value="unknown">noch unklar</option><option value="yes">ja</option><option value="no">nein</option></select>{help&&<small className="muted">{help}</small>}</label>
}

function RelevanceProfileTab({assessment}:{assessment:Assessment}){
  const [profile,setProfile]=useState<RelevanceProfile|null>(null)
  const [message,setMessage]=useState('')
  useEffect(()=>{void api.profile(assessment.id).then(setProfile)},[assessment.id])
  if(!profile)return <p>Lade Relevanzprofil…</p>
  const setBool=(field:keyof RelevanceProfile,value:boolean|null)=>setProfile({...profile,[field]:value})
  const save=async()=>{const saved=await api.saveProfile(assessment.id,profile);setProfile(saved);setMessage('Relevanzprofil gespeichert ✓');setTimeout(()=>setMessage(''),1500)}
  return <>
    <h1>Relevanzprofil</h1>
    <p className="lead">Diese wenigen Scope-Fakten steuern den Fragenpfad. „Noch unklar“ führt bewusst zu <b>Prüfen</b>, nicht zum unsichtbaren Wegfiltern.</p>
    <section className="panel form-grid">
      <h2>Technischer / vertraglicher Scope</h2>
      <label>Service-Modell<select value={profile.service_model} onChange={e=>setProfile({...profile,service_model:e.target.value as RelevanceProfile['service_model']})}><option value="unknown">noch unklar</option><option value="saas">SaaS</option><option value="paas">PaaS</option><option value="iaas">IaaS</option><option value="managed-service">Managed Service</option><option value="on-prem">On-Prem / selbst betrieben</option><option value="other">Sonstiges</option></select></label>
      <TriStateSelect label="Cloud-Service?" value={profile.cloud_service} onChange={v=>setBool('cloud_service',v)}/>
      <TriStateSelect label="Vertrag / Leistungsbeziehung im Scope?" value={profile.contract_in_scope} onChange={v=>setBool('contract_in_scope',v)}/>
      <TriStateSelect label="Datenverarbeitung?" value={profile.data_processing} onChange={v=>setBool('data_processing',v)}/>
      <TriStateSelect label="Persistente Daten / Speicherung?" value={profile.persistent_data} onChange={v=>setBool('persistent_data',v)}/>
      <TriStateSelect label="Verschlüsselung relevant/eingesetzt?" value={profile.encryption_used} onChange={v=>setBool('encryption_used',v)}/>
      <label>Schlüsselmodell<select value={profile.key_model} onChange={e=>setProfile({...profile,key_model:e.target.value as RelevanceProfile['key_model']})}><option value="unknown">noch unklar</option><option value="customer">kundenseitig kontrolliert</option><option value="provider">providerseitig</option><option value="external">externer Key-Service</option><option value="mixed">gemischt</option><option value="none">keine Schlüssel im Scope</option></select></label>
      <TriStateSelect label="Internet-exponiert?" value={profile.internet_exposed} onChange={v=>setBool('internet_exposed',v)}/>
    </section>
    <section className="panel form-grid">
      <h2>KI, Betrieb und Abhängigkeiten</h2>
      <TriStateSelect label="KI wird eingesetzt?" value={profile.ai_used} onChange={v=>setBool('ai_used',v)}/>
      <TriStateSelect label="Generative / agentische KI?" value={profile.agentic_ai} onChange={v=>setBool('agentic_ai',v)}/>
      <TriStateSelect label="Exit / Portabilität relevant?" value={profile.exit_relevant} onChange={v=>setBool('exit_relevant',v)}/>
      <TriStateSelect label="Backup / Restore relevant?" value={profile.backup_relevant} onChange={v=>setBool('backup_relevant',v)}/>
      <TriStateSelect label="Mehrere Provider / Multi-Provider?" value={profile.multi_provider} onChange={v=>setBool('multi_provider',v)}/>
      <TriStateSelect label="Unterauftragnehmer / Subprocessor?" value={profile.subcontractors_used} onChange={v=>setBool('subcontractors_used',v)}/>
      <TriStateSelect label="IAM / Identitätsanker relevant?" value={profile.iam_relevant} onChange={v=>setBool('iam_relevant',v)}/>
      <TriStateSelect label="Logging / Monitoring relevant?" value={profile.logging_relevant} onChange={v=>setBool('logging_relevant',v)}/>
      <TriStateSelect label="C5 im Assessment relevant?" value={profile.c5_relevant} onChange={v=>setBool('c5_relevant',v)}/>
      <TriStateSelect label="C3A im Assessment relevant?" value={profile.c3a_relevant} onChange={v=>setBool('c3a_relevant',v)}/>
    </section>
    <button className="primary" onClick={save}>Relevanzprofil speichern</button>{message&&<span className="save-message">{message}</span>}
  </>
}

function Questions({assessment}:{assessment:Assessment}){
  const [questions,setQuestions]=useState<Question[]>([])
  const [answers,setAnswers]=useState<Answer[]>([])
  const [domain,setDomain]=useState('')
  const [view,setView]=useState<'relevant'|'all'>('relevant')
  useEffect(()=>{void Promise.all([api.assessmentQuestions(assessment.id,view),api.answers(assessment.id)]).then(([q,a])=>{setQuestions(q);setAnswers(a)})},[assessment.id,view])
  const domains=useMemo(()=>Array.from(new Set(questions.map(q=>q.domain))),[questions])
  const visible=domain?questions.filter(q=>q.domain===domain):questions
  const answerMap=useMemo(()=>new Map(answers.map(a=>[a.question_id,a])),[answers])
  const needsReview=questions.filter(q=>q.applicability_status==='needs_review').length
  const applicable=questions.filter(q=>q.applicability_status==='applicable').length
  const answered=questions.filter(q=>answerMap.get(q.id)?.answer_value).length
  const save=async(q:Question,value:string,comment:string)=>{const saved=await api.saveAnswer(assessment.id,q.id,{answer_value:value,comment,evidence_ids:answerMap.get(q.id)?.evidence_ids||[],review_state:'draft'});setAnswers(prev=>[...prev.filter(a=>a.question_id!==q.id),saved])}
  return <><h1>Fragen</h1><p className="lead">Der Standardpfad zeigt anwendbare und noch zu prüfende Fragen. Sicher nicht anwendbare Fragen werden nur in „Alle Fragen“ sichtbar.</p><div className="metric-grid"><Metric label="Aktiver Pfad" value={String(questions.length)}/><Metric label="Anwendbar" value={String(applicable)}/><Metric label="Zu prüfen" value={String(needsReview)}/><Metric label="Beantwortet" value={`${answered}/${questions.length}`}/></div><div className="toolbar toolbar-wrap"><div className="segmented"><button className={view==='relevant'?'active':''} onClick={()=>setView('relevant')}>Relevante Fragen</button><button className={view==='all'?'active':''} onClick={()=>setView('all')}>Alle Fragen</button></div><select value={domain} onChange={e=>setDomain(e.target.value)}><option value="">Alle Domänen</option>{domains.map(d=><option key={d}>{d}</option>)}</select></div><div className="question-list">{visible.map(q=><QuestionCard key={q.id} q={q} answer={answerMap.get(q.id)} onSave={save}/>)}</div></>
}

function QuestionCard({q,answer,onSave}:{q:Question;answer?:Answer;onSave:(q:Question,v:string,c:string)=>Promise<void>}){
  const [value,setValue]=useState(answer?.answer_value||'')
  const [comment,setComment]=useState(answer?.comment||'')
  const [saved,setSaved]=useState(false)
  useEffect(()=>{setValue(answer?.answer_value||'');setComment(answer?.comment||'')},[answer?.answer_value,answer?.comment])
  const status=q.applicability_status||'needs_review'
  const label=status==='applicable'?'anwendbar':status==='not_applicable'?'nicht anwendbar':'prüfen'
  return <article className={`question-card ${status==='not_applicable'?'excluded':''}`}><div className="question-meta"><span className="qid">{q.id} · {q.domain}</span><span className={`applicability-badge ${status}`}>{label}</span></div><h3>{q.question}</h3><p className="applicability-reason"><b>Anwendbarkeit:</b> {q.applicability_reason||q.applicability||'nicht spezifiziert'}</p><p className="muted">Methodenregel: {q.applicability||'—'} · Erwartete Evidence: {q.expected_evidence||'—'} · Min Trust: {q.min_trust||'—'}</p><select value={value} onChange={e=>setValue(e.target.value)}><option value="">— offen —</option><option value="fulfilled">erfüllt</option><option value="partial">teilweise</option><option value="not-fulfilled">nicht erfüllt</option><option value="unknown">unbekannt</option><option value="not-applicable">nicht anwendbar</option></select><textarea placeholder="Kommentar / Begründung" value={comment} onChange={e=>setComment(e.target.value)}/><button onClick={async()=>{await onSave(q,value,comment);setSaved(true);setTimeout(()=>setSaved(false),1200)}}>{saved?'Gespeichert ✓':'Speichern'}</button></article>
}

function EvidenceTab({assessment}:{assessment:Assessment}){
  const [items,setItems]=useState<Evidence[]>([])
  const [form,setForm]=useState({title:'',evidence_type:'document',description:'',source:'',source_date:'',content_excerpt:''})
  const [file,setFile]=useState<File|null>(null)
  const load=()=>api.evidence(assessment.id).then(setItems)
  useEffect(()=>{void load()},[assessment.id])
  const submit=async(e:FormEvent)=>{e.preventDefault();const fd=new FormData();Object.entries(form).forEach(([k,v])=>fd.set(k,v));if(file)fd.set('file',file);await api.addEvidence(assessment.id,fd);setForm({title:'',evidence_type:'document',description:'',source:'',source_date:'',content_excerpt:''});setFile(null);await load()}
  return <><h1>Evidence</h1><p className="lead">Dateien bleiben lokal. Die Anwendung analysiert im MVP keine Dokumentinhalte automatisch.</p><form className="panel form-grid" onSubmit={submit}><h2>Evidence hinzufügen</h2><label>Titel<input required value={form.title} onChange={e=>setForm({...form,title:e.target.value})}/></label><label>Typ<select value={form.evidence_type} onChange={e=>setForm({...form,evidence_type:e.target.value})}><option value="contract">Vertrag</option><option value="architecture">Architektur</option><option value="provider-doc">Provider-Dokumentation</option><option value="assurance">Audit/Assurance</option><option value="customer-statement">Kundenangabe</option><option value="technical-export">Technischer Export</option><option value="test">Testnachweis</option><option value="other">Sonstiges</option></select></label><label>Quelle<input value={form.source} onChange={e=>setForm({...form,source:e.target.value})}/></label><label>Stand<input value={form.source_date} onChange={e=>setForm({...form,source_date:e.target.value})}/></label><label className="wide">Beschreibung<textarea value={form.description} onChange={e=>setForm({...form,description:e.target.value})}/></label><label className="wide">Freigegebener Textauszug für LLM Bridge<textarea value={form.content_excerpt} onChange={e=>setForm({...form,content_excerpt:e.target.value})}/></label><label className="wide">Optionale Datei<input type="file" onChange={e=>setFile(e.target.files?.[0]||null)}/></label><div className="wide"><button className="primary">Evidence speichern</button></div></form><div className="cards">{items.map(i=><div className="panel" key={i.id}><div className="qid">{i.id}</div><h3>{i.title}</h3><p>{i.description}</p><p className="muted">{i.evidence_type} · {i.source||'keine Quelle'} · {i.file_name||'keine Datei'}</p></div>)}</div></>
}

function LlmBridge({assessment}:{assessment:Assessment}){
  const [prompt,setPrompt]=useState('')
  const [raw,setRaw]=useState('')
  const [imports,setImports]=useState<LlmImport[]>([])
  const [message,setMessage]=useState('')
  const loadImports=()=>api.llmImports(assessment.id).then(setImports)
  useEffect(()=>{void loadImports()},[assessment.id])
  const generate=async()=>setPrompt((await api.prompt(assessment.id)).prompt)
  const copy=async()=>{await navigator.clipboard.writeText(prompt);setMessage('Prompt kopiert ✓')}
  const importResult=async()=>{try{await api.importLlm(assessment.id,raw);setMessage('LLM-Ergebnis validiert und als Vorschlag gespeichert ✓');setRaw('');await loadImports()}catch(e){setMessage(`Import abgelehnt: ${String(e)}`)}}
  return <><h1>LLM Bridge</h1><p className="lead">Keine API-Verbindung. Der Prompt enthält nur relevante/zu prüfende offene Fragen aus dem Guided Workflow.</p><div className="two-col"><section className="panel"><h2>1. Prompt Package</h2><button className="primary" onClick={generate}>Prompt erzeugen</button>{prompt&&<><textarea className="codebox" readOnly value={prompt}/><button onClick={copy}>In Zwischenablage kopieren</button></>}</section><section className="panel"><h2>2. LLM JSON importieren</h2><textarea className="codebox" placeholder='{"assessment_id":"...","proposals":[]}' value={raw} onChange={e=>setRaw(e.target.value)}/><button className="primary" disabled={!raw.trim()} onClick={importResult}>Validieren & als Vorschlag speichern</button>{message&&<p>{message}</p>}</section></div><h2>Importierte Vorschläge</h2>{imports.length===0?<p className="muted">Noch keine LLM-Vorschläge importiert.</p>:imports.map(item=><section className="panel" key={item.id}><div className="qid">{item.created_at} · {item.validation_status}</div>{item.proposals.map((p,idx)=><div className="proposal" key={idx}><b>{p.question_id}: {p.proposed_answer}</b><p>{p.rationale}</p><small>Confidence {Math.round(p.confidence*100)}% · Evidence {p.evidence_ids.join(', ')||'keine'}</small></div>)}{item.evidence_gaps.map((g,idx)=><p key={idx}><b>Gap {g.question_id}:</b> {g.missing}</p>)}{item.warnings.map((w,idx)=><p className="warning" key={idx}>⚠ {w}</p>)}</section>)}</>
}

function Result({assessment}:{assessment:Assessment}){
  const [answers,setAnswers]=useState<Answer[]>([])
  const [imports,setImports]=useState<LlmImport[]>([])
  const [questions,setQuestions]=useState<Question[]>([])
  useEffect(()=>{void Promise.all([api.answers(assessment.id),api.llmImports(assessment.id),api.assessmentQuestions(assessment.id,'relevant')]).then(([a,i,q])=>{setAnswers(a);setImports(i);setQuestions(q)})},[assessment.id])
  const activeIds=new Set(questions.map(q=>q.id))
  const answered=answers.filter(a=>a.answer_value&&activeIds.has(a.question_id)).length
  const proposals=imports.reduce((n,i)=>n+i.proposals.length,0)
  const gaps=imports.reduce((n,i)=>n+i.evidence_gaps.length,0)
  const review=questions.filter(q=>q.applicability_status==='needs_review').length
  return <><h1>Ergebnis</h1><p className="lead">MVP-Statusübersicht. Hard-Gate-/Risikoauswertung folgt in NEXT-112.</p><div className="metric-grid"><Metric label="Aktive Fragen" value={String(questions.length)}/><Metric label="Beantwortet" value={`${answered}/${questions.length}`}/><Metric label="Applicability offen" value={String(review)}/><Metric label="LLM-Vorschläge" value={String(proposals)}/><Metric label="Evidence Gaps" value={String(gaps)}/><Metric label="Entscheidungsstatus" value="UNVERIFIED"/></div><section className="notice"><b>Governance:</b> LLM-Vorschläge sind keine automatisch übernommenen Antworten. Risikoakzeptanz, Legal-Schlussfolgerungen und finale Freigaben bleiben menschliche Entscheidungen.</section></>
}
