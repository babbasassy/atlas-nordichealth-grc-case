# NordicHealth — initial fictional risk assessment

Assessment date: 29 October 2026. This is an exercise judgment based only on the invented scenario in the README. Existing controls have not been inspected. All acceptance decisions are pending. Proposed improvements are not current residual-risk measurements.

## Scales and decision rules

Likelihood is ordinal: 1 requires exceptional circumstances; 2 requires several enabling conditions; 3 is plausible given the stated exposure; 4 has common opportunities and weak assumed barriers; 5 has repeated, readily available opportunities. These labels are scenario judgments, not calibrated annual probabilities.

Impact is also ordinal: 1 minor reversible inconvenience; 2 limited disruption or limited disclosure; 3 significant service or confidentiality harm; 4 major sustained disruption or serious harm to affected people; 5 extensive sensitive disclosure or prolonged loss of an essential administrative service. Consider confidentiality, integrity, availability and harm to people; use the most severe credible impact, not their average. Actual consequences depend on scope, volume and dependencies that this fictional case assumes.

Score = likelihood × impact. Exercise bands: 1–4 low, 5–9 moderate, 10–16 high, 17–25 critical. Every critical-score risk and every impact-5 risk needs escalation, regardless of the latter's score. Low scores are not automatic acceptance. The accountable risk owner must review scope, uncertainty and evidence; no real approval is represented here. Proposed review periods below run from a hypothetical approval date, not today's date.

## Register

| Risk | Assets | Accountable role | L | I | Score | Rationale for assumed exposure and impact |
|---|---|---|---:|---:|---:|---|
| R01 Credential theft | A01, A03 | IT operations lead | 4 | 5 | 20 | Routine external sign-in and document access create opportunities. Assume strong authentication and access review are not evidenced. Broad document disclosure is the severe scenario; actual access scope is unknown. |
| R02 Unrecoverable disruption | A02, A06 | Administration lead | 3 | 5 | 15 | Destructive error or ransomware is plausible. Assume recoverability and separation of backup administration are untested. Scheduling could remain unavailable without a usable restore path. |
| R03 Partner authorization error | A04, A02 | Integration lead | 3 | 5 | 15 | Multiple partner contexts make an authorization mistake plausible. An incorrect tenant/object check could disclose appointments across customers; scope of exposure has not been measured. |
| R04 Lost laptop | A05 | IT operations lead | 3 | 4 | 12 | Portable devices can be misplaced. Assume encryption and session handling are unverified. Cached documents or reusable sessions could cause serious disclosure. |
| R05 Supplier disruption or excess access | A02, A07 | Administration lead | 3 | 4 | 12 | A supplier is a service and access dependency. Assume continuity obligations and privileged access boundaries have not been reviewed. Disruption and support-record disclosure are distinct impacts requiring review. |
| R06 Excess retention | A03, A07 | Records lead | 4 | 4 | 16 | Routine copying into documents/support cases creates repeated opportunities for unnecessary retention. Accumulation can increase privacy harm and the scope of a later disclosure. No lawful retention duration is assumed. |
| R07 Unaddressed weakness | A05, A04 | IT operations lead | 3 | 4 | 12 | Exposed integrations and device software may contain weaknesses. Assume ownership and patch verification are not demonstrated. Unauthorized changes or access could affect several administrative services. |
| R08 Detection gap | A08, A01 | Security lead | 4 | 4 | 16 | Assume log coverage, retention and review are unverified. Undetected misuse could persist and evidence might be unavailable for investigation. This amplifies other risks; scores must not be summed as independent loss estimates. |

## Proposed treatment and acceptance evidence

All rows have status **proposed**, implementation evidence **none**, current residual risk **unknown**, and acceptance **pending**.

| Treatment | Risk | Suggested review window | Proposed work | Evidence needed before reassessment |
|---|---|---|---|---|
| T01 | R01 | T+7 days | Review authentication strength, recovery paths, access scope and privileged roles. | Scoped policy export, test sign-in outcomes, role-review record and recovery-path test; validate all relevant identities, not a single example. |
| T02 | R02 | T+7 days | Separate backup administration and define service recovery needs with the service owner. | Restore an isolated representative backup, record recovered completeness and elapsed recovery against approved needs; assess dependencies and backup access separately. |
| T03 | R03 | T+7 days | Specify object/customer authorization and test positive and cross-customer negative cases. | Reproducible request/response evidence with synthetic identities; every relevant API operation covered or explicitly listed as untested. |
| T04 | R04 | T+30 days | Establish device inventory, encryption evidence and lost-device/session procedure. | Inventory coverage, encryption/recovery-key governance and a safe revocation exercise; no claim based only on a written policy. |
| T05 | R05 | T+30 days | Review supplier roles, access scope, service recovery and exit arrangements. | Reviewed responsibilities, access evidence, supplier assurance limitations and a tabletop dependency test. No contract or service commitment is signed by this exercise. |
| T06 | R06 | T+30 days | Map purpose and data categories; obtain a reasoned retention/deletion decision and assess privacy risks. | Approved rationale, legal/privacy review where needed, synthetic deletion and restore-handling test, and evidence of exceptions. A deletion job alone does not establish lawful processing. |
| T07 | R07 | T+30 days | Inventory versions, prioritize applicable weaknesses and verify remediation. | Scoped scan/version evidence before and after, applicability rationale, supported-version checks and time-limited exception decisions. |
| T08 | R08 | T+30 days | Define audit sources, access, retention, alert ownership and investigation workflow. | Synthetic test events traced from source to review, failure/missing-source checks and an incident exercise; do not infer business coverage from the separate ATLAS Wazuh lab. |

Proposed success criteria are evidence requests, not completed controls. Assign target likelihood/impact only after reviewing these designs; replace them with an evidence-based residual assessment only after implementation. Reassess whenever the scenario, data categories, supplier, integration or threat exposure changes. A privacy/DPIA screening and a complete applicability review remain outstanding.
