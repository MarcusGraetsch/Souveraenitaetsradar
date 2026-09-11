import { FormEvent, ReactNode, useState } from 'react'

type Tri='yes'|'no'|'unknown'
type LegalEntity={name:string;country:string;city:string;postal_code:string;role:string}
type Candidate={framework:string;candidate_status:string;rationale:string[];missing_facts:string[];disclaimer:string}
type IntakeResult={assessment_id:string;pre_assessment:{workload_tags:string[];compliance_candidates:Candidate[];missing_scope_facts:string[];suggested_deep_dive_profiles:string[];suggested_screening_focus:string[];jurisdiction_complexity:string[]}}

const archetypes=[
  ['business-application','Fachanwendung / Business Application'],
  ['saas','SaaS-Anwendung'],
  ['data-analytics','Daten-/Analyseplattform'],
  ['integration-api','Integrations-/API-Service'],
  ['cloud-platform','Cloud-/Plattformdienst'],
  ['ai-system','KI-System'],
  ['ai-agent','KI-Agent / agentisches System'],
  ['devops-platform','Entwicklungs-/CI-CD-/DevOps-Plattform'],
  ['iam-trust','Identitäts-/IAM-/Trust-Service'],
  ['database-storage','Datenbank-/Storage-Service'],
  ['infrastructure-compute','Infrastruktur-/Compute-Plattform'],
  ['collaboration','End-User-/Collaboration-Service'],
  ['ot-iot-edge','OT/IoT/Edge-System'],
  ['other','Sonstiges'],
] as const

const sectors=[
  ['public-administration','Öffentliche Verwaltung'],
  ['energy','Energie'],
  ['transport-logistics','Verkehr / Logistik'],
  ['banking-financial','Banken / Finanzdienstleistungen / Versicherungen'],
  ['financial-market-infrastructure','Finanzmarktinfrastruktur'],
  ['health','Gesundheitswesen'],
  ['water-wastewater','Trinkwasser / Abwasser'],
  ['digital-infrastructure','Digitale Infrastruktur / Rechenzentrum / Telekommunikation'],
  ['ict-managed-services','IT-/ICT-Dienstleistungen / Managed Services'],
  ['space','Weltraum'],
  ['postal-courier','Post / Kurier'],
  ['waste-management','Abfallwirtschaft'],
  ['chemicals','Chemie'],
  ['food','Lebensmittel'],
  ['manufacturing','Produktion / Herstellung'],
  ['digital-services','Digitale Dienste / Online-Plattformen'],
  ['research-education','Forschung / Bildung'],
  ['retail-trade','Handel'],
  ['construction-real-estate','Bau / Immobilien'],
  ['professional-services','Beratung / professionelle Dienstleistungen'],
  ['other','Sonstiges'],
] as const

const tags=[
  {value:'ai',label:'KI im Einsatz'},
  {value:'agentic',label:'Agentisches KI-System / KI-Agent'},
  {value:'internet_exposed',label:'Aus dem Internet erreichbar'},
  {value:'customer_facing',label:'Kunden-/Bürgerkontakt'},
  {value:'internal',label:'Interne Nutzung'},
  {value:'data_intensive',label:'Datenintensiver Workload'},
  {value:'identity_critical',label:'Identitäts-/Berechtigungskritisch'},
  {value:'real_time',label:'Echtzeit- / zeitkritisch'},
  {value:'regulated_process',label:'Regulierter / hoheitlicher Prozess'},
  {value:'multi_provider',label:'Mehrere Provider / Multi-Cloud'},
] as const

const frameworkLabels:Record<string,string>={GDPR:'DSGVO',NIS2:'NIS2',DORA:'DORA',AI_ACT:'EU AI Act / KI-Verordnung'}
const statusLabels:Record<string,string>={likely_applicable:'wahrscheinlich anwendbar',likely_not_applicable:'wahrscheinlich nicht anwendbar',needs_review:'Prüfung erforderlich'}
const stepTitles=['Entscheidungsfall','Organisation','Workload & Beteiligte','Prüfen & Speichern']

const overlay:React.CSSProperties={position:'fixed',inset:0,background:'rgba(15,23,42,.64)',zIndex:1000,overflow:'auto',padding:'4vh 3vw'}
const modal:React.CSSProperties={maxWidth:1000,margin:'0 auto',background:'#fff',borderRadius:16,padding:24,boxShadow:'0 24px 80px rgba(0,0,0,.25)'}
const steps:React.CSSProperties={display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:8,margin:'16px 0 24px'}
const stepStyle=(active:boolean):React.CSSProperties=>({padding:'10px 12px',borderRadius:10,background:active?'#e2e8f0':'#f8fafc',fontWeight:active?700:500,fontSize:14})
const grid:React.CSSProperties={display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(240px,1fr))',gap:14}
const full:React.CSSProperties={gridColumn:'1 / -1'}
const row:React.CSSProperties={display:'flex',gap:10,flexWrap:'wrap',alignItems:'center'}
const box:React.CSSProperties={border:'1px solid #e2e8f0',borderRadius:12,padding:14,marginTop:12}
const footer:React.CSSProperties={position:'sticky',bottom:0,display:'flex',justifyContent:'space-between',gap:12,margin:'24px -24px -24px',padding:'16px 24px',background:'#fff',borderTop:'1px solid #e2e8f0',borderRadius:'0 0 16px 16px'}

function Field({label,children,wide=false,help=''}:{label:string;children:ReactNode;wide?:boolean;help?:string}){
  return <label style={wide?full:undefined}><span style={{display:'block',fontWeight:600,marginBottom:6}}>{label}</span>{children}{help&&<small className="muted" style={{display:'block',marginTop:6}}>{help}</small>}</label>
}
function Text({value,onChange,required=false,placeholder=''}:{value:string;onChange:(v:string)=>void;required?:boolean;placeholder?:string}){
  return <input style={{width:'100%'}} required={required} value={value} placeholder={placeholder} onChange={e=>onChange(e.target.value)}/>
}
function Select({value,onChange,children}:{value:string;onChange:(v:string)=>void;children:ReactNode}){
  return <select style={{width:'100%'}} value={value} onChange={e=>onChange(e.target.value)}>{children}</select>
}

export function AssessmentIntakeShell({children}:{children:ReactNode}){
  const[open,setOpen]=useState(false)
  const intercept=(e:React.MouseEvent<HTMLDivElement>)=>{
    const target=e.target as HTMLElement
    const button=target.closest('button')
    if(button?.textContent?.includes('Neues Assessment')){
      e.preventDefault();e.stopPropagation();setOpen(true)
    }
  }
  return <div onClickCapture={intercept}>{children}{open&&<AssessmentIntakeWizard onClose={()=>setOpen(false)}/>}</div>
}

function AssessmentIntakeWizard({onClose}:{onClose:()=>void}){
  const[step,setStep]=useState(0)
  const[result,setResult]=useState<IntakeResult|null>(null)
  const[error,setError]=useState('')
  const[saving,setSaving]=useState(false)
  const[decision,setDecision]=useState({title:'',objective:'',project_reference:'',consultant_owner:'',target_decision_date:''})
  const[org,setOrg]=useState({
    name:'',organization_type:'company',sector:'',sector_detail:'',employee_size:'unknown',
    headquarters_country:'Deutschland',headquarters_city:'',headquarters_postal_code:'',headquarters_street:'',
    activity_countries:[] as string[],group_structure:'unknown' as Tri,annual_revenue_eur:'',balance_sheet_eur:''
  })
  const[entities,setEntities]=useState<LegalEntity[]>([{name:'',country:'Deutschland',city:'',postal_code:'',role:'primary'}])
  const[workload,setWorkload]=useState({
    name:'',description:'',primary_archetype:'business-application',tags:[] as string[],personal_data:'unknown' as Tri,
    sensitive_business_data:'unknown' as Tri,ai_used:'unknown' as Tri,ai_role:'unknown',external_provider_in_scope:'unknown' as Tri,
    current_operating_model:'unknown',user_countries:[] as string[],legal_entity_names:[] as string[]
  })

  const syncPrimary=()=>setEntities(current=>current.map((item,i)=>i===0?{
    ...item,
    name:item.name||org.name,
    country:item.country||org.headquarters_country,
    city:item.city||org.headquarters_city,
    postal_code:item.postal_code||org.headquarters_postal_code,
  }:item))
  const sectorComplete=Boolean(org.sector&&org.sector!=='other'||org.sector==='other'&&org.sector_detail.trim())
  const canNext=step===0
    ?Boolean(decision.title.trim()&&decision.objective.trim())
    :step===1
      ?Boolean(org.name.trim()&&sectorComplete&&org.headquarters_country.trim()&&org.headquarters_city.trim())
      :step===2
        ?Boolean(workload.name.trim()&&workload.description.trim()&&workload.primary_archetype&&entities[0]?.name.trim()&&entities[0]?.country.trim())
        :true
  const next=()=>{if(step===1)syncPrimary();if(canNext)setStep(Math.min(3,step+1))}
  const toggleTag=(tag:string)=>setWorkload(w=>({...w,tags:w.tags.includes(tag)?w.tags.filter(x=>x!==tag):[...w.tags,tag]}))
  const updateEntity=(i:number,key:keyof LegalEntity,value:string)=>setEntities(rows=>rows.map((r,index)=>index===i?{...r,[key]:value}:r))

  const submit=async(e:FormEvent)=>{
    e.preventDefault()
    if(step!==3||result)return
    setError('');setSaving(true)
    const payload={
      decision_case:decision,
      organization:{...org,legal_entities:entities},
      workload:{...workload,legal_entity_names:entities.map(x=>x.name).filter(Boolean)},
    }
    try{
      const response=await fetch('/api/assessment-intakes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
      if(!response.ok)throw new Error(await response.text())
      setResult(await response.json() as IntakeResult)
    }catch(err){setError(String(err))}finally{setSaving(false)}
  }

  return <div style={overlay} role="dialog" aria-modal="true"><form style={modal} onSubmit={submit}>
    <div style={{display:'flex',justifyContent:'space-between',gap:16,alignItems:'start'}}>
      <div><h2 style={{margin:0}}>Neues Assessment · Intake v0.5</h2><p className="muted">Fakten zuerst. Kritikalität, C/I/A und Rechtsanwendbarkeit werden hier nicht vorweggenommen.</p></div>
      <button type="button" onClick={onClose}>Schließen</button>
    </div>

    <div style={steps}>{stepTitles.map((title,i)=><div key={title} style={stepStyle(step===i)}>{i+1}. {title}</div>)}</div>
    {error&&<div className="error">{error}</div>}

    {step===0&&<div style={grid}>
      <Field label="Titel des Entscheidungsfalls" wide help="Ein sprechender Name für die konkrete Entscheidung, nicht nur Kunden- oder Projektname."><Text required value={decision.title} onChange={v=>setDecision({...decision,title:v})} placeholder="z. B. Betriebsmodell KI-Assistent Bürgerdienste"/></Field>
      <Field label="Entscheidungsfrage / Ziel" wide><textarea required style={{width:'100%',minHeight:100}} value={decision.objective} onChange={e=>setDecision({...decision,objective:e.target.value})} placeholder="Welche Betriebsvariante bietet ausreichende Souveränität bei vertretbarem Aufwand?"/></Field>
      <Field label="Projekt-/Aktenzeichen"><Text value={decision.project_reference} onChange={v=>setDecision({...decision,project_reference:v})}/></Field>
      <Field label="Consultant / Owner"><Text value={decision.consultant_owner} onChange={v=>setDecision({...decision,consultant_owner:v})}/></Field>
    </div>}

    {step===1&&<>
      <div style={grid}>
        <Field label="Organisation / Kunde"><Text required value={org.name} onChange={v=>setOrg({...org,name:v})}/></Field>
        <Field label="Organisationstyp"><Select value={org.organization_type} onChange={v=>setOrg({...org,organization_type:v})}><option value="company">Unternehmen</option><option value="public_authority">Behörde</option><option value="public_body">Sonstige öffentliche Stelle</option><option value="non_profit">Non-Profit</option><option value="other">Sonstiges</option></Select></Field>
        <Field label="Primärer Sektor" help="Routing-Hilfe, keine rechtliche Klassifikation."><Select value={org.sector} onChange={v=>setOrg({...org,sector:v})}><option value="">Bitte auswählen</option>{sectors.map(([v,l])=><option key={v} value={v}>{l}</option>)}</Select></Field>
        <Field label="Tätigkeit / Zusatzinfo" help={org.sector==='other'?'Bei „Sonstiges“ bitte ausfüllen.':'Optional: Tätigkeit genauer beschreiben, z. B. kommunaler Netzbetreiber oder Softwarehersteller.'}><Text required={org.sector==='other'} value={org.sector_detail} onChange={v=>setOrg({...org,sector_detail:v})} placeholder="z. B. kommunaler Stromnetzbetreiber"/></Field>
        <Field label="Größenklasse"><Select value={org.employee_size} onChange={v=>setOrg({...org,employee_size:v})}><option value="unknown">noch unklar</option><option value="micro">Mikro</option><option value="small">klein</option><option value="medium">mittel</option><option value="large">groß</option></Select></Field>
        <Field label="Sitzland"><Text required value={org.headquarters_country} onChange={v=>setOrg({...org,headquarters_country:v})}/></Field>
        <Field label="Ort"><Text required value={org.headquarters_city} onChange={v=>setOrg({...org,headquarters_city:v})}/></Field>
        <Field label="Postleitzahl"><Text value={org.headquarters_postal_code} onChange={v=>setOrg({...org,headquarters_postal_code:v})}/></Field>
        <Field label="Straße (optional)"><Text value={org.headquarters_street} onChange={v=>setOrg({...org,headquarters_street:v})}/></Field>
      </div>
      <div className="notice" style={{marginTop:16}}><b>Konzern-/Gruppenstruktur:</b> wird hier nicht pauschal mit Ja/Nein abgefragt. Wenn für den Workload mehrere juristische Einheiten relevant sind, werden sie im nächsten Schritt konkret erfasst.</div>
    </>}

    {step===2&&<>
      <div style={grid}>
        <Field label="Workload-Name"><Text required value={workload.name} onChange={v=>setWorkload({...workload,name:v})}/></Field>
        <Field label="Primärer Workload-Archetyp"><Select value={workload.primary_archetype} onChange={v=>setWorkload({...workload,primary_archetype:v})}>{archetypes.map(([v,l])=><option key={v} value={v}>{l}</option>)}</Select></Field>
        <Field label="Beschreibung in natürlicher Sprache" wide><textarea required style={{width:'100%',minHeight:120}} value={workload.description} onChange={e=>setWorkload({...workload,description:e.target.value})} placeholder="Was macht der Workload, wer nutzt ihn, welche Daten und Systeme sind beteiligt?"/></Field>
        <Field label="Personenbezogene Daten?"><Select value={workload.personal_data} onChange={v=>setWorkload({...workload,personal_data:v as Tri})}><option value="unknown">noch unklar</option><option value="yes">ja</option><option value="no">nein</option></Select></Field>
        <Field label="Sensible Fach-/Geschäftsdaten?"><Select value={workload.sensitive_business_data} onChange={v=>setWorkload({...workload,sensitive_business_data:v as Tri})}><option value="unknown">noch unklar</option><option value="yes">ja</option><option value="no">nein</option></Select></Field>
        <Field label="KI eingesetzt?"><Select value={workload.ai_used} onChange={v=>setWorkload({...workload,ai_used:v as Tri})}><option value="unknown">noch unklar</option><option value="yes">ja</option><option value="no">nein</option></Select></Field>
        <Field label="Aktuelles Betriebsmodell"><Select value={workload.current_operating_model} onChange={v=>setWorkload({...workload,current_operating_model:v})}><option value="unknown">noch unklar</option><option value="on-prem">On-Prem</option><option value="private-cloud">Private Cloud</option><option value="public-cloud">Public Cloud</option><option value="saas">SaaS</option><option value="hybrid">Hybrid</option><option value="multi-cloud">Multi-Cloud</option><option value="open">noch offen</option></Select></Field>
        <Field label="Externer Provider im Scope?"><Select value={workload.external_provider_in_scope} onChange={v=>setWorkload({...workload,external_provider_in_scope:v as Tri})}><option value="unknown">noch unklar</option><option value="yes">ja</option><option value="no">nein</option></Select></Field>
        <div style={full}><b>Zusätzliche Merkmale</b><p className="muted">Optional. Die technischen Codes bleiben intern; sichtbar sind fachliche Bezeichnungen.</p><div style={{...row,marginTop:8}}>{tags.map(tag=><label key={tag.value} style={{fontWeight:400}}><input type="checkbox" checked={workload.tags.includes(tag.value)} onChange={()=>toggleTag(tag.value)}/> {tag.label}</label>)}</div></div>
      </div>
      <div style={box}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}><div><h3 style={{margin:0}}>Beteiligte juristische Einheiten</h3><p className="muted">Eine primäre Einheit ist Pflicht. Weitere Tochter-, Mutter- oder andere Gesellschaften nur ergänzen, wenn sie für diesen Workload tatsächlich im Scope sind.</p></div><button type="button" onClick={()=>setEntities([...entities,{name:'',country:org.headquarters_country||'',city:'',postal_code:'',role:'other'}])}>+ Einheit hinzufügen</button></div>
        {entities.map((entity,i)=><div key={i} style={{...grid,marginTop:12}}>
          <Field label={i===0?'Primäre juristische Einheit':'Juristische Einheit'}><Text required value={entity.name} onChange={v=>updateEntity(i,'name',v)}/></Field>
          <Field label="Land"><Text required value={entity.country} onChange={v=>updateEntity(i,'country',v)}/></Field>
          <Field label="Ort"><Text value={entity.city} onChange={v=>updateEntity(i,'city',v)}/></Field>
          <Field label="Rolle"><Select value={entity.role} onChange={v=>updateEntity(i,'role',v)}><option value="primary">Primäre Einheit</option><option value="workload_owner">Workload-Verantwortlicher</option><option value="operator">Betreiber</option><option value="contracting_party">Vertragspartner</option><option value="data_controller">Datenschutzrechtlich Verantwortlicher</option><option value="user_group">Nutzende Einheit</option><option value="other">Sonstige Rolle</option></Select></Field>
          {i>0&&<button type="button" onClick={()=>setEntities(entities.filter((_,index)=>index!==i))}>Entfernen</button>}
        </div>)}
      </div>
    </>}

    {step===3&&!result&&<div>
      <h3>Prüfen & Assessment anlegen</h3>
      <div className="notice"><b>Noch nicht gespeichert.</b> Erst mit „Assessment speichern & Voranalyse erstellen“ werden die Angaben gespeichert und anschließend die automatische Voranalyse erzeugt.</div>
      <div style={box}><b>{decision.title}</b><p>{decision.objective}</p><p>{org.name} · {sectors.find(([v])=>v===org.sector)?.[1]||org.sector}{org.sector_detail?` · ${org.sector_detail}`:''} · {org.headquarters_city}, {org.headquarters_country}</p><p>{workload.name} · {archetypes.find(([v])=>v===workload.primary_archetype)?.[1]||workload.primary_archetype}</p><p>{workload.description}</p><p className="muted">Kritikalität und C/I/A bleiben unbewertet. Compliance wird erst nach dem Speichern als transparente Kandidatenliste berechnet.</p></div>
    </div>}

    {step===3&&result&&<div>
      <h3>Assessment gespeichert ✓</h3>
      <p className="lead">Voranalyse</p>
      <p className="muted">Diese Ergebnisse wurden erst nach dem Speichern aus den Intake-Fakten erzeugt. Sie dienen dem Routing und sind keine finale Souveränitäts- oder Rechtsbewertung.</p>
      <div style={grid}>{result.pre_assessment.compliance_candidates.map(c=><div key={c.framework} style={box}><b>{frameworkLabels[c.framework]||c.framework}</b><div><strong>{statusLabels[c.candidate_status]||c.candidate_status}</strong></div>{c.rationale.map(x=><p key={x}>{x}</p>)}{c.missing_facts.length>0&&<p className="muted">Noch zu klären: {c.missing_facts.join(' · ')}</p>}</div>)}</div>
      {result.pre_assessment.missing_scope_facts.length>0&&<div style={box}><h4>Offene Scope-Fakten</h4><ul>{result.pre_assessment.missing_scope_facts.map(x=><li key={x}>{x}</li>)}</ul></div>}
      {result.pre_assessment.suggested_deep_dive_profiles.length>0&&<div style={box}><h4>Vorgeschlagene Vertiefungen</h4><p>{result.pre_assessment.suggested_deep_dive_profiles.join(' · ')}</p></div>}
      {result.pre_assessment.suggested_screening_focus.length>0&&<div style={box}><h4>Vorgeschlagener Screening-Fokus</h4><ul>{result.pre_assessment.suggested_screening_focus.map(x=><li key={x}>{x}</li>)}</ul></div>}
      {result.pre_assessment.jurisdiction_complexity.length>0&&<div style={box}><h4>Scope-Komplexität</h4><ul>{result.pre_assessment.jurisdiction_complexity.map(x=><li key={x}>{x}</li>)}</ul></div>}
      <p className="muted">Assessment-ID: {result.assessment_id}</p>
    </div>}

    <div style={footer}>
      <div>{!result&&step>0&&<button type="button" onClick={()=>setStep(step-1)}>← Zurück</button>}</div>
      <div style={row}>
        {!result&&step<3&&<button className="primary" type="button" disabled={!canNext} onClick={next}>Weiter →</button>}
        {!result&&step===3&&<button className="primary" type="submit" disabled={saving}>{saving?'Speichere…':'Assessment speichern & Voranalyse erstellen'}</button>}
        {result&&<button className="primary" type="button" onClick={()=>window.location.reload()}>Zurück zum Dashboard</button>}
      </div>
    </div>
  </form></div>
}
