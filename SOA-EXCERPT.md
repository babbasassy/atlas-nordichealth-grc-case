# NordicHealth — illustrative applicability register

**Fictional case; scoped sample only.** This register records case-specific control choices. It is not a complete ISO/IEC 27001 Annex A assessment, a formal organization-wide Statement of Applicability, or a certification or compliance claim. C01–C10 are local identifiers, not ISO control numbers. The public [ISO/IEC 27001 overview](https://www.iso.org/standard/27001) provides ISMS context; the full standard has not been assessed here.

The [scenario](README.md) assumes supplier-hosted administrative services, staff laptops and an external service desk. Clinical decisions, medical devices and industrial/operational technology are excluded. There is no assumed organization-operated datacenter or server room. These invented boundaries require confirmation before any real application.

## Proposed applicability

The structured record is [controls.json](controls.json). Each applicable row maps to its corresponding risk and treatment in the [assessment](RISK-ASSESSMENT.md). All applicable controls have status `proposed` and evidence status `not_implemented`: no NordicHealth implementation or effectiveness is demonstrated. The NSM identifiers reproduce the [scenario seeds](scenario-seeds.json); the mapping is an exercise judgment using [NSM v2.1](https://nsm.no/getfile.php/1313975-1717589722/NSM/Filer/Dokumenter/Veiledere/NSMs%20Grunnprinsipper%20for%20IKT-sikkerhet%20v2.1.pdf), not an NSM endorsement or exhaustive mapping.

| Control | Applies | Risk / treatment | NSM principles | Case-specific justification and evidence focus |
|---|---|---|---|---|
| C01 Authentication, recovery and privileged access | Yes | R01 / T01 | 2.6 | Document access depends on identities. Request scoped policy, sign-in/recovery tests and privilege-review evidence. |
| C02 Backup administration and recovery exercise | Yes | R02 / T02 | 2.9, 4.1 | Scheduling requires usable records. Request a representative isolated restore and measured recovery against approved service needs. |
| C03 Partner authorization and exchange boundaries | Yes | R03 / T03 | 2.1, 2.5 | Partner requests cross customer boundaries. Request synthetic positive and cross-customer negative tests covering relevant operations. |
| C04 Laptop custody and lost-device response | Yes | R04 / T04 | 1.2, 2.6, 2.7 | Portable devices can expose cached information and sessions. Review inventory, custody/storage arrangements, encryption, recovery-key governance and revocation tests. |
| C05 Supplier responsibilities and continuity | Yes | R05 / T05 | 1.1, 2.1, 4.1 | Hosted services and support depend on suppliers. Review access, recovery, exit, responsibility boundaries and supplier physical-security assurance. |
| C06 Purpose, retention and deletion | Yes | R06 / T06 | 1.1, 2.5 | Documents and support copies can outlive their purpose. Request reasoned privacy decisions and synthetic deletion/restore tests; security references do not settle legality. |
| C07 Weakness ownership and remediation | Yes | R07 / T07 | 3.1, 2.10 | Device/API weaknesses need owners and verified changes. Request applicability, version and before/after remediation evidence with explicit exceptions. |
| C08 Audit coverage and incident exercise | Yes | R08 / T08 | 3.2, 3.3, 4.2 | Misuse may remain undetected. Trace synthetic events to review, test missing sources and exercise incident classification. |
| C09 Industrial/OT safeguards | No | None | None assigned | No industrial process, OT or medical-device operation is within the invented scope. Reassess if assets, interfaces or responsibilities change. |
| C10 Organization-operated datacenter safeguards | No | None | None assigned | No organization-operated datacenter, server room or facility plant is assumed. Direct facility operation is excluded; supplier assurance remains in C05 and staff-device physical protection remains in C04. |

C09 and C10 have status and evidence status `not_applicable`. Their detailed reasons in [controls.json](controls.json) are conditional scope decisions, not evidence that all physical or dependency risks have been addressed. A missing control from this sample is **unassessed**, not implicitly excluded. No Annex A control is declared inapplicable by omission.

## Outstanding review

A full applicability exercise would need a confirmed scope, applicable obligations, complete control reference, justified selections and exclusions, and implementation evidence. The portfolio does not supply those results. Review privacy questions in [PRIVACY-REVIEW.md](PRIVACY-REVIEW.md) and keep operational approvals open in [REVIEW-GATES.md](REVIEW-GATES.md). Low target scores and successful artifact checks cannot close those gates.

Sources above rechecked 31 October 2026. Control descriptions and evidence requests are original proposals for this fictional case.
