import type { ClaimReviewStatus, EvidenceReviewStatus, GateFinalState } from './types'

export const gateUi:Record<string,{name:string;description:string}>={
  'HG-01':{
    name:'Rechtsraum und tatsächliche Kontrolle',
    description:'Vertragspartner, Unternehmenssitz und tatsächliche Kontrolle müssen zu den festgelegten Anforderungen an den Rechts- und Kontrollraum passen.',
  },
  'HG-02':{
    name:'Datenstandort und Datenverarbeitung',
    description:'Speicherung und Verarbeitung – einschließlich Backups, Ausweichbetrieb, Support und relevanter KI-Verarbeitung – müssen den festgelegten Standortanforderungen entsprechen.',
  },
  'HG-03':{
    name:'Kontrolle über kryptografische Schlüssel',
    description:'Es wird geprüft, wer relevante Schlüssel technisch verwenden, sperren, ersetzen oder wiederherstellen kann.',
  },
  'HG-04':{
    name:'Ausstieg und Übertragbarkeit',
    description:'Daten, Konfiguration und Workload müssen in einer nutzbaren Form auf eine realistische Alternative übertragbar sein; bei höheren Anforderungen gehört ein getesteter Wechsel dazu.',
  },
  'HG-05':{
    name:'Betriebliche Eigenständigkeit',
    description:'Der Workload soll für die geforderte Zeit ohne kritische externe Support- oder Steuerungsabhängigkeiten weiterbetrieben werden können.',
  },
  'HG-06':{
    name:'Identitäten und zentrale Vertrauensdienste',
    description:'Kritische Abhängigkeiten von Identitätsdiensten, PKI, DNS, Schlüsselmanagement und anderen Vertrauensankern müssen kontrolliert oder durch getestete Alternativen abgesichert sein.',
  },
  'HG-07':{
    name:'Kritische Abhängigkeiten in der Lieferkette',
    description:'Kritische Software-, Hardware-, Dienstleister- und Unterauftragnehmer-Abhängigkeiten müssen bekannt und angemessen ersetzbar oder kontrolliert sein.',
  },
  'HG-08':{
    name:'Sicherheits-Mindestniveau',
    description:'Der Workload muss das für seinen Schutzbedarf erforderliche Sicherheitsniveau mit tatsächlich umgesetzten und – soweit gefordert – getesteten Maßnahmen erreichen.',
  },
}

export const gateStateLabel:Record<GateFinalState,string>={
  PASS:'Mindestanforderung erfüllt',
  FAIL:'Mindestanforderung nicht erfüllt',
  UNVERIFIED:'nicht ausreichend belegt',
  'N/A':'nicht anwendbar',
}

export const gateStateShortLabel:Record<GateFinalState,string>={
  PASS:'erfüllt',
  FAIL:'nicht erfüllt',
  UNVERIFIED:'nicht ausreichend belegt',
  'N/A':'nicht anwendbar',
}

export const claimReviewStatusLabel:Record<ClaimReviewStatus,string>={
  draft:'Entwurf',
  reviewed:'geprüft',
  approved:'freigegeben',
  rejected:'verworfen',
}

export const evidenceReviewStatusLabel:Record<EvidenceReviewStatus,string>={
  raw:'noch nicht geprüft',
  normalized:'aufbereitet',
  reviewed:'geprüft',
  approved:'freigegeben',
  rejected:'verworfen',
}

export const appliedStateLabel:Record<string,string>={
  asserted:'angegeben',
  available:'als Funktion verfügbar',
  documented:'dokumentiert',
  observed:'beobachtet',
  configured:'konfiguriert',
  tested:'getestet',
  attested:'extern bestätigt',
}

export const requirementSourceLabel=(source:string):string=>{
  if(source==='criticality-template:basis')return 'Aus Kritikalitätsprofil: niedrig'
  if(source==='criticality-template:standard')return 'Aus Kritikalitätsprofil: mittel'
  if(source==='criticality-template:elevated')return 'Aus Kritikalitätsprofil: erhöht'
  if(source==='criticality-template:critical')return 'Aus Kritikalitätsprofil: kritisch'
  if(source==='consultant-override')return 'Manuell vom Consultant angepasst'
  return source
}

type EvidenceRequestUi={title:string;question:string;examples:string}

export const evidenceRequestUi:Record<string,EvidenceRequestUi>={
  'ER-001':{
    title:'Vertragspartner und kontrollierende Gesellschaft',
    question:'Welche rechtliche Einheit schließt den Vertrag, und welche Gesellschaft kontrolliert sie letztlich?',
    examples:'Unterzeichneter Vertrag; Bestellformular; Auftragsverarbeitungsvertrag (DPA/AVV); Handels- oder Anbieterregister',
  },
  'ER-002':{
    title:'Zugriffs- und Kontrollrisiken aus anderen Rechtsräumen',
    question:'Welche Staaten außerhalb des Zielraums können rechtlich Zugriff oder Kontrolle erzwingen?',
    examples:'Rechtliche Bewertung/TIA; Vertrag; Richtlinie zu Behördenzugriffen',
  },
  'ER-003':{
    title:'Speicher- und Verarbeitungsorte',
    question:'Wo werden Primärdaten, Backups, Supportdaten, Ausweichbetrieb und gegebenenfalls KI-Inferenz verarbeitet?',
    examples:'Architekturunterlagen; Vertrag; Anbieterexport; Screenshots; Service-Konfiguration',
  },
  'ER-004':{
    title:'Technische Kontrolle über Schlüssel',
    question:'Wer kann die relevanten Schlüssel technisch verwenden, sperren, ersetzen oder wiederherstellen?',
    examples:'Schlüsselmanagement-Konzept; Konfigurationsexport; Key Policy; Testbericht',
  },
  'ER-005':{
    title:'Export von Daten und Konfiguration',
    question:'Können Daten, Metadaten, Konfiguration und Richtlinien in einer praktisch nutzbaren Form exportiert werden?',
    examples:'Export-Dokumentation; Beispiel-Export; API-Schema; Infrastructure-as-Code',
  },
  'ER-006':{
    title:'Getesteter Ausstieg',
    question:'Wurde ein alternatives Ziel Ende-zu-Ende getestet – einschließlich Migration, Wiederherstellung oder Umschaltung?',
    examples:'Testbericht zu Migration, Restore, Cutover oder Rollback',
  },
  'ER-007':{
    title:'Anforderung und Test zur betrieblichen Eigenständigkeit',
    question:'Wie lange muss der Workload ohne kritische externe Provider- oder Supportabhängigkeit weiterlaufen können, und wurde das getestet?',
    examples:'BCM-Anforderung; Runbook für eingeschränkten Betrieb; Übungs- oder Testbericht',
  },
  'ER-008':{
    title:'Identitäten und zentrale Vertrauensdienste',
    question:'Welche gemeinsam genutzten Identitäts-, PKI-, DNS-, KMS- oder vergleichbaren Vertrauensdienste können mehrere Services gleichzeitig blockieren?',
    examples:'Architektur; IdP-/PKI-/DNS-/KMS-Dokumentation; redigierte Richtlinien; Break-Glass-Test',
  },
  'ER-009':{
    title:'Unterauftragnehmer und kritische Abhängigkeiten',
    question:'Welche kritischen Abhängigkeiten von Unterauftragnehmern, Software, Hardware oder Diensten lassen sich nicht ohne Weiteres ersetzen?',
    examples:'Unterauftragnehmerliste; SBOM; CMDB; Abhängigkeitskarte; Vertrag',
  },
  'ER-010':{
    title:'Konzentrations- und gemeinsame Ausfallabhängigkeiten',
    question:'Welche Workloads teilen denselben Provider, IdP, DNS-, Netzwerk- oder KMS-Dienst, dasselbe KI-Modell oder denselben Unterauftragnehmer?',
    examples:'Portfolio-Inventar; DORA-RoI-ähnlicher Export; CMDB',
  },
  'ER-011':{
    title:'Umgesetzte Sicherheitsmaßnahmen',
    question:'Welche für den Workload erforderlichen Sicherheitsmaßnahmen sind tatsächlich konfiguriert?',
    examples:'ISMS-Unterlagen; Konfigurationsexport; Architektur; Screenshots',
  },
  'ER-012':{
    title:'Wirksamkeit der Sicherheitsmaßnahmen',
    question:'Welche Sicherheitsmaßnahmen wurden getestet, und welche Ausnahmen oder Restbefunde bestehen?',
    examples:'Test-, Scan-, Incident-Response- oder Restore-Nachweise; unabhängige Prüfberichte',
  },
}

export const getGateUi=(gateId:string,fallbackName:string,fallbackDescription:string)=>
  gateUi[gateId]??{name:fallbackName,description:fallbackDescription}

export const getEvidenceRequestUi=(requestId:string,fallbackTitle:string,fallbackQuestion:string,fallbackExamples:string):EvidenceRequestUi=>
  evidenceRequestUi[requestId]??{title:fallbackTitle,question:fallbackQuestion,examples:fallbackExamples}
