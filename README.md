# ATLAS NordicHealth GRC case

A fictional governance, risk and compliance exercise connecting **8 assets, 8 risk assessments, 8 proposed treatments and 10 applicability decisions**. The practical result is a traceable assessment package plus executable checks of its consistency.

**No real company or personal records are assessed.** NordicHealth is an invented scenario, unrelated to any organization with that name. All ratings, owners and controls are exercise assumptions. Operational approvals remain pending; actual residual risk is unknown. This is not a certification, legal opinion, completed DPIA or proof of implemented security controls.

## Start here

- [Decision brief](CASE-SUMMARY.md): scope, priorities and evidence needed before decisions.
- [Risk assessment and treatment plan](RISK-ASSESSMENT.md): scales, rationales, accountable roles and proposed review windows.
- [Applicability excerpt](SOA-EXCERPT.md): eight proposed controls and two justified scope exclusions. This is a limited SoA sample, not a complete ISO/IEC 27001 Annex A assessment.
- [Privacy review](PRIVACY-REVIEW.md): possible harms to people and decisions that remain unresolved.
- [Review gates](REVIEW-GATES.md): evidence and authority required before implementation or risk acceptance.
- [Verification record](evidence/VERIFICATION.md): actual local artifact checks, test results and limitations.

## Scenario

Assume a 40-person outpatient administration provider using supplier-hosted appointment, document, identity and support services. Staff laptops and supplier physical-security assurance are included. No organization-operated datacenter, clinical decision system, emergency-care service, industrial/OT system or medical device is in scope. Changes to these assumptions would reopen the relevant exclusions.

No patients, staff accounts or business systems were accessed. The project uses Python's standard library, local JSON and Markdown. It needs no VM, Docker, cloud service, credentials, license purchase or dependency installation. No CI workflow or infrastructure deployment is included.

## Structured records and reproducibility

The current structured sources are [register.json](register.json), [treatments.json](treatments.json) and [controls.json](controls.json). [scenario-seeds.json](scenario-seeds.json) is the preserved initial design snapshot from 29 October; its draft status is historical. The structured assessment was reviewed on 31 October 2026.

Run from the repository root with Python:

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
```

To save a separate local report:

```sh
python scripts/validate.py --output evidence/local-validation.json
```

The validator checks IDs and reciprocal references, numeric types/ranges, recalculated scores/bands, escalation flags, justified exclusions and the proposed/pending statuses required by this case. It returns a failing exit code for invalid inputs and records their SHA-256 hashes. Unit tests include deliberately invalid copies, boundary values, malformed JSON and CLI behavior. No operational control or legal judgment is evaluated by those tests.

The 1–5 ratings are ordinal assumptions. Their product prioritizes review; it is not an annual probability, expected financial loss or automatic acceptance decision. Impact 5 requires escalation even with a modest product score. A proposed target or passing artifact check cannot establish an actual residual risk. Error reports can include local diagnostic paths; review them before sharing.

## Sources and scope of mapping

[ISO's official overview](https://www.iso.org/standard/27001) supplies ISMS context; this project does not reproduce or assess the full normative standard. Control identifiers C01–C10 are local identifiers. Selected principle references use [NSM v2.1](https://nsm.no/getfile.php/1313975-1717589722/NSM/Filer/Dokumenter/Veiledere/NSMs%20Grunnprinsipper%20for%20IKT-sikkerhet%20v2.1.pdf); their mapping is an exercise judgment. The [Datatilsynet DPIA guidance](https://www.datatilsynet.no/rettigheter-og-plikter/virksomhetenes-plikter/vurdering-av-personvernkonsekvenser/) informs the unresolved privacy questions. Sources were rechecked on 31 October 2026.

The case demonstrates preparation and validation of portfolio artifacts. It makes no claim about an individual's independent proficiency or a real organization's compliance.
