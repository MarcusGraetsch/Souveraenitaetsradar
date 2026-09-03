# ADR-0008 – Provider adapters are translation-only

Status: accepted – 2026-09-03

Provider adapters translate provider-specific terminology or customer-generated export formats into generic Facts/Capabilities. They must not implement risk acceptance, provider-specific gate thresholds or live credential collection.

This keeps AWS, Azure, GCP, OpenStack, Kubernetes, sovereign cloud and SaaS behind the same method core.
