# Duyen — Annotation Guideline / Bảng hướng dẫn gán nhãn

**This is the single source of truth for the label set.** Both annotators and the AI judge use exactly these labels. The paper cites this file as the released guideline. Bilingual on purpose: Vietnamese for the annotators, English so the co-author and reviewers can audit it.

**Phiên bản: `v1.0-FROZEN` (25/8/2026).** Bộ nhãn đã chốt: **9 nhãn** như Mục 2, giữ nguyên FP2, không thêm nhãn mới. Lỗi "quá khách sáo" (nói với vai dưới mà dùng kính ngữ) được xử lý bằng `OTHER` theo quy tắc ranh giới số 5. **Không đổi bộ nhãn sau khi đã gửi cho người gán nhãn** — đổi nhãn sau khi chấm sẽ làm hỏng toàn bộ số liệu RQ2. Ghi số phiên bản này vào cả hai bảng gán nhãn.

> Nếu thấy ví dụ nào trong bảng chưa tự nhiên với tai bạn, cứ chấm theo cảm nhận của mình và ghi lại ở cột ghi chú — bất đồng là dữ liệu quý, không phải lỗi của bạn.

---

## 1. Nhiệm vụ / The task

Bạn đọc **một câu do máy (AI) viết ra**, cùng với **thông tin về quan hệ giữa người nói và người nghe**. Câu hỏi duy nhất: *người Việt (miền Bắc) trong tình huống đó có nói như vậy không?*

Bạn **không** chấm đúng sai ngữ pháp, **không** chấm nội dung hay hay dở. Chỉ chấm **mức độ tự nhiên về mặt quan hệ xã hội**: xưng hô, lễ phép, tiểu từ cuối câu.

*You read one machine-generated Vietnamese sentence together with the stated relationship between speaker and addressee, and judge only whether a Northern Vietnamese speaker would say it that way. Not grammar, not content quality: only social/relational naturalness.*

---

## 2. Bộ nhãn / The label set (9 nhãn)

Một câu có thể mang **nhiều nhãn** cùng lúc. Ghi cách nhau bằng dấu chấm phẩy, ví dụ: `FP1;PR2`

| Mã | Tên (VN) | Nhận biết (VN) | English gloss |
|----|----------|----------------|---------------|
| PR1 | Sai từ xưng hô | Từ gọi người nghe không hợp tuổi/vai của họ | Wrong address term for the addressee's age or status |
| PR2 | Cặp xưng hô không khớp | Từ tự xưng không đi cặp với từ gọi người kia (*em… bạn*) | Speaker's self-term is not the licensed partner of the address term |
| PR4 | Cặp trung tính kiểu sách vở | *tôi* và *bạn* xuất hiện **cùng lúc** ở chỗ đáng lẽ dùng từ thân tộc | Textbook-neutral *tôi/bạn* pair where kin terms are required |
| PF1 | Thiếu từ lễ phép | Nói với người trên mà thiếu *dạ / thưa / vâng* khi cần | Missing deferential word when speaking upward |
| PF2 | Thiếu giảm nhẹ khi nhờ | Nhờ người trên mà không có *giúp… với / làm ơn / phiền* | Upward request with no softening |
| FP1 | Thiếu tiểu từ *ạ* | Chào, trả lời hoặc nhờ người trên mà cuối câu thiếu *ạ* | Missing sentence-final respect particle *ạ* |
| FP2 | Thiếu tiểu từ đồng thuận | Rủ rê hoặc nhận xét chung với bạn bè mà thiếu *nhé / nhỉ* | Missing alignment particle among peers |
| **NONE** | **Không có lỗi** | Câu đã tự nhiên, không cần sửa gì về mặt quan hệ | **No pragmatic problem** |
| **OTHER** | **Lỗi khác** | Có chỗ nghe không tự nhiên nhưng không thuộc 7 loại trên. **Bắt buộc ghi rõ ở cột ghi chú.** | **Unnatural but outside the seven types; note required** |

*(Không có mã PR3: mã đó dành cho lỗi "đổi cách xưng hô giữa các lượt nói", thuộc phần future work, không dùng trong nghiên cứu này. Giữ nguyên khoảng trống để khỏi lẫn với tài liệu cũ.)*

### Quy tắc ranh giới (để hai người không xếp khác nhau)

1. **PR1 với PR4.** Nếu chỉ có mình *bạn* (hoặc mình *tôi*) dùng sai thì là **PR1**. Chỉ khi **cả *tôi* và *bạn* cùng xuất hiện** mới là **PR4**. Một câu không bao giờ vừa PR1 vừa PR4 vì cùng một chỗ.
2. **NONE không đi với nhãn nào khác.** Đã chọn `NONE` thì không chọn thêm gì.
3. **Một câu sửa nhiều thứ thì ghi nhiều mã.** Ví dụ vừa thiếu *dạ* vừa thiếu *ạ* thì ghi `PF1;FP1`, đừng chọn một cái.
4. **`OTHER` bắt buộc có ghi chú.** Không ghi chú thì coi như bỏ trống.
5. **Quá khách sáo với vai dưới → `OTHER`.** Nói với vai DƯỚI (ít tuổi hơn / cấp dưới) mà dùng *ạ / dạ / thưa* là không tự nhiên theo chiều ngược lại. Bộ nhãn không có mã riêng cho lỗi "thừa lễ phép", nên ghi `OTHER` và ghi chú "quá khách sáo".
6. **Câu hỏi với người trên mà thiếu *ạ* → `OTHER`.** Test của FP1 chỉ phủ chào / trả lời / nhờ vả. Nếu một **câu hỏi** hướng lên nghe cộc vì thiếu *ạ*, bộ nhãn v1.0 không có mã riêng — ghi `OTHER` và ghi chú "câu hỏi thiếu ạ". Nhiều `OTHER` loại này là tín hiệu để bản sau mở rộng FP1.

### Câu máy trả về nhiều câu hoặc có lời dẫn

Model hay trả lời kiểu *"Chắc chắn rồi! Đây là tin nhắn: ..."*. Quy tắc:
- **Chỉ chấm câu thật sự nói với người nghe**, bỏ qua lời dẫn của model ("Chắc chắn rồi", "Hy vọng giúp được bạn").
- Nếu có nhiều câu cùng nói với người nghe thì chấm **cả cụm như một đơn vị**: chỉ cần một câu trong đó sai là gán nhãn tương ứng.
- Nếu model trả lời bằng tiếng Anh, lạc đề, hoặc không ra câu nào nói với người nghe: ghi `OTHER` và mô tả ở ghi chú.

### Hai nhãn quan trọng nhất về mặt phương pháp

- **NONE là một nhãn thật, không phải "bỏ trống".** Nếu câu đã ổn, hãy chọn `NONE`. Đây là cách duy nhất đo được tỉ lệ báo động giả. Đừng cố tìm lỗi cho bằng được.
- **OTHER là lối thoát an toàn.** Nếu thấy gợn mà không biết xếp vào đâu, chọn `OTHER` và tả bằng một câu. Nhiều `OTHER` không phải thất bại, đó là tín hiệu bộ nhãn cần bổ sung.

---

## 3. Đơn vị gán nhãn / Unit of annotation

**Đơn vị là cả câu (một output của model), không phải từng chỗ sửa.**

Lý do: nếu tách theo từng chỗ sửa thì hai người sẽ tách khác nhau trước cả khi kịp bất đồng về nhãn, và con số agreement sẽ bẩn. Gán nhãn cả câu thì hai bộ nhãn so được trực tiếp với nhau.

*Unit = the whole output. Agreement is computed per item and per label (present/absent), which keeps the two label sets directly comparable.*

---

## 4. Quy tắc giữ tính độc lập / Independence rules

Đây là phần quyết định giá trị của con số agreement.

Người gán nhãn thứ hai **chỉ được thấy**:
- thông tin quan hệ (ai nói với ai, thân hay sơ, bối cảnh, kiểu câu), và
- **câu gốc do máy viết**.

Người gán nhãn thứ hai **tuyệt đối không được thấy**:
- bản đã sửa (nếu thấy bản sửa thì chỉ cần so hai câu là đoán ra nhãn, lúc đó ta đo khả năng so chuỗi chứ không đo cảm nhận tiếng Việt),
- nhãn mà người thứ nhất đã gán,
- cột dự đoán loại lỗi khi thiết kế prompt.

Người thứ nhất (Hieu) cũng nên gán nhãn **trước khi** nhìn lại cột dự đoán, để tránh bị mồi.

---

## 5. Yêu cầu về người gán nhãn thứ hai

**Bắt buộc là người nói tiếng Việt miền Bắc.** Toàn bộ dữ liệu là ngữ miền Bắc, nên người miền khác sẽ đưa biến thể vùng miền vào đúng con số mà bài báo dựa vào.

Không cần biết ngôn ngữ học. Bảng này đủ để làm việc.

---

## 6. Chọn mẫu cho người thứ hai / Sampling

Người thứ hai chỉ nhận **một phần dữ liệu**, chọn ngẫu nhiên có phân tầng theo vai (trên / ngang / dưới). Không phải chỉ lấy những câu đã tìm ra lỗi: có cả câu không lỗi trộn vào, vì nếu chỉ đưa các câu có lỗi thì (a) không đo được báo động giả, và (b) người chấm sẽ nhanh chóng đoán ra rằng "câu nào cũng có lỗi" rồi gán bừa. Chi tiết kỹ thuật của phép lấy mẫu nằm trong tài liệu thiết kế đi kèm bản công bố, không cần cho việc gán nhãn.

---

## 7. Xử lý bất đồng / Adjudication

- Con số agreement được tính trên **nhãn độc lập ban đầu của hai người**, trước khi thống nhất. Không được sửa lại rồi mới tính.
- Sau khi đã tính xong, chỗ nào hai người khác nhau thì Hieu chốt nhãn cuối cho bản dữ liệu công bố, và **ghi lại là đã có bất đồng**.
- Chỗ bất đồng là dữ liệu quý: nó chỉ ra định nghĩa nào trong bảng còn mờ.

*Agreement is computed on the two independent label sets before any reconciliation. Disagreements are then resolved by the primary curator for the released dataset and recorded as such.*

---

## 8. Ví dụ / Examples

| Câu máy viết | Tình huống | Nhãn | Vì sao |
|---|---|---|---|
| *Em chào anh.* | nhân viên trẻ chào anh đồng nghiệp lớn tuổi hơn | `FP1` | Chào người trên, cuối câu cần *ạ* |
| *Em nghĩ bạn đúng.* | nói với anh đồng nghiệp lớn tuổi hơn | `PR2` | Tự xưng *em* nhưng lại gọi *bạn*, hai từ không đi cặp |
| *Mai mình đi ăn trưa.* | rủ bạn thân | `FP2` | Rủ rê giữa bạn bè mà thiếu *nhé* nghe cộc; với đề nghị giữa bạn bè, thiếu *nhé/nhỉ* tính là FP2 |
| *Dạ, em làm tốt lắm ạ.* | sếp khen cậu nhân viên trẻ mới vào | `OTHER` | Nói với vai dưới mà dùng *dạ/ạ* — quá khách sáo (quy tắc ranh giới số 5), ghi `OTHER` + ghi chú |
| *Dạ, cháu ăn rồi ạ.* | trả lời bà | `NONE` | Xưng hô đúng, có *dạ/ạ* khi trả lời người trên — câu đã tự nhiên, chọn `NONE`, không cố tìm lỗi |
