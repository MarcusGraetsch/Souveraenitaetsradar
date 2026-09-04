import type {
  Answer,
  Assessment,
  Claim,
  ClaimReviewStatus,
  Evidence,
  EvidenceReview,
  EvidenceReviewStatus,
  GateDefinition,
  GateEvaluation,
  GateRequirement,
  LlmImport,
  LlmProposalReview,
  LlmProposalReviewDecision,
  Question,
  QuestionView,
  QuestionWorkflowSummary,
  RelevanceProfile,
  AppliedState,
} from './types'

async function request<T>(path:string,init?:RequestInit):Promise<T>{
  const response=await fetch(path,init)
  if(!response.ok){
    const text=await response.text()
    throw new Error(text||`${response.status} ${response.statusText}`)
  }
  if(response.status===204)return undefined as T
  return response.json() as Promise<T>
}

function validateLlmAssessmentId(expectedId:string,raw:string):void{
  let parsed:unknown
  try{parsed=JSON.parse(raw)}catch{return}
  if(typeof parsed!=='object'||parsed===null)return
  const received=(parsed as {assessment_id?:unknown}).assessment_id
  if(typeof received==='string'&&received!==expectedId){
    throw new Error(`Assessment-ID stimmt nicht überein. Erwartet: ${expectedId}; erhalten: ${received}. Bitte die LLM-Ausgabe korrigieren oder neu erzeugen. IDs werden aus Sicherheitsgründen nicht automatisch verändert.`)
  }
}

export const api={
  assessments:()=>request<Assessment[]>('/api/assessments'),
  createAssessment:(payload:Partial<Assessment>&{name:string})=>
    request<Assessment>('/api/assessments',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(payload),
    }),
  deleteAssessment:(id:string)=>request<void>(`/api/assessments/${id}`,{method:'DELETE'}),
  questions:()=>request<Question[]>('/api/method/questions'),
  assessmentQuestions:(id:string,view:QuestionView='relevant')=>
    request<Question[]>(`/api/assessments/${id}/questions?view=${view}`),
  questionWorkflow:(id:string)=>request<QuestionWorkflowSummary>(`/api/assessments/${id}/question-workflow`),
  profile:(id:string)=>request<RelevanceProfile>(`/api/assessments/${id}/profile`),
  saveProfile:(id:string,payload:RelevanceProfile)=>
    request<RelevanceProfile>(`/api/assessments/${id}/profile`,{
      method:'PUT',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(payload),
    }),
  answers:(id:string)=>request<Answer[]>(`/api/assessments/${id}/answers`),
  saveAnswer:(assessmentId:string,questionId:string,payload:Partial<Answer>)=>
    request<Answer>(`/api/assessments/${assessmentId}/answers/${questionId}`,{
      method:'PUT',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({question_id:questionId,...payload}),
    }),
  evidence:(id:string)=>request<Evidence[]>(`/api/assessments/${id}/evidence`),
  addEvidence:(id:string,form:FormData)=>
    request<Evidence>(`/api/assessments/${id}/evidence`,{method:'POST',body:form}),
  evidenceReviews:(id:string)=>request<EvidenceReview[]>(`/api/assessments/${id}/evidence-reviews`),
  saveEvidenceReview:(assessmentId:string,evidenceId:string,payload:{
    applied_state:AppliedState
    base_trust:number
    scope_fit:number
    freshness_fit:number
    review_status:EvidenceReviewStatus
  })=>request<EvidenceReview>(`/api/assessments/${assessmentId}/evidence/${evidenceId}/review`,{
    method:'PUT',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify(payload),
  }),
  hardGates:()=>request<GateDefinition[]>('/api/method/hard-gates'),
  gateRequirements:(id:string)=>request<GateRequirement[]>(`/api/assessments/${id}/gate-requirements`),
  saveGateRequirement:(assessmentId:string,gateId:string,requirementLevel:number)=>
    request<GateRequirement>(`/api/assessments/${assessmentId}/gate-requirements/${gateId}`,{
      method:'PUT',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({requirement_level:requirementLevel}),
    }),
  claims:(id:string)=>request<Claim[]>(`/api/assessments/${id}/claims`),
  createClaim:(assessmentId:string,payload:{
    gate_id:string
    statement:string
    review_status:ClaimReviewStatus
    capability_level:number|null
    evidence_ids:string[]
    question_ids:string[]
    notes:string
  })=>request<Claim>(`/api/assessments/${assessmentId}/claims`,{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify(payload),
  }),
  updateClaim:(assessmentId:string,claimId:string,payload:{
    gate_id:string
    statement:string
    review_status:ClaimReviewStatus
    capability_level:number|null
    evidence_ids:string[]
    question_ids:string[]
    notes:string
  })=>request<Claim>(`/api/assessments/${assessmentId}/claims/${claimId}`,{
    method:'PUT',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify(payload),
  }),
  deleteClaim:(assessmentId:string,claimId:string)=>
    request<void>(`/api/assessments/${assessmentId}/claims/${claimId}`,{method:'DELETE'}),
  gates:(id:string)=>request<GateEvaluation[]>(`/api/assessments/${id}/gates`),
  prompt:(id:string)=>request<{prompt:string}>(`/api/assessments/${id}/llm-bridge/prompt`),
  importLlm:(id:string,raw:string)=>{
    validateLlmAssessmentId(id,raw)
    return request<LlmImport>(`/api/assessments/${id}/llm-bridge/import`,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:raw,
    })
  },
  llmImports:(id:string)=>request<LlmImport[]>(`/api/assessments/${id}/llm-bridge/imports`),
  llmProposalReviews:(id:string)=>request<LlmProposalReview[]>(`/api/assessments/${id}/llm-bridge/proposal-reviews`),
  reviewLlmProposal:(assessmentId:string,importId:string,proposalIndex:number,payload:{
    decision:LlmProposalReviewDecision
    answer_value?:string
    evidence_ids?:string[]
    reviewer_note?:string
  })=>request<LlmProposalReview>(`/api/assessments/${assessmentId}/llm-bridge/imports/${importId}/proposals/${proposalIndex}/review`,{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify(payload),
  }),
}
