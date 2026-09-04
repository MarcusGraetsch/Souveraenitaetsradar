import { useState } from 'react'
import type { Assessment } from './types'

async function restoreFile(file:File):Promise<{assessment_id:string;gate_semantic_drift:boolean;warnings?:string[]}>{
  if(file.name.toLowerCase().endsWith('.zip')||file.type==='application/zip'){
    const form=new FormData();form.set('file',file)
    const response=await fetch('/api/assessments/import-backup',{method:'POST',body:form})
    if(!response.ok)throw new Error(await response.text()||`HTTP ${response.status}`)
    return response.json()
  }
  const raw=await file.text()
  let payload:unknown
  try{payload=JSON.parse(raw)}catch{throw new Error('Die Datei enthält kein valides JSON.')}
  const response=await fetch('/api/assessments/import',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
  if(!response.ok)throw new Error(await response.text()||`HTTP ${response.status}`)
  return response.json()
}

function DownloadLink({href,children,dangerous=false}:{href:string;children:string;dangerous?:boolean}){
  const warning='Dieses vollständige Backup kann vertrauliche Nachweisdateien und ausdrücklich für die LLM-Nutzung freigegebene Textauszüge enthalten. Speichern Sie die Datei entsprechend geschützt. Vollständiges Backup jetzt erstellen?'
  return <a className="primary export-link" href={href} download onClick={event=>{if(dangerous&&!window.confirm(warning))event.preventDefault()}}>{children}</a>
}

export function ExportTools({assessment}:{assessment:Assessment}){
  const[file,setFile]=useState<File|null>(null)
  const[busy,setBusy]=useState(false)
  const[message,setMessage]=useState('')
  const restore=async()=>{
    if(!file)return
    setBusy(true);setMessage('')
    try{
      const result=await restoreFile(file)
      if(result.gate_semantic_drift){
        setMessage(`Restore erzeugt Assessment ${result.assessment_id}, aber der Gate-Vergleich meldet semantischen Drift. Vor Nutzung fachlich prüfen.`)
      }else{
        setMessage(`Restore erfolgreich: neues Assessment ${result.assessment_id}. Gate-Semantik stimmt mit dem Exportzustand überein.`)
      }
    }catch(error){setMessage(`Restore fehlgeschlagen: ${String(error)}`)}finally{setBusy(false)}
  }
  return <section className="panel"><h2>Export, Bericht & Backup</h2><p>Diese Funktionen verändern das Assessment und seine Hard-Gate-Ergebnisse nicht. Der Standardexport und der Consultant Report enthalten keine Raw-Evidence-Dateien und keine freigegebenen Evidence-Textauszüge.</p><div className="action-row export-actions"><DownloadLink href={`/api/assessments/${assessment.id}/export`}>Structured JSON</DownloadLink><DownloadLink href={`/api/assessments/${assessment.id}/report`}>Consultant Report</DownloadLink><DownloadLink href={`/api/assessments/${assessment.id}/backup`}>Strukturiertes Backup</DownloadLink><DownloadLink href={`/api/assessments/${assessment.id}/backup?include_evidence=true`} dangerous>Vollbackup inkl. Evidence</DownloadLink></div><div className="notice"><b>Evidence-Minimierung:</b> Das Vollbackup ist ein explizites Opt-in für Wiederherstellung und kann vertrauliche Raw-Evidence-Dateien sowie freigegebene Textauszüge enthalten. Für Management-/Berichtsweitergabe den Consultant Report oder das strukturierte Backup verwenden.</div><h3>Assessment wiederherstellen</h3><p className="muted">Hier können Sie einen zuvor vom Souveränitäts-Radar erzeugten Assessment-Export (.json) oder ein Radar-Backup (.zip) wiederherstellen. Ein Consultant Report ist nicht importierbar. Restore überschreibt nichts, sondern erzeugt ein neues Assessment, mappt Referenzen neu und berechnet Hard Gates erneut.</p><div className="action-row"><input type="file" accept=".json,.zip,application/json,application/zip" onChange={event=>{setFile(event.target.files?.[0]||null);setMessage('')}}/><button className="primary" disabled={!file||busy} onClick={()=>void restore()}>{busy?'Restore läuft…':'Als neues Assessment wiederherstellen'}</button></div>{message&&<p className={message.startsWith('Restore fehlgeschlagen')||message.includes('Drift')?'warning':'save-message'}>{message}</p>}<p className="muted">Nach erfolgreichem Restore über „← Assessments“ zur Übersicht zurückkehren. Die Assessment-Liste wird dabei neu geladen.</p></section>
}
