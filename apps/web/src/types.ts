export type Assessment={
  id:string
  name:string
  customer:string
  description:string
  workload_type:string
  criticality:string
  confidentiality:string
  integrity:string
  availability:string
  control_region:string
  regulatory_context:string
  status:string
  created_at:string
  updated_at:string
}

export type ApplicabilityStatus='applicable'|'not_applicable'|'needs_review'

export type Question={
  id:string
  domain:string
  target_object:string
  question:string
  answer_type:string
  applicability:string
  requiredness:string
  expected_evidence:string
  min_trust:string
  risk_ids:string
  sov_reference:string
  follow_up:string
  applicability_status?:ApplicabilityStatus
  applicability_reason?:string
  applicability_facts?:string[]
}

export type RelevanceProfile={
  assessment_id?:string
  service_model:'unknown'|'saas'|'paas'|'iaas'|'managed-service'|'on-prem'|'other'
  cloud_service:boolean|null
  contract_in_scope:boolean|null
  data_processing:boolean|null
  persistent_data:boolean|null
  encryption_used:boolean|null
  key_model:'unknown'|'customer'|'provider'|'external'|'mixed'|'none'
  ai_used:boolean|null
  agentic_ai:boolean|null
  exit_relevant:boolean|null
  backup_relevant:boolean|null
  multi_provider:boolean|null
  subcontractors_used:boolean|null
  c5_relevant:boolean|null
  c3a_relevant:boolean|null
  iam_relevant:boolean|null
  logging_relevant:boolean|null
  internet_exposed:boolean|null
  updated_at?:string|null
}

export type Answer={
  id:string
  assessment_id:string
  question_id:string
  answer_value:string
  comment:string
  evidence_ids:string[]
  review_state:'draft'|'reviewed'
  updated_at:string
}

export type Evidence={
  id:string
  assessment_id:string
  title:string
  evidence_type:string
  description:string
  source:string
  source_date:string
  content_excerpt:string
  file_name:string
  created_at:string
}

export type LlmProposal={
  question_id:string
  proposed_answer:string
  rationale:string
  evidence_ids:string[]
  confidence:number
}

export type LlmImport={
  id:string
  assessment_id:string
  validation_status:string
  proposals:LlmProposal[]
  evidence_gaps:{question_id:string;missing:string}[]
  warnings:string[]
  created_at:string
}
