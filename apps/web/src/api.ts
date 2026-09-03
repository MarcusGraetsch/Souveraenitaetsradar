import type { Answer, Assessment, Evidence, LlmImport, Question, RelevanceProfile } from './types'

async function request<T>(path:string,init?:RequestInit):Promise<T>{
  const response=await fetch(path,init)
  if(!response.ok){
    const text=await response.text()
    throw new Error(text||`${response.status} ${response.statusText}`)
  }
  if(response.status===204)return undefined as T
  return response.json() as Promise<T>
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
  assessmentQuestions:(id:string,view:'relevant'|'all'='relevant')=>
    request<Question[]>(`/api/assessments/${id}/questions?view=${view}`),
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
  prompt:(id:string)=>request<{prompt:string}>(`/api/assessments/${id}/llm-bridge/prompt`),
  importLlm:(id:string,raw:string)=>
    request<LlmImport>(`/api/assessments/${id}/llm-bridge/import`,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:raw,
    }),
  llmImports:(id:string)=>request<LlmImport[]>(`/api/assessments/${id}/llm-bridge/imports`),
}
