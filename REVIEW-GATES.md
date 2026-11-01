# NordicHealth — unresolved operational review gates

**Fictional roles and proposed decisions only.** Every gate below is `pending`. No approval, contract, risk acceptance or authority to process real personal data is represented. Suggested reviewers identify needed responsibilities; no named person has accepted a role.

These gates govern hypothetical adoption of the [case](README.md). Publishing a clearly labelled portfolio artifact can demonstrate the reasoning while the operational gates remain pending. Local consistency checks verify records and links; they do not implement controls or grant operational approval.

| Gate | Proposed decision and reviewer roles | Evidence needed before a real decision | Related records |
|---|---|---|---|
| G01 Scope and accountability | Service sponsor and asset owners confirm boundaries, dependencies and decision authority | Verified asset/data-flow inventory; supplier-hosting responsibilities; confirmation of no organization-operated datacenter or OT; review of staff-device physical protection and excluded-service dependencies | [Scope](README.md); C04, C05, C09, C10 in [controls.json](controls.json) |
| G02 Processing purpose and lawfulness | Service owner with an appointed privacy/legal reviewer assesses proposed activities | Purpose/category/recipient inventory; actual organizational roles; necessary fields; supported lawful-basis and, where relevant, sensitive-data analysis; transparency and rights-handling design | [Privacy questions](PRIVACY-REVIEW.md); C03, C06, C08 |
| G03 Retention and deletion | Records lead with privacy/legal review decides a reasoned schedule | Applicable obligations and business needs; copy/backup locations; exceptions; synthetic deletion and restore-handling results; a method to verify actual coverage | R06 / T06; C06 |
| G04 Privacy risk and DPIA | Service owner with privacy expertise documents screening and required follow-through | Processing context and affected groups; necessity/proportionality analysis; harms and safeguards; documented DPIA decision and, if required, completed review and any further consultation assessment | [Privacy review](PRIVACY-REVIEW.md); all in-scope processing |
| G05 Supplier assurance and dependencies | Administration lead with privacy/legal and technical reviewers assesses arrangements | Responsibility/access records; recovery and exit evidence; supplier physical-security assurance; reviewed agreements and transfer arrangements as applicable; limitations and dependency exercise | R05 / T05; C05; C10 exclusion boundary |
| G06 Control implementation and effectiveness | Treatment owners implement; an appropriate reviewer evaluates evidence | Scoped configuration and test records for T01–T08; test dates and versions; positive/negative outcomes; coverage gaps, failed tests and remediation; no borrowed evidence from unrelated labs | [Risk and treatment evidence](RISK-ASSESSMENT.md); [control sample](SOA-EXCERPT.md) |
| G07 Residual risk and acceptance | Accountable risk owners and authorized management decide after reassessment | G01–G06 outcomes as relevant; demonstrated implementation; revised likelihood/impact rationale; remaining uncertainty; conditions, review dates and explicit decisions; escalation of every impact-5 risk regardless of score | R01–R08 in [assessment](RISK-ASSESSMENT.md) |
| G08 Full applicability and ongoing review | Service sponsor and ISMS owner, if appointed, review wider coverage | Complete relevant control reference and obligation review; justified selection/exclusion decisions; evidence and change/review process beyond this sample | [SoA limitations](SOA-EXCERPT.md) |

## Decision record requirements

For each real review, record the exact scope and version reviewed, evidence references, decision-maker authority, outcome and rationale, conditions, unresolved exceptions, decision date and next review trigger. A proposed role or empty template is not a sign-off. An implementation test does not resolve lawfulness, and a privacy review does not demonstrate technical effectiveness.

Keep actual residual risk `unknown` and acceptance `pending` until evidence and authorized decisions exist. Proposed target scores are design expectations only. A failed or uncovered test must remain visible; it cannot be converted into a successful result by lowering the score. Review again when the service, data, supplier, integration, threat exposure or control design changes.

## Portfolio release review

Before release, review fictional labelling, absence of real personal data and secrets, consistency of assets/risks/treatments/controls, working internal links, accurate sources, and clear separation of proposed design from observed evidence. Record only checks actually completed. Release of these documents does not close G01–G08 or establish certification, compliance or an operational deployment.

See [PRIVACY-REVIEW.md](PRIVACY-REVIEW.md) for unresolved privacy facts and [SOA-EXCERPT.md](SOA-EXCERPT.md) for the deliberately limited applicability sample.
