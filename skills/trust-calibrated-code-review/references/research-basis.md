# Research basis: what the source does and does not establish

Source: Lo Gullstrand Heander et al., *Trust-Calibrated Code Review: A Participatory Design Study of Review Workflows for LLM-Generated Multi-File Changes*, ESEM 2026, DOI: 10.4230/LIPIcs.ESEM.2026.89.

Source-supported concepts:
- **Trust calibration**: allocate review effort by segment risk when generated code offers uniform apparent confidence (pp. 1, 8, 14-16).
- **Three levels**: overview (change-set reasoning), file analysis (file risk and limits), code snippet review (cohesive chunks) (pp. 8-11, Table 2 on p. 10).
- **Seven design constructs**: chunk, risk-per-line, risk-per-file, Judge, walk-through, zooming in/out, security cage (pp. 10-12).
- **Chunk**: smallest subset of proposed changes that could apply together without breaking compilation/tests, in their conceptual definition. In practical reviews, establish actual independence empirically, or use only semantic chunking (pp. 9-11).
- **Risk-per-file/line**: varying potential consequences; participant sketch suggested history/change frequency as one input, but it is not validated as a quantitative risk model (pp. 9-11).
- **Judge**: model-provided issue/security/fact-checking verdict for reviewer attention, not an authority; paper explicitly notes Judge's own opacity (pp. 11, 14-15).
- **Security cage**: bound agent actions; reception was mixed and location of sandboxing within review versus agent settings remains contested (pp. 11, 13, 14-15).
- **Walk-through**: explain reconstructed rationale and implementation choices, while LLM explanation may be post-hoc and unreliable (pp. 3, 11).

Validation: survey of 43 practitioners rated overview 3.50, file analysis 3.69, chunk review 3.91 on a 1-5 scale; 63% anticipated reduced overall review effort and 52% reduced trust assessment effort (pp. 10, 12-13). Semi-interactive prototype was shown through video; study did **not** measure defects detected, actual review speed, review precision, or merge outcome (pp. 13, 17).

This skill **adds** operational review checklists, heuristic scoring, severity definitions, evidence standards, safety gates, test log and merge decisions. None of these additions should be falsely attributed as empirically validated by the paper.
