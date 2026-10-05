#!/usr/bin/env python3
"""
Duyen pilot: sinh gói gán nhãn cho NGƯỜI THỨ HAI, có chặn lộ đáp án.

Vì sao cần script thay vì copy tay: nếu người thứ hai nhìn thấy bản đã sửa, họ chỉ
cần so hai câu là suy ra nhãn, lúc đó ta đo khả năng so chuỗi chứ không đo cảm nhận
tiếng Việt, và RQ2 mất giá trị.

Các lớp bảo vệ (đều chạy thật, kiểm trên FILE ĐÃ GHI):
  1. Cột xuất ra bị khoá cứng: chỉ tình huống + câu gốc + hai cột trống.
     Kiểm sau khi ghi: header đúng y bộ cột cho phép, không dính cột cấm.
  2. Mỗi item_id chỉ lấy MỘT output. Nếu đưa cả hai model của cùng một kịch bản
     vào một gói thì người ta lại so hai câu với nhau, hở đúng như cũ.
  3. Đọc lại từng dòng đã ghi: cột nhãn/ghi chú phải trống, và không một bản sửa
     nào (khác câu gốc) xuất hiện trong nội dung gói.

Ngoài ra (bản 25/8):
  - Lấy mẫu PHÂN TẦNG theo relative_status (giữ tỉ lệ trên/ngang/dưới của kho).
  - row_uid là mã ẩn (hash) và thứ tự dòng được xáo — không suy ngược ra item_id.
  - Tình huống hiển thị cả GIỚI TÍNH + TUỔI người nghe (cần cho PR1/PR2).
  - Tự trộn câu kiểm soát viết tay từ control-items.csv (nếu có); cột
    expected_note_PRIVATE không bao giờ được chép sang gói.
  - --n bỏ trống = tự lấy tối đa cho phép (60% kho).

Dùng:
    python3 make_annotator2_sheet.py            # n = tối đa cho phép
    python3 make_annotator2_sheet.py --n 18 --seed 7 --force

Đầu ra:
    to-send/Annotator2-Sheet.csv   <- gửi cho người thứ hai (kèm GUIDELINE.md)
    _private/annotator2-key.csv    <- CHỈ mình giữ, có nhãn của bạn + map uid
"""
import argparse, csv, hashlib, os, random, sys

FORBIDDEN_COLS = {"corrected_vi", "error_types", "target_types_hypothesis",
                  "note", "expected_note_PRIVATE", "model", "item_id", "control_id"}
REQUIRED_COLS = ["item_id", "register", "relative_status", "closeness",
                 "setting", "utterance_type", "addressee_gender",
                 "addressee_age_cue", "raw_output"]
CONTROL_COLS = ["control_id", "register", "relative_status", "closeness",
                "setting", "utterance_type", "addressee_gender",
                "addressee_age_cue", "cau_viet_tay"]
VALID_LABELS = ["PR1", "PR2", "PR4", "PF1", "PF2", "FP1", "FP2", "NONE", "OTHER"]
OUT_FIELDS = ["row_uid", "tinh_huong", "cau_may_viet", "nhan", "ghi_chu"]

VI = {
    "status": {"higher": "vai TRÊN (lớn tuổi hơn hoặc cấp trên)",
               "equal":  "NGANG HÀNG",
               "lower":  "vai DƯỚI (ít tuổi hơn hoặc cấp dưới)"},
    "close":  {"intimate": "thân", "familiar": "quen", "distant": "không thân"},
    "set":    {"formal": "trang trọng", "neutral": "bình thường", "casual": "thoải mái"},
    "utt":    {"request": "nhờ vả", "greeting": "chào", "answer": "trả lời",
               "question": "hỏi", "proposal": "rủ", "statement": "nhận xét"},
    "reg":    {"workplace": "nơi làm việc", "school": "trường học", "family": "gia đình",
               "service": "cửa hàng / dịch vụ", "friends": "bạn bè"},
}

def die(msg):
    sys.exit(f"\nDỪNG: {msg}\n")

def scenario(r):
    gender = (r.get("addressee_gender") or "không rõ").strip()
    age = (r.get("addressee_age_cue") or "").strip()
    who = f"{VI['status'].get(r['relative_status'], r['relative_status'])}"
    detail = ", ".join(x for x in [f"giới tính {gender}" if gender else "", age] if x)
    if detail:
        who += f" ({detail})"
    return (f"Bối cảnh: {VI['reg'].get(r['register'], r['register'])}. "
            f"Người nghe là {who}, "
            f"quan hệ {VI['close'].get(r['closeness'], r['closeness'])}, "
            f"không khí {VI['set'].get(r['setting'], r['setting'])}. "
            f"Kiểu câu: {VI['utt'].get(r['utterance_type'], r['utterance_type'])}.")

def parse_labels(s):
    return {p.strip().upper() for p in (s or "").split(";") if p.strip()}

def make_uid(seed, kind, key):
    h = hashlib.sha256(f"{seed}:{kind}:{key}".encode("utf-8")).hexdigest()[:6].upper()
    return f"U{h}"

def stratified_sample(pool, n, rng):
    """Giữ đúng tỉ lệ relative_status của kho (largest remainder)."""
    groups = {}
    for r in pool:
        groups.setdefault(r["relative_status"], []).append(r)
    total = len(pool)
    quotas, remainders = {}, []
    used = 0
    for k, rows in groups.items():
        exact = n * len(rows) / total
        quotas[k] = int(exact)
        used += quotas[k]
        remainders.append((exact - quotas[k], k))
    for _, k in sorted(remainders, reverse=True)[: n - used]:
        quotas[k] += 1
    out = []
    for k, rows in groups.items():
        q = min(quotas.get(k, 0), len(rows))
        out.extend(rng.sample(rows, q))
    # nếu nhóm nào thiếu (quota > kho), bù từ phần còn lại
    if len(out) < n:
        rest = [r for r in pool if r not in out]
        out.extend(rng.sample(rest, n - len(out)))
    return out

def load_controls(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in CONTROL_COLS if c not in (reader.fieldnames or [])]
        if missing:
            die(f"{path} thiếu cột: " + ", ".join(missing))
        rows = list(reader)
    for r in rows:
        r["raw_output"] = r["cau_viet_tay"]  # để render chung một đường
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=None,
                    help="số câu lấy từ kho (bỏ trống = tối đa cho phép)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--infile", default="Duyen-Pilot-Sheet.csv")
    ap.add_argument("--controls", default="control-items.csv",
                    help="file câu kiểm soát viết tay (đặt '' để tắt)")
    ap.add_argument("--force", action="store_true", help="cho phép ghi đè gói đã tạo")
    a = ap.parse_args()

    if not os.path.exists(a.infile):
        die(f"không tìm thấy {a.infile}")

    with open(a.infile, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLS if c not in (reader.fieldnames or [])]
        if missing:
            die("bảng thiếu cột: " + ", ".join(missing) +
                "\n(Có phải bạn đổi tên tiêu đề cột trong Excel không?)")
        rows = list(reader)

    filled = [r for r in rows if (r.get("raw_output") or "").strip()]
    if not filled:
        print("CHƯA CÓ raw_output nào. Hãy chạy model và dán output vào cột raw_output trước.")
        print(f"(Đọc được {len(rows)} dòng, 0 dòng có output.)")
        return

    # --- Lớp 2: mỗi kịch bản chỉ lấy một output -------------------------------
    by_item = {}
    for r in filled:
        by_item.setdefault(r["item_id"], []).append(r)
    rng = random.Random(a.seed)
    pool = [rng.choice(v) for v in by_item.values()]
    dropped = len(filled) - len(pool)
    if dropped:
        print(f"Bỏ {dropped} dòng trùng kịch bản (mỗi item_id chỉ lấy 1 output, "
              f"để người thứ hai không so hai model với nhau).")

    cap = int(0.6 * len(pool))
    if cap < 5:
        die(f"kho chỉ có {len(pool)} kịch bản dùng được → trần 60% là {cap} câu, "
            f"dưới mức tối thiểu 5 câu. Cần thêm kịch bản có output vào bảng pilot "
            f"(khoảng 9 kịch bản trở lên) rồi chạy lại.")
    n = a.n if a.n is not None else cap
    if n < 5:
        die("--n quá nhỏ, cần ít nhất 5 câu thì mới có gì để so.")
    if n > cap:
        die(f"xin {n} câu nhưng kho chỉ có {len(pool)} kịch bản dùng được. "
            f"Lấy quá {cap} câu (60% kho) thì việc 'chọn ngẫu nhiên' không còn ý nghĩa "
            f"và không còn phần giữ lại để kiểm chéo về sau.\n"
            f"Cách xử lý: tăng số kịch bản trong bảng pilot, hoặc chạy --n {cap} trở xuống.")
    sample = stratified_sample(pool, n, rng)
    strat = {}
    for r in sample:
        strat[r["relative_status"]] = strat.get(r["relative_status"], 0) + 1
    print(f"Mẫu {n} câu, phân tầng theo vai: {strat} "
          f"(kho: { {k: len([r for r in pool if r['relative_status']==k]) for k in strat} }).")

    # --- Câu kiểm soát viết tay -----------------------------------------------
    controls = load_controls(a.controls) if a.controls else []
    if controls:
        print(f"Trộn thêm {len(controls)} câu kiểm soát viết tay từ {a.controls} "
              f"(báo cáo tách riêng, không tính vào số liệu chính).")

    # --- Cảnh báo tỉ lệ câu không lỗi ----------------------------------------
    labelled = [r for r in sample if (r.get("error_types") or "").strip()]
    if not labelled:
        print("\n⚠ Bạn chưa gán nhãn câu nào trong mẫu này, nên không kiểm được tỉ lệ "
              "câu không lỗi. Nếu gần như câu nào cũng có lỗi, người thứ hai sẽ đoán ra "
              "và gán bừa. Nên gán nhãn xong (bước 3) rồi hãy tạo gói này.")
    else:
        none_cnt = sum(1 for r in labelled if "NONE" in parse_labels(r["error_types"]))
        pct = 100 * none_cnt / len(labelled)
        print(f"Trong mẫu: {none_cnt}/{len(labelled)} câu bạn gán NONE ({pct:.0f}%).")
        if pct < 15:
            print("  ⚠ Tỉ lệ câu không lỗi thấp. Cân nhắc thêm item dễ vào kho.")

    # --- Gộp, gán uid ẩn, xáo thứ tự -----------------------------------------
    packet = []
    for r in sample:
        packet.append({"_uid": make_uid(a.seed, "item", f"{r['item_id']}|{r.get('model','')}"),
                       "_src": r, "_is_control": False})
    for r in controls:
        packet.append({"_uid": make_uid(a.seed, "control", r["control_id"]),
                       "_src": r, "_is_control": True})
    if len({p["_uid"] for p in packet}) != len(packet):
        die("trùng row_uid (cực hiếm) — đổi --seed rồi chạy lại.")
    rng.shuffle(packet)

    # --- Lớp 1: khoá bộ cột trước khi ghi -------------------------------------
    bad = set(OUT_FIELDS) & FORBIDDEN_COLS
    if bad:
        die("bộ cột xuất ra dính cột cấm: " + ", ".join(bad))

    os.makedirs("to-send", exist_ok=True)
    os.makedirs("_private", exist_ok=True)
    out_sheet = os.path.join("to-send", "Annotator2-Sheet.csv")
    out_key = os.path.join("_private", "annotator2-key.csv")
    if os.path.exists(out_sheet) and not a.force:
        die(f"{out_sheet} đã tồn tại. Nếu người thứ hai đã bắt đầu chấm, tạo lại sẽ ra "
            f"mẫu khác và hỏng phép so. Chắc chắn muốn ghi đè thì thêm --force.")

    tmp = out_sheet + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=OUT_FIELDS)
        w.writeheader()
        for p in packet:
            r = p["_src"]
            w.writerow({"row_uid": p["_uid"], "tinh_huong": scenario(r),
                        "cau_may_viet": r["raw_output"].strip(),
                        "nhan": "", "ghi_chu": ""})

    # --- Lớp 1 (kiểm thật) + Lớp 3: kiểm trên file đã ghi ---------------------
    with open(tmp, encoding="utf-8-sig") as f:
        written = list(csv.DictReader(f))
        f.seek(0)
        written_header = next(csv.reader(f))
        f.seek(0)
        body = f.read()
    if written_header != OUT_FIELDS:
        os.remove(tmp); die(f"header gói không đúng bộ cột cho phép: {written_header}")
    for i, row in enumerate(written, 1):
        if (row.get("nhan") or "").strip() or (row.get("ghi_chu") or "").strip():
            os.remove(tmp); die(f"dòng {i}: cột nhãn/ghi chú không trống.")
    for r in sample:
        corr = (r.get("corrected_vi") or "").strip()
        # câu không lỗi thì bản sửa trùng câu gốc, đó là bình thường, bỏ qua
        if corr and corr != r["raw_output"].strip() and corr in body:
            os.remove(tmp); die(f"bản sửa của item {r['item_id']} lọt vào gói.")
    for r in controls:
        note = (r.get("expected_note_PRIVATE") or "").strip()
        if note and note in body:
            os.remove(tmp); die(f"ghi chú riêng của {r['control_id']} lọt vào gói.")

    # cảnh báo nếu hai dòng trong gói có tình huống trùng khít (mời người ta so câu)
    seen = {}
    for row in written:
        seen.setdefault(row["tinh_huong"], []).append(row["row_uid"])
    dup = {k: v for k, v in seen.items() if len(v) > 1}
    if dup:
        os.remove(tmp)
        die("có các dòng TRÙNG tình huống trong gói (người chấm sẽ so hai câu với nhau "
            "và nhận ra câu kiểm soát):\n  " +
            "\n  ".join(f"{v}: {k[:80]}…" for k, v in dup.items()) +
            "\nSửa metadata của câu kiểm soát (control-items.csv) cho khác item pilot, "
            "hoặc đổi --seed.")

    os.replace(tmp, out_sheet)

    with open(out_key, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["row_uid", "item_id_hoac_control_id", "model", "is_control",
                    "nhan_cua_Hieu", "ghi_chu_thiet_ke_control"])
        for p in packet:
            r = p["_src"]
            src_id = r.get("item_id") or r.get("control_id", "")
            w.writerow([p["_uid"], src_id, r.get("model", ""),
                        "yes" if p["_is_control"] else "",
                        r.get("error_types", ""),
                        r.get("expected_note_PRIVATE", "") if p["_is_control"] else ""])

    h = hashlib.sha256(open(a.infile, "rb").read()).hexdigest()[:10]
    with open(os.path.join("_private", "packet-info.txt"), "w", encoding="utf-8") as f:
        f.write(f"seed={a.seed}\nn_kho={n}\nn_control={len(controls)}\ninfile={a.infile}\n"
                f"infile_sha256_10={h}\nnhan hop le={VALID_LABELS}\n"
                f"phan tang theo vai={strat}\n")

    print(f"\nĐã tạo {out_sheet}: {n} câu từ kho + {len(controls)} câu kiểm soát, "
          f"thứ tự đã xáo, uid ẩn (seed={a.seed}).")
    print(f"Khoá đối chiếu để riêng ở {out_key}.")
    print("Gửi cho người thứ hai: to-send/Annotator2-Sheet.csv + GUIDELINE.md")
    print("KHÔNG gửi: thư mục _private/, _design-probe-map.csv, control-items.csv, bảng pilot gốc.")

if __name__ == "__main__":
    main()
