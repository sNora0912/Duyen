# Duyen: Pragmatic Naturalness in Vietnamese LLM Output

Data, annotation guideline, and scripts for the paper

> Nguyen Duc Hieu Phung and Tunn Cho Lwin. **Duyen: Measuring Pragmatic Naturalness in Vietnamese LLM Output.** In: Proceedings of VTCA 2026, Smart Innovation, Systems and Technologies, Springer (to appear).

Vietnamese marks the social relationship between speaker and addressee in almost every utterance, through kinship-based address terms, deference words, and utterance-final particles. A model can produce grammatical Vietnamese that is still socially wrong. Duyen treats the appropriateness of these choices, *pragmatic naturalness*, as a measurable axis for LLM output, with a compact label set and a written guideline.

## Contents

| Path | Description |
|---|---|
| `guideline/GUIDELINE-v1.0.md`, `.pdf` | Annotation guideline v1.0, frozen before annotation began. Vietnamese with English glosses. |
| `data/scenarios.csv` | The 42 scenarios: 30 base (N-01 to N-30) and 12 adversarial (H-01 to H-12), with relationship metadata, the Vietnamese prompt, and the designed opportunities (the error types each scenario was built to probe, fixed in advance). |
| `data/outputs.csv` | The 126 raw outputs: each scenario sent to three LLMs on 26 August 2026. |
| `data/annotation_30.csv` | The doubly annotated subset: 25 sampled outputs and 5 control sentences, with the curator's labels and notes, the second annotator's labels, and the AI judge's labels and notes. |
| `data/controls.csv` | The 5 constructed control sentences and their design notes. |
| `data/sampling/` | The exact input file and script used to draw the annotation sample (seed 42). |
| `generation/README.md` | How the outputs were generated, including the one-line chatbot instructions given to two of the generators. |
| `judge/prompt_template.txt` | The exact prompt given to the AI judge. |
| `scripts/reproduce_tables.py` | Recomputes Tables 3–5 and the counts reported in Section 4.1 of the paper. |

## Label set

An item may carry several labels, separated by `;`. `NONE` means no pragmatic problem.

| ID | Label | Short test |
|---|---|---|
| PR1 | Wrong address term | Address term does not fit the addressee's age or status |
| PR2 | Address and self term do not match | Self term is not the licensed partner of the address term |
| PR4 | Textbook-neutral pair | *tôi* and *bạn* used together where kin terms are required |
| PF1 | Missing deferential word | Upward speech without *dạ*, *thưa*, or *vâng* where expected |
| PF2 | Missing request softening | Upward request without *giúp…với*, *làm ơn*, or *phiền* |
| FP1 | Missing respect particle *ạ* | Upward greeting, answer, or request not ending in *ạ* |
| FP2 | Missing alignment particle | Peer proposal or shared remark without *nhé* or *nhỉ* |
| NONE | No pragmatic problem | Natural as written |
| OTHER | Outside the seven types | Unnatural in a way not covered above; a note is required |

PR2, PF1, and FP1 are the three core types, fixed in advance as the focus of the reliability analysis. PR3 is reserved for cross-turn address switching, which is out of scope for single-turn items.

## Reproducing the tables

```bash
python3 scripts/reproduce_tables.py
```

Python 3.8 or later, standard library only.

To regenerate the blind annotation packet from the original input file:

```bash
cd data/sampling
python3 make_annotator2_sheet.py --force
```

The input file `Duyen-Pilot-Sheet.csv` has SHA-256 prefix `a43ced3301`; its model labels carry the date 25/8/2026, which was a stale date in the generation harness (the runs took place on 26 August 2026). The script writes the packet to `to-send/` and the key to `_private/` inside `data/sampling/`.

## How the labels were produced

- **Curator.** A native Northern Vietnamese speaker and the first author wrote a free-text judgment for each item, with a correction where needed (`curator_note_vi`). An AI assistant converted these judgments into labels with a fixed rule: an output usable as written is `NONE`; a relational problem that must be fixed receives its type, or `OTHER`. The curator checked the result and decided the cases the rule left open.
- **Second annotator (A2).** A second native Northern Vietnamese speaker labeled the 30 items blind, seeing only the relationship description and the text. A2's free-text notes are not released.
- **AI judge.** Claude through the Claude Agent SDK, alias `fable` resolved to `claude-fable-5`, one fresh context per item, run on 1 September 2026 with the prompt in `judge/prompt_template.txt`. The judge ran after A2's labels were collected and saw no human labels.
- **Notes.** The curator's and the judge's notes are in Vietnamese. Two curator notes were reworded for publication to remove a pejorative term; their meaning and labels are unchanged.
- **Scope.** Gold labels and corrections currently cover the 30-item subset. Labels for the remaining 101 outputs are in progress and will be added to this repository.

## License

The data and the guideline are licensed under [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (see `data/LICENSE.md`). The code is licensed under the MIT License (see `LICENSE`).

## Ethics

All annotated text is model-generated or was constructed by the authors; no personal data were collected. The second annotator took part voluntarily and is not identified.

## Contact

Corresponding author: Tunn Cho Lwin, tlwin@miu.ac.jp. Questions about the data can also be raised as GitHub issues.

## Citation

```bibtex
@inproceedings{phung2026duyen,
  title     = {Duyen: Measuring Pragmatic Naturalness in {Vietnamese} {LLM} Output},
  author    = {Phung, Nguyen Duc Hieu and Lwin, Tunn Cho},
  booktitle = {Proceedings of the 8th International Conference on Smart Vehicular Technology,
               Transportation, Communication and Applications (VTCA 2026)},
  series    = {Smart Innovation, Systems and Technologies},
  publisher = {Springer},
  year      = {2026},
  note      = {To appear}
}
```
