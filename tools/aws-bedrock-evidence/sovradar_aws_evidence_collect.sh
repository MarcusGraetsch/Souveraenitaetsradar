#!/usr/bin/env bash
set -u
set -o pipefail

usage(){ echo "Usage: $0 --profile PROFILE --region REGION [--agent-id ID] [--agent-version DRAFT|N] [--model-id ID] [--inference-profile-id ID] [--kms-key ID] [--out DIR]"; }
PROFILE=""; REGION=""; AGENT_ID=""; AGENT_VERSION="DRAFT"; MODEL_ID=""; INFERENCE_PROFILE_ID=""; EXPLICIT_KMS_KEY=""; OUT_PARENT="./r6_evidence"
while [[ $# -gt 0 ]]; do case "$1" in
 --profile) PROFILE="$2";shift 2;; --region) REGION="$2";shift 2;; --agent-id) AGENT_ID="$2";shift 2;; --agent-version) AGENT_VERSION="$2";shift 2;; --model-id) MODEL_ID="$2";shift 2;; --inference-profile-id) INFERENCE_PROFILE_ID="$2";shift 2;; --kms-key) EXPLICIT_KMS_KEY="$2";shift 2;; --out) OUT_PARENT="$2";shift 2;; -h|--help) usage;exit 0;; *) echo "Unknown: $1" >&2;usage;exit 2;; esac; done
[[ -n "$PROFILE" && -n "$REGION" ]] || { usage >&2; exit 2; }
for dep in aws jq sha256sum; do command -v "$dep" >/dev/null || { echo "Missing $dep" >&2; exit 3; }; done
AWS_VER="$(aws --version 2>&1 || true)"; [[ "$AWS_VER" == aws-cli/2* ]] || { echo "AWS CLI v2 required" >&2; exit 4; }
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"; OUT="${OUT_PARENT%/}/${STAMP}_${REGION}"; mkdir -p "$OUT"; MANIFEST="$OUT/_manifest.jsonl"; ERRORS="$OUT/_errors.jsonl"; :>"$MANIFEST"; :>"$ERRORS"
AWS=(aws --profile "$PROFILE" --region "$REGION" --no-cli-pager)
record(){ local id="$1" desc="$2" file="$3" cmd="$4" rc="$5" sha="" size=0; [[ -f "$file" ]] && { sha="$(sha256sum "$file"|awk '{print $1}')"; size="$(wc -c <"$file")"; }; jq -cn --arg id "$id" --arg description "$desc" --arg file "$(basename "$file")" --arg command "$cmd" --arg sha256 "$sha" --arg t "$(date -u +%FT%TZ)" --argjson rc "$rc" --argjson bytes "${size:-0}" '{collector_id:$id,description:$description,file:$file,command:$command,exit_code:$rc,sha256:$sha256,bytes:$bytes,collected_at:$t}' >>"$MANIFEST"; }
run(){ local id="$1" desc="$2" file="$3";shift 3; local tmp="$file.tmp" err="$file.stderr" cmd; printf -v cmd '%q ' "${AWS[@]}" "$@"; if "${AWS[@]}" "$@" >"$tmp" 2>"$err"; then mv "$tmp" "$file";rm -f "$err";record "$id" "$desc" "$file" "$cmd" 0; else local rc=$?;rm -f "$tmp";jq -cn --arg id "$id" --arg description "$desc" --arg command "$cmd" --arg error "$(cat "$err" 2>/dev/null||true)" --arg t "$(date -u +%FT%TZ)" --argjson rc "$rc" '{collector_id:$id,description:$description,command:$command,exit_code:$rc,error:$error,collected_at:$t}' >>"$ERRORS";rm -f "$err";record "$id" "$desc" "$file" "$cmd" "$rc";fi; }
jq -n --arg v "0.9" --arg t "$(date -u +%FT%TZ)" --arg p "$PROFILE" --arg r "$REGION" --arg av "$AWS_VER" --arg a "$AGENT_ID" --arg aver "$AGENT_VERSION" --arg m "$MODEL_ID" --arg ip "$INFERENCE_PROFILE_ID" '{collector_version:$v,collected_at:$t,profile_name:$p,region:$r,aws_cli_version:$av,agent_id:$a,agent_version:$aver,model_id:$m,inference_profile_id:$ip,privacy_mode:"configuration-only; no prompts/model invocations/log events/S3 objects"}' >"$OUT/_collector_meta.json"; record META "Collector metadata" "$OUT/_collector_meta.json" local 0
run COL-001 "Caller identity" "$OUT/00_identity.json" sts get-caller-identity
run COL-002 "Foundation models" "$OUT/10_foundation_models.json" bedrock list-foundation-models
[[ -n "$MODEL_ID" ]] && run COL-003 "Selected foundation model" "$OUT/11_selected_model.json" bedrock get-foundation-model --model-identifier "$MODEL_ID"
run COL-004 "Inference profiles" "$OUT/12_inference_profiles.json" bedrock list-inference-profiles
[[ -n "$INFERENCE_PROFILE_ID" ]] && run COL-005 "Selected inference profile" "$OUT/13_selected_inference_profile.json" bedrock get-inference-profile --inference-profile-identifier "$INFERENCE_PROFILE_ID"
run COL-006 "Invocation logging config" "$OUT/20_model_invocation_logging.json" bedrock get-model-invocation-logging-configuration
run COL-007a "Guardrails" "$OUT/30_guardrails.json" bedrock list-guardrails
run COL-008 "Enforced guardrails" "$OUT/31_enforced_guardrails.json" bedrock list-enforced-guardrails-configuration
run COL-009a "Agents" "$OUT/40_agents.json" bedrock-agent list-agents
ROLE_ARN=""
if [[ -n "$AGENT_ID" ]]; then run COL-009b "Selected agent" "$OUT/41_agent.json" bedrock-agent get-agent --agent-id "$AGENT_ID"; [[ -s "$OUT/41_agent.json" ]] && ROLE_ARN="$(jq -r '.agent.agentResourceRoleArn//empty' "$OUT/41_agent.json")"; run COL-010a "Action groups" "$OUT/42_action_groups.json" bedrock-agent list-agent-action-groups --agent-id "$AGENT_ID" --agent-version "$AGENT_VERSION"; run COL-011a "Agent KBs" "$OUT/43_agent_knowledge_bases.json" bedrock-agent list-agent-knowledge-bases --agent-id "$AGENT_ID" --agent-version "$AGENT_VERSION"; fi
if [[ -n "$ROLE_ARN" ]]; then ROLE_NAME="${ROLE_ARN##*/}"; run COL-012a "Agent role" "$OUT/50_iam_role.json" iam get-role --role-name "$ROLE_NAME"; run COL-012b "Attached policies" "$OUT/50_iam_attached_policies.json" iam list-attached-role-policies --role-name "$ROLE_NAME"; run COL-012c "Inline policies" "$OUT/50_iam_inline_policies.json" iam list-role-policies --role-name "$ROLE_NAME"; fi
[[ -n "$EXPLICIT_KMS_KEY" ]] && { run COL-014a "KMS key metadata" "$OUT/70_kms_describe.json" kms describe-key --key-id "$EXPLICIT_KMS_KEY"; run COL-014b "KMS key policy" "$OUT/70_kms_policy.json" kms get-key-policy --key-id "$EXPLICIT_KMS_KEY" --policy-name default; run COL-014c "KMS rotation" "$OUT/70_kms_rotation.json" kms get-key-rotation-status --key-id "$EXPLICIT_KMS_KEY"; }
run COL-015a "VPC endpoints" "$OUT/80_vpc_endpoints_all.json" ec2 describe-vpc-endpoints
[[ -s "$OUT/80_vpc_endpoints_all.json" ]] && { jq '{VpcEndpoints:[.VpcEndpoints[]?|select((.ServiceName//"")|test("bedrock";"i"))]}' "$OUT/80_vpc_endpoints_all.json" >"$OUT/80_vpc_endpoints_bedrock.json";record COL-015b "Bedrock VPC endpoint filter" "$OUT/80_vpc_endpoints_bedrock.json" "jq local filter" 0; }
run COL-016a "CloudTrail trails" "$OUT/90_cloudtrail_trails.json" cloudtrail describe-trails --include-shadow-trails
SUCCESS="$(jq -s '[.[]|select(.exit_code==0)]|length' "$MANIFEST")"; FAILED="$(jq -s '[.[]|select(.exit_code!=0)]|length' "$MANIFEST")"; jq -n --arg r "$REGION" --argjson s "$SUCCESS" --argjson f "$FAILED" '{collector_version:"0.9",region:$r,successful_evidence_steps:$s,failed_or_denied_steps:$f,manifest:"_manifest.jsonl",errors:"_errors.jsonl"}' >"$OUT/_run_summary.json";record SUMMARY "Run summary" "$OUT/_run_summary.json" local 0
echo "R6 evidence collection complete: $OUT"; echo "Successful: $SUCCESS | Failed/denied: $FAILED"; echo "No model invocation, prompt/log-event, or S3 object contents were collected."
