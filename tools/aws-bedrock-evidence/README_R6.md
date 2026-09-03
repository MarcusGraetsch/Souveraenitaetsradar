# Souveränitäts-Radar – R6 Technical Evidence Pilot

Zweck: technische, reproduzierbare Evidence für einen Amazon-Bedrock-Agenten sammeln, ohne den produktiven Zustand zu verändern.

## Sicherheitsprinzipien

- **Read-only:** nur `List`, `Get` und `Describe`.
- **Keine Modell-/Agentenaufrufe:** kein `InvokeModel`, `Converse`, `InvokeAgent` oder `ApplyGuardrail`.
- **Keine Nutzdaten:** keine Prompt-/Response-Inhalte, keine CloudTrail/CloudWatch Log Events, keine S3-Objekte.
- **Chain of custody:** jeder erfolgreiche Raw-Evidence-Output erhält SHA-256, UTC-Zeit und den ausgeführten CLI-Befehl im `_manifest.jsonl`.
- **Best effort:** `AccessDenied` oder nicht vorhandene Ressourcen werden als Evidence Gaps in `_errors.jsonl` protokolliert; der Lauf geht weiter.

## Voraussetzungen

- AWS CLI **v2**
- `jq`
- `sha256sum`
- ein autorisierter AWS-CLI-Profile-Kontext mit den benötigten Read-Rechten
- idealerweise: Region, Bedrock `AGENT_ID`, `MODEL_ID`, `INFERENCE_PROFILE_ID`

## Start

```bash
chmod +x sovradar_aws_evidence_collect.sh
./sovradar_aws_evidence_collect.sh \
  --profile my-profile \
  --region eu-central-1 \
  --agent-id ABCDEFGHIJ \
  --agent-version DRAFT \
  --model-id provider.model-id \
  --inference-profile-id some-profile-id
```

Danach:

```bash
python3 r6_normalize_evidence.py ./r6_evidence/<timestamp>_eu-central-1
```

Wichtige Outputs:

- `_manifest.jsonl` – Provenienz/Hashes
- `_errors.jsonl` – AccessDenied/fehlende APIs
- `normalized_evidence.json` – normalisierte technische Facts
- `technical_findings.json` – erste deterministic findings

## Was R6 technisch klären kann

- ausgewähltes Bedrock-Modell / Inference Profile
- Bedrock Invocation Logging Konfiguration
- Guardrails / account-level enforced guardrails
- Bedrock Agent Service Role, Action Groups, Knowledge Bases
- IAM Role/Policies
- Lambda Resource Policies für Action Groups
- KMS Key-Metadaten/Policy/Rotation
- Bedrock PrivateLink/VPC Endpoints
- CloudTrail Trails/Event Selectors
- CloudWatch Log Group Retention
- Metadaten des S3 Logging Buckets

## Was R6 **nicht** allein klären kann

- juristische Transfer-/CLOUD-Act-Bewertung
- tatsächliche Wirksamkeit der Controls ohne Tests
- Exit-Fähigkeit ohne Migrationstest
- autonome Betriebsdauer ohne Exercise
- C5-Trust-Level 5 ohne den tatsächlichen Prüfbericht
- organisatorischen Risikoappetit

## IAM Policy

`r6_collector_readonly_policy_template.json` ist ein **technisches Referenztemplate**, kein finaler Least-Privilege-Produktionsstandard.
Es enthält ausschließlich Leseaktionen, ist aber absichtlich noch relativ breit mit `Resource: "*"`, damit der Pilot nicht an uneinheitlicher Resource-Level-Unterstützung scheitert.
Für einen echten Kundeneinsatz sollte es auf konkrete Agent-/Role-/KMS-/Lambda-Ressourcen und den Assessment-Account zugeschnitten werden.

## Weiterverarbeitung im Radar

R6 führt den zusätzlichen Zustand ein:

`available -> selected -> configured -> tested -> attested`

Ein Service kann eine Fähigkeit anbieten (`available`), ohne dass der konkrete Workload sie tatsächlich nutzt. Nur `configured/tested/attested` kann – abhängig vom Gate – einen belastbaren Applied-Capability-PASS begründen.
