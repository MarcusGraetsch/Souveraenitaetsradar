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
export type WorkflowStage='screening'|'clarification'|'deep_dive'|'completed'|'excluded'
export type QuestionView='work'|'screening'|'clarification'|'deep_dive'|'completed'|'relevant'|'all'
export type AnswerControlKind='single_select'|'text'|'list'|'date'|'structured_text'
export type AnswerControlOption={value:string;label:string}
export type AnswerControl={
  source_type:string
  kind:AnswerControlKind
  options:AnswerControlOption[]
  placeholder:string
  help_text:string
  mapping_status:'mapped'|'needs_review'
}

export type Question={
  id:string
  domain:string
  target_object:string
  question:string
  answer_type:string
  answer_control:AnswerControl
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
  workflow_stage?:WorkflowStage
  workflow_reason?:string
  workflow_order?:number
}

export type QuestionWorkflowSummary={
  assessment_id:string
  total:number
  relevant:number
  work_queue:number
  stages:Record<WorkflowStage,number>
  applicability:Record<ApplicabilityStatus,number>
  domains:Record<string,Record<WorkflowStage,number>>
  next_stage:'screening'|'clarification'|'deep_dive'|'done'
  stage_order:WorkflowStage[]
  policy:string
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

export type AppliedState='asserted'|'available'|'documented'|'observed'|'configured'|'tested'|'attested'
export type EvidenceReviewStatus='raw'|'normalized'|'reviewed'|'approved'|'rejected'

export type EvidenceReview={
  evidence_id:string
  assessment_id:string
  applied_state:AppliedState
  base_trust:number
  scope_fit:number
  freshness_fit:number
  review_status:EvidenceReviewStatus
  effective_trust:number
  updated_at:string
}

export type ClaimReviewStatus='draft'|'reviewed'|'approved'|'rejected'
export type Claim={
  id:string
  assessment_id:string
  gate_id:string
  statement:string
  review_status:ClaimReviewStatus
  capability_level:number|null
  evidence_ids:string[]
  question_ids:string[]
  notes:string
  created_at:string
  updated_at:string
}

export type GateRequirement={
  assessment_id:string
  gate_id:string
  requirement_level:number
  source:string
  updated_at:string|null
}

export type EvidenceRequest={
  request_id:string
  gate_id:string
  claim_area:string
  acceptable_evidence:string
  required_for:string
  follow_up:string
  preferred_applied_state:string
  typical_min_trust:string
  provenance:string
}

export type GateDefinition={
  gate_id:string
  name:string
  subject:string
  requirement_templates:Record<string,number>
  source_ids:string[]
  provenance:string
  evidence_requests:EvidenceRequest[]
}

export type GateFinalState='PASS'|'FAIL'|'UNVERIFIED'|'N/A'
export type GateEvaluation={
  gate_id:string
  name:string
  subject:string
  requirement_level:number
  requirement_source:string
  capability_level:number|null
  effective_trust:number|null
  technical_state:GateFinalState
  evidence_state:'VERIFIED'|'UNVERIFIED'|'N/A'
  final_state:GateFinalState
  claim_ids:string[]
  evidence_ids:string[]
  reasons:string[]
  evidence_requests:EvidenceRequest[]
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

export type LlmProposalReviewDecision='accepted'|'edited'|'rejected'
export type LlmProposalReview={
  id:string
  assessment_id:string
  llm_import_id:string
  proposal_index:number
  question_id:string
  decision:LlmProposalReviewDecision
  final_answer_value:string
  evidence_ids:string[]
  answer_id:string|null
  reviewer_note:string
  created_at:string
}
