# NordicHealth — privacy review questions

**Fictional scenario; no real personal data.** This document contains invented categories and possible harms, not records about identifiable people. It is an assessment prompt, not a completed DPIA, legal opinion, processing authorization or signed approval. The [scenario](README.md), [risk assessment](RISK-ASSESSMENT.md) and [control sample](SOA-EXCERPT.md) define its limited scope.

## Separate operational impact from harm to people

An outage, investigation cost or supplier failure describes consequences for the organization. A privacy review separately asks what a person could lose: confidentiality, autonomy, fair treatment, access to services or control over information about them. Security scores can help prioritize work but do not establish that processing is lawful or proportionate.

The table contains plausible exercise scenarios; none is an observed incident or quantified impact.

| Risk(s) | Operational concern | Possible consequence for people | Evidence or question needed |
|---|---|---|---|
| R01, R03 | Account misuse or incorrect partner authorization | Appointment context or documents disclosed to an unintended person; distress or unfair treatment from sensitive inferences | Map fields, recipients, access scope and affected groups; test authorization with synthetic identities. |
| R02, R05 | Scheduling interruption or unavailable supplier | Delayed administration and difficulty arranging or changing an appointment | Establish service dependencies and safe alternatives; do not infer clinical outcomes from this administrative case. |
| R04, R07 | Lost device or compromised software | Disclosure or alteration of cached information; misuse of an active session | Determine what is stored locally, session reach, device custody and effective revocation. |
| R06 | Unnecessary copies and uncertain deletion | Continued exposure of details after their purpose ends; difficulty exercising information rights | Establish purposes, necessary fields, copy locations, deletion exceptions and how requests would be handled. |
| R08 | Missing records or delayed investigation | Misuse persists; affected people cannot be accurately informed about what happened | Assess event coverage and investigation capability while limiting unnecessary staff or service-user monitoring. |

Privacy concerns extend beyond security failures. Even a correctly functioning system could collect excessive details, obscure its purpose or retain information without a reviewed need. C06 and C08 therefore require privacy review alongside technical testing.

## Decisions deliberately left open

| Decision | Information required before a decision | Current position / suggested reviewer |
|---|---|---|
| Processing inventory and roles | Purpose per activity; categories and people affected; recipients; supplier/subprocessor roles; locations and transfers; data flows and copies | Unresolved. Records lead and service owner to assemble; privacy/legal reviewer to assess roles. |
| Lawfulness and sensitive information | Facts supporting a lawful basis for each purpose; whether health-related or other special-category information is actually processed; applicable conditions and duties | No basis or condition selected. Privacy/legal reviewer to assess before any real processing is authorized. |
| Necessity, proportionality and transparency | Why each field/use is needed; less intrusive options; proposed notices; how access, correction and other applicable requests would be handled | Unresolved. Service owner and privacy reviewer to review with the intended users' context. |
| Retention and deletion | Purpose-specific needs and applicable obligations; copy/backup paths; deletion capability; exceptions and restoration handling | No duration selected. Records lead and privacy/legal reviewer to document a reasoned schedule before implementation. |
| Supplier and transfer arrangements | Actual parties and services; responsibility allocation; access and location evidence; applicable contract/transfer requirements | No agreement or transfer conclusion supplied. Administration lead and privacy/legal reviewer to assess. |
| DPIA screening and follow-through | Nature, scope, context and purpose; scale and affected groups; foreseeable harms; proposed safeguards; documented screening rationale | Whether a DPIA is required remains unresolved. Complete and review one if required; identify any further consultation obligations from the resulting facts. |
| Security records and staff privacy | Needed event fields, authorized audiences, review purpose, retention rationale and monitoring implications | No blanket logging or retention approval. Security lead and privacy reviewer to assess. |

Datatilsynet describes DPIA as a process addressing the proposed processing, necessity and proportionality, and risks to people's rights and freedoms. It also explains that a DPIA cannot make unlawful processing lawful. This case therefore keeps the lawfulness review and DPIA screening open rather than deriving either conclusion from a security score. [Datatilsynet DPIA guidance](https://www.datatilsynet.no/rettigheter-og-plikter/virksomhetenes-plikter/vurdering-av-personvernkonsekvenser/) (rechecked 31 October 2026).

## Evidence handling and review

Portfolio examples and tests must use invented identifiers and synthetic payloads. Do not add patient records, real support messages, account exports or production logs to this public exercise. A real implementation would need an approved way to obtain and protect evidence; a public portfolio would receive only appropriately reviewed summaries.

Record the proposed decision, supporting facts, reviewer role, limitations and review trigger before seeking authorization. No reviewer has approved this scenario. [REVIEW-GATES.md](REVIEW-GATES.md) identifies the unresolved decisions; [controls.json](controls.json) records C06 and C08 as proposed with no implementation evidence. A scope, supplier, data-category, purpose or integration change would reopen the relevant review.
