# Executed verification — 31 October 2026

The final structured case passed validation with **8 assets, 8 risks, 8 treatments and 10 control decisions**, with zero reported errors. The validator's **22 unit tests passed**. These are actual local Python checks of artifacts and validator behavior, not tests of organizational control effectiveness.

- [Validation report](validation-report.json): input hashes, counts, outcome and check scope.
- [Unit test output](unit-tests.txt): named tests and final result.
- [Execution record](run-environment.json): observed time, Python version, exit codes and tested source/data hashes.

Tests cover rating boundaries, impact-5 escalation even at a score of 5, critical-score escalation, missing flags, duplicate/orphan references, reciprocal mappings, incorrect scores/bands, invalid numeric types, false implemented/accepted statuses, exclusion reasons, malformed/missing inputs, duplicate JSON properties, report privacy and CLI exits. They use disposable local fixtures; no network or external business system is accessed.

During preparation, the initial Markdown draft lacked numeric score cells on seven rows; these were corrected before structured extraction and release. Early unit-test fixtures hit the host's default temporary-directory permissions, so the tests use and clean up their own project-local temporary folders. Review also found that a missing escalation flag could pass; the field is now required and a regression test covers it. Final evidence above was captured after these corrections.

Manual release review checked the fictional scope, unchanged pending approvals, risk/control/treatment agreement, source references and the two limited exclusions. C09/C10 do not exclude device physical protection or supplier assurance. The applicability sample remains incomplete as an ISO Annex A assessment, and the privacy review remains a set of unanswered operational questions.

Reproduce using the commands in [README](../README.md). A fresh report has a different timestamp. Passing checks do not certify a risk rating, lawful processing, complete control coverage, implemented safeguards or personal proficiency.
