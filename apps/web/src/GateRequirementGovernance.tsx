import { FormEvent, useEffect, useMemo, useState } from 'react'
import { api } from './api'
import { requirementSourceLabel } from './consultantTerminology'
import type { GateDefinition, GateRequirement, GateRequirementChange } from './types'
import './GateRequirementGovernance.css'

export function GateRequirementGovernance({
  assessmentId,
  gateId,
  definition,
  requirement,
  onChanged,
}:{
  assessmentId:string
  gateId:string
  definition:GateDefinition
  requirement:GateRequirement
  onChanged:()=>Promise<void>
}){
  const[overrideLevel,setOverrideLevel]=useState(String(requirement.requirement_level))
  const[overrideReason,setOverrideReason]=useState('')
  const[resetReason,setResetReason]=useState('')
  const[changes,setChanges]=useState<GateRequirementChange[]>([])
  const[message,setMessage]=useState('')
  const[busy,setBusy]=useState(false)

  const loadHistory=async()=>setChanges(await api.gateRequirementChanges(assessmentId,gateId))
  useEffect(()=>{setOverrideLevel(String(requirement.requirement_level));setOverrideReason('');setResetReason('');setMessage('');void loadHistory()},[assessmentId,gateId,requirement.requirement_level,requirement.is_override])

  const levels=useMemo(()=>[0,1,2,3,4].map(level=>({level,description:definition.capability_levels[level]||'Keine Methodenbeschreibung vorhanden.'})),[definition])
  const overrideNumber=Number(overrideLevel)
  const canSaveOverride=overrideReason.trim().length>=3&&overrideNumber!==requirement.default_level&&overrideNumber!==requirement.requirement_level&&!busy
  const canReset=requirement.is_override&&resetReason.trim().length>=3&&!busy

  const saveOverride=async(event:FormEvent)=>{
    event.preventDefault()
    if(!canSaveOverride)return
    setBusy(true);setMessage('')
    try{
      await api.saveGateRequirement(assessmentId,gateId,overrideNumber,overrideReason.trim())
      setOverrideReason('')
      setMessage('Abweichende Mindeststufe mit Begründung gespeichert ✓')
      await onChanged();await loadHistory()
    }catch(error){setMessage(`Änderung abgelehnt: ${String(error)}`)}finally{setBusy(false)}
  }

  const resetDefault=async(event:FormEvent)=>{
    event.preventDefault()
    if(!canReset)return
    setBusy(true);setMessage('')
    try{
      await api.resetGateRequirement(assessmentId,gateId,resetReason.trim())
      setResetReason('')
      setMessage('Standardwert aus dem Kritikalitätsprofil wiederhergestellt ✓')
      await onChanged();await loadHistory()
    }catch(error){setMessage(`Reset abgelehnt: ${String(error)}`)}finally{setBusy(false)}
  }

  return <section className="requirement-governance">
    <h3>Geforderte Mindeststufe und Herleitung</h3>
    <p><b>Standardwert:</b> Stufe {requirement.default_level} · {requirementSourceLabel(requirement.default_source)}</p>
    <p><b>Aktueller Wert:</b> Stufe {requirement.requirement_level} · {requirement.is_override?'begründete manuelle Abweichung':'Standardwert des Kritikalitätsprofils'}</p>
    <p className="muted">Die Stufen 0–4 sind eine interne Operationalisierung des Souveränitäts-Radars und keine offizielle BSI-, EU- oder Gesetzesskala. Der Standardwert ist eine Startkonfiguration; eine Abweichung muss fachlich begründet werden.</p>

    <h4>Was bedeuten die Stufen bei diesem Kriterium?</h4>
    <div className="requirement-scale">
      {levels.map(item=><div className={`requirement-scale-row ${item.level===requirement.requirement_level?'current':''}`} key={item.level}><b>Stufe {item.level}</b><span>{item.description}</span>{item.level===requirement.default_level&&<small>Standardwert</small>}{item.level===requirement.requirement_level&&requirement.is_override&&<small>aktuelle Abweichung</small>}</div>)}
    </div>

    <form className="governance-form" onSubmit={saveOverride}>
      <h4>Begründet abweichende Mindeststufe setzen</h4>
      <p className="muted">Nur verwenden, wenn Rechtslage, Schutzbedarf, interne Policy oder Risikoappetit für dieses Assessment bewusst vom Kritikalitäts-Standard abweichen.</p>
      <label>Abweichende Mindeststufe
        <select value={overrideLevel} onChange={event=>setOverrideLevel(event.target.value)}>
          {[0,1,2,3,4].map(level=><option key={level} value={level} disabled={level===requirement.default_level}>Stufe {level}{level===requirement.default_level?' – Standardwert':''}</option>)}
        </select>
      </label>
      <label>Begründung
        <textarea value={overrideReason} onChange={event=>setOverrideReason(event.target.value)} placeholder="Warum soll für dieses konkrete Assessment eine andere Mindeststufe gelten?"/>
      </label>
      <button className="primary" type="submit" disabled={!canSaveOverride}>{busy?'Speichere…':'Abweichung speichern'}</button>
    </form>

    {requirement.is_override&&<form className="governance-form" onSubmit={resetDefault}>
      <h4>Standardwert wieder verwenden</h4>
      <p className="muted">Der aktuelle manuelle Override wird entfernt. Danach gilt wieder Stufe {requirement.default_level} aus dem Kritikalitätsprofil.</p>
      <label>Begründung für die Rückkehr zum Standard
        <textarea value={resetReason} onChange={event=>setResetReason(event.target.value)} placeholder="Warum ist die abweichende Mindeststufe nicht mehr erforderlich?"/>
      </label>
      <button type="submit" disabled={!canReset}>{busy?'Speichere…':'Standardwert wieder verwenden'}</button>
    </form>}

    {message&&<p className={message.includes('abgelehnt')?'warning':'save-message'}>{message}</p>}

    <h4>Änderungshistorie</h4>
    {changes.length===0?<p className="muted">Für dieses Kriterium wurde die Mindeststufe noch nicht manuell verändert.</p>:<div className="governance-history">{[...changes].reverse().map(change=><div className="governance-history-row" key={change.id}><b>{change.change_type==='override'?'Manuelle Abweichung':'Rückkehr zum Standard'}: Stufe {change.previous_level} → Stufe {change.new_level}</b><span>{change.reason}</span><small>{new Date(change.created_at).toLocaleString('de-DE')} · {requirementSourceLabel(change.previous_source)} → {requirementSourceLabel(change.new_source)}</small></div>)}</div>}
  </section>
}