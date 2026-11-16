# Changelog

Release v1.0 (commit `1fb667c`, 5 October 2026) is the version described in the VTCA 2026 paper. Nothing below changes a label, and `scripts/reproduce_tables.py` prints the same numbers before and after. Dates are in UTC.

## 16 November 2026: documentation

- Added this changelog.
- `data/annotation_30.csv`, item N-02: appended a dated addendum, in Vietnamese, to `curator_note_vi`. The original note is kept as it was. The addendum records the curator's two later decisions on this item.
- `README.md`: named the two items whose labels the curator decided, and pointed to this file.

## Label decisions by the curator (already part of v1.0)

The curator's free-text notes were converted into labels on 1 September 2026 by an AI assistant with a fixed rule. The rule left two items open, because the note alone did not settle them, and the curator decided both. The assistant that did the conversion had seen the AI judge's output, as Section 3.5 of the paper states.

| Item | Label in v1.0 | What the note says | Decision |
|---|---|---|---|
| N-02 | `OTHER;PR1;PR2` | The note rewrites only the offer of coffee and adds *ạ* to it (`OTHER`). It keeps *anh/chú*, and it was written before the question in the next column was asked. | Asked whether *chú/anh* and *em* fit an addressee old enough to be the speaker's grandfather, the curator answered on 1 September 2026 that the address term should be *ông* (`PR1`). `PR2` was added in the same conversion step, because the self term *em* pairs with neither *chú* nor *ông*; the fitting self term is *cháu*. The curator confirmed `PR2` on 4 October 2026. |
| C-01 (control) | `NONE` | "ok" | The conversion had set `PR1` by analogy with N-02, without a decision from the curator. On 4 October 2026 the curator restored `NONE`, in line with his note. |

Where N-02 enters the reported numbers: it is the one error at a designed opportunity in Table 3 (`PR1`), one of the curator's two core-type labels in Section 4.1 (`PR2`), the one item that the curator flagged and the second annotator accepted (Table 4 and the text below it), and one of the 17 exact matches between the AI judge and the curator in Table 5.
