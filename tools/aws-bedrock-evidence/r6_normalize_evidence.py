#!/usr/bin/env python3
"""Normalize R6 collector output into reviewable technical facts; no AWS/network calls."""
from pathlib import Path
import json, sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 r6_normalize_evidence.py <evidence_dir>")
root=Path(sys.argv[1])
if not root.is_dir():
    raise SystemExit(f"Not a directory: {root}")

def load(name, default=None):
    p=root/name
    if not p.exists(): return default
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return default

meta=load("_collector_meta.json",{}) or {}; identity=load("00_identity.json",{}) or {}
logging_cfg=load("20_model_invocation_logging.json",{}) or {}; profiles=load("12_inference_profiles.json",{}) or {}
selected_profile=load("13_selected_inference_profile.json",None); agent=load("41_agent.json",None)
guardrails=load("30_guardrails.json",{}) or {}; enforced=load("31_enforced_guardrails.json",{}) or {}
vpc=load("80_vpc_endpoints_bedrock.json",{}) or {}; trails=load("90_cloudtrail_trails.json",{}) or {}
actions=load("42_action_groups.json",{}) or {}; agent_kbs=load("43_agent_knowledge_bases.json",{}) or {}
errors=[]; ef=root/"_errors.jsonl"
if ef.exists():
    for line in ef.read_text(encoding="utf-8").splitlines():
        try: errors.append(json.loads(line))
        except Exception: pass
log_config=logging_cfg.get("loggingConfig") or {}; cloudwatch=log_config.get("cloudWatchConfig") or {}; s3cfg=log_config.get("s3Config") or {}
facts={
 "collector_version":meta.get("collector_version"),"collected_at":meta.get("collected_at"),"account_id":identity.get("Account"),"caller_arn":identity.get("Arn"),"region":meta.get("region"),
 "selected_model_id":meta.get("model_id") or None,"selected_inference_profile_id":meta.get("inference_profile_id") or None,"selected_agent_id":meta.get("agent_id") or None,
 "agent_name":((agent or {}).get("agent") or {}).get("agentName") if agent else None,"agent_status":((agent or {}).get("agent") or {}).get("agentStatus") if agent else None,
 "agent_foundation_model":((agent or {}).get("agent") or {}).get("foundationModel") if agent else None,"agent_role_arn":((agent or {}).get("agent") or {}).get("agentResourceRoleArn") if agent else None,
 "agent_customer_encryption_key_arn":((agent or {}).get("agent") or {}).get("customerEncryptionKeyArn") if agent else None,
 "inference_profile_count":len(profiles.get("inferenceProfileSummaries",[]) or []),"selected_inference_models":(selected_profile or {}).get("models") if selected_profile else None,
 "model_invocation_logging_configured":bool(log_config),"model_invocation_log_group":cloudwatch.get("logGroupName"),
 "model_invocation_s3_bucket":s3cfg.get("bucketName") or (cloudwatch.get("largeDataDeliveryS3Config") or {}).get("bucketName"),
 "guardrail_count":len(guardrails.get("guardrails",[]) or []),"enforced_guardrail_count":len(enforced.get("guardrailsConfig",[]) or []),
 "bedrock_vpc_endpoint_count":len(vpc.get("VpcEndpoints",[]) or []),"cloudtrail_trail_count":len(trails.get("trailList",[]) or []),
 "agent_action_group_count":len(actions.get("actionGroupSummaries",[]) or []),"agent_knowledge_base_count":len(agent_kbs.get("agentKnowledgeBaseSummaries",[]) or []),"collector_error_count":len(errors)}
findings=[]
def add(fid,gate,state,title,evidence,next_action): findings.append({"finding_id":fid,"gate":gate,"state":state,"title":title,"evidence":evidence,"next_action":next_action})
if facts["selected_inference_profile_id"]:
    add("TECH-F01","HG-02","EVIDENCED" if selected_profile else "UNVERIFIED","Selected inference profile retrieved." if selected_profile else "Selected inference profile was not retrieved.","13_selected_inference_profile.json" if selected_profile else "_errors.jsonl","Review routed model regions." if selected_profile else "Resolve permission/identifier and rerun.")
else: add("TECH-F01","HG-02","UNVERIFIED","No selected inference profile supplied.","_collector_meta.json","Set --inference-profile-id or prove direct in-region use.")
add("TECH-F02","HG-08","EVIDENCED" if facts["model_invocation_logging_configured"] else "UNVERIFIED","Invocation logging config evidenced." if facts["model_invocation_logging_configured"] else "No invocation logging config evidenced.","20_model_invocation_logging.json","Review content flags, encryption and retention.")
add("TECH-F03","HG-06/HG-08","EVIDENCED" if facts["bedrock_vpc_endpoint_count"]>0 else "UNVERIFIED",f"{facts['bedrock_vpc_endpoint_count']} Bedrock VPC endpoint(s) evidenced." if facts["bedrock_vpc_endpoint_count"]>0 else "No Bedrock VPC endpoint evidenced.","80_vpc_endpoints_bedrock.json","Review endpoint policies/network placement.")
if facts["selected_agent_id"]:
    add("TECH-F04","HG-06/HG-08","EVIDENCED" if agent else "UNVERIFIED","Selected agent configuration retrieved." if agent else "Agent ID supplied but not retrieved.","41_agent.json" if agent else "_errors.jsonl","Review role/model/KMS/action groups/KBs.")
else: add("TECH-F04","HG-06/HG-08","UNVERIFIED","No Agent ID supplied.","_collector_meta.json","Rerun with --agent-id.")
add("TECH-F05","HG-03","PARTIAL" if facts["agent_customer_encryption_key_arn"] else "UNVERIFIED","Agent references customer encryption key." if facts["agent_customer_encryption_key_arn"] else "No agent customer encryption key evidenced.","41_agent.json + 70_kms_*","Review key origin/policy/control; CMK does not prove HYOK.")
add("TECH-F06","HG-08","PARTIAL" if (facts["guardrail_count"]>0 or facts["enforced_guardrail_count"]>0) else "UNVERIFIED","Guardrail configuration exists." if (facts["guardrail_count"]>0 or facts["enforced_guardrail_count"]>0) else "No guardrail configuration evidenced.","30_guardrails.json / 31_enforced_guardrails.json","Verify selected agent/model usage and test tool paths.")
out={"schema_version":"0.9","facts":facts,"technical_findings":findings,"evidence_state":"TECHNICAL_EVIDENCE_COLLECTED" if facts["collector_error_count"]==0 else "PARTIAL_WITH_COLLECTION_ERRORS","warning":"Configuration evidence, not a final sovereignty/security decision."}
(root/"normalized_evidence.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
(root/"technical_findings.json").write_text(json.dumps(findings,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps({"output":str(root/"normalized_evidence.json"),"findings":len(findings),"collector_errors":facts["collector_error_count"]},indent=2))
