#!/usr/bin/env python3
"""
Toy Tool Demo (course/mini_labs/day02_tool_calling/run_toy_tool_demo.py) — Day 2 Mini Lab

목표: 도구 호출 결과를 "Raw JSON" 과 "사람용 Markdown Report" 로 분리하는 패턴을 체감한다.
이 분리가 Day 2 본 실습의 lab2_scan_raw.json / lab2_report.md 구조로 그대로 확장된다.

- 외부 API 호출 없음 / LLM 호출 없음 / Python 표준 라이브러리만 사용

실행:  python course/mini_labs/day02_tool_calling/run_toy_tool_demo.py
산출물: reports/tool_calling_raw.json, reports/tool_calling_result.md
"""
import json
import os
import sys

# `python course/mini_labs/.../run_toy_tool_demo.py` 와 repo 루트 실행 모두 지원
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import toy_tools  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FEEDBACK = os.path.join(HERE, "sample_feedback.txt")
RAW_OUT = "reports/tool_calling_raw.json"
MD_OUT = "reports/tool_calling_result.md"


def main():
    with open(FEEDBACK, encoding="utf-8") as f:
        text = f.read()

    # ── 도구(함수) 호출 ── 각 도구가 구조화된 결과(dict/list)를 돌려준다 ──
    raw = {
        "count_words": toy_tools.count_words(text),
        "extract_keywords": toy_tools.extract_keywords(text, top_n=5),
        "compare_lists": toy_tools.compare_lists(
            ["sast", "secret", "dependency"],
            ["sast", "dependency", "threat"],
        ),
        "summarize_feedback": toy_tools.summarize_feedback(text),
    }

    os.makedirs("reports", exist_ok=True)

    # 1) 기계용 Raw JSON — 그대로, 가공 없이 저장
    with open(RAW_OUT, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)

    # 2) 사람용 Markdown Report — 읽기 쉽게 요약해 저장
    cw = raw["count_words"]
    fb = raw["summarize_feedback"]
    kw = raw["extract_keywords"]
    cmp_ = raw["compare_lists"]

    lines = [
        "# Toy Tool Demo 결과 (Day 2 Mini Lab)", "",
        "> Raw JSON 과 사람용 Report 를 의도적으로 분리했습니다.", "",
        "## 텍스트 통계",
        f"- 단어 수: {cw['word_count']}",
        f"- 문장 수: {cw['sentence_count']}",
        f"- 문자 수: {cw['char_count']}", "",
        "## 키워드 Top 5",
    ]
    lines += [f"- {k['word']} ({k['count']}회)" for k in kw] or ["- (없음)"]
    lines += [
        "", "## 피드백 요약",
        f"- 긍정 문장: {fb['positive_count']}개",
        f"- 부정 문장: {fb['negative_count']}개",
        "", "### 부정 피드백(개선 후보)",
    ]
    lines += [f"- {s}" for s in fb["negative"]] or ["- (없음)"]
    lines += [
        "", "## 도구 비교 예시 (compare_lists)",
        f"- 공통: {', '.join(cmp_['in_both']) or '-'}",
        f"- A 에만: {', '.join(cmp_['only_in_a']) or '-'}",
        f"- B 에만: {', '.join(cmp_['only_in_b']) or '-'}",
        "",
        "> 연결: 여기서 Raw JSON 과 Report 를 분리한 것처럼,",
        "> Day 2 본 실습은 security-tools 결과를 lab2_scan_raw.json 과 lab2_report.md 로 분리합니다.",
        "",
    ]
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[ToyTool] 도구 4종 호출 완료")
    print(f"[ToyTool] Raw JSON  → {RAW_OUT}")
    print(f"[ToyTool] Report    → {MD_OUT}")


if __name__ == "__main__":
    main()
