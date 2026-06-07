"""대시보드 공용 렌더 모듈 — 키 없이 동작 · 외부 API 호출 없음."""
import importlib.util
import json
import os
import random
import sys

import streamlit as st

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


toy = _load("course/mini_labs/day02_tool_calling/toy_tools.py", "toy")
from agents import sast_agent, secret_agent, dependency_agent, llm_client  # noqa: E402

def render_overview():
    st.subheader("👋 이 대시보드는 '데모 실행기'예요")
    st.markdown(
        "AI 에이전트로 **코드·보안 취약점 점검을 자동화**하는 5일 실습을, "
        "터미널 없이 **버튼 클릭**으로 직접 돌려봅니다."
    )

    st.markdown("#### 🧭 사용법 — 딱 3단계")
    s1, s2, s3 = st.columns(3)
    s1.info("**① 위 탭 선택**\n\n🤔 왜 만드나 · Day 1~5 중 하나 클릭")
    s2.info("**② 버튼 누르기**\n\n각 탭의 파란 버튼(🔍 🧰 🐞 🚀 …)을 클릭")
    s3.info("**③ 결과 확인**\n\n표·차트·메시지가 화면에 바로 나타남")

    st.markdown("#### ✨ '뭐가 바뀌는지' 눈으로 보이는 곳 (먼저 가보세요)")
    st.markdown(
        "- **🤔 왜 만드나?** 탭 → 버튼 여러 번 클릭 → *왼쪽(그냥 LLM)은 숫자가 흔들리고 비밀이 새고, "
        "오른쪽(에이전트)은 항상 똑같고 안전* 한 게 **나란히** 보여요.\n"
        "- **Day 1** 탭 → 정책 **체크박스를 껐다 켜면** 결과 리포트가 **즉시** 바뀝니다.\n"
        "- **Day 1** 탭 → SAST 정책을 `CLAUDE_base` ↔ `CLAUDE` 로 바꾸면 차량모듈이 **High → Critical** 로 올라가요."
    )
    st.success("👆 위 두 곳이 '에이전트가 무엇을, 어떻게 바꾸는지' 가장 빨리 체감되는 지점이에요.")

    st.markdown("#### 🤖 어떤 에이전트가 'AI(LLM)를 부르나'?")
    key_on = bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY"))
    st.dataframe([
        {"구성요소": "SAST · Secret · Dependency · Threat · Report", "종류": "⚙️ 규칙(결정론)", "AI 호출": "❌ (키 없이 항상 동작)"},
        {"구성요소": "llm_client · run_llm_interpret", "종류": "🧠 AI 해석(선택)", "AI 호출": "✅ 키 있을 때만 (없으면 규칙 fallback)"},
    ], width="stretch", hide_index=True)
    if key_on:
        st.info("🧠 현재 **AI 키 감지됨** → 해석 레이어가 LLM을 부릅니다.")
    else:
        st.warning("⚙️ 현재 **AI 키 없음** → 5개 에이전트는 전부 **규칙(LLM 없이)** 으로 동작합니다. "
                   "그래도 모든 실습이 끝까지 돌아가요. (키를 넣으면 🧠 해석만 추가됨)")
    st.caption("흐름: ⚙️ 규칙 에이전트가 '발견' → (선택) 🧠 AI가 그 발견을 자연어로 '해석'.")

    with st.expander("📐 전체 구조 그림 보기"):
        arch = os.path.join(ROOT, "docs/diagrams/01_architecture.png")
        if os.path.exists(arch):
            st.image(arch, caption="전체 아키텍처", width="stretch")


def render_why():
    st.subheader("🤔 왜 'LLM 그냥 쓰기'가 아니라 '에이전트를 만드나'?")
    st.markdown(
        "**LLM = 엄청 똑똑한 신입사원** 🧑‍💻\n\n"
        "그냥 \"보안 점검해줘\" 하고 맡기는 것 vs **매뉴얼·검수·결재선·기록을 붙인 것**.\n\n"
        "아래 버튼으로 **같은 일을 두 방식으로** 시켜보세요 👇 (여러 번 눌러보세요!)"
    )
    if st.button("🎬 같은 일, 두 방식으로 시켜보기!", key="why_btn"):
        full = sast_agent.run("sample_app/", "policies/CLAUDE.md")
        raw_secret = next(
            (l.strip() for l in open("sample_app/vulnerability.py", encoding="utf-8")
             if "API_TOKEN" in l and '"' in l and not l.strip().startswith("#")),
            'API_TOKEN = "..."')
        left, right = st.columns(2)
        with left:
            st.markdown("### 😱 그냥 LLM한테 시킴")
            wobble = random.randint(max(1, len(full) - 4), len(full))
            st.error(f"이번엔 **{wobble}건** 찾았대요 🎲 (또 누르면 숫자 바뀜)")
            st.markdown("**비밀값도 그대로 뱉음:**")
            st.code(raw_secret, language="python")
            st.markdown("📋 감사 기록 **없음**  ·  🤥 틀려도 **그냥 통과**")
            st.caption("→ 매번 답이 달라서 못 믿어요.")
        with right:
            st.markdown("### 😎 울타리 친 에이전트 (이 repo)")
            st.success(f"항상 **{len(full)}건** ✅ (몇 번 눌러도 똑같음)")
            st.markdown("**비밀값은 자동 마스킹:**")
            masked = next((r["evidence"] for r in full if "CWE-798" in r["cwe"]), 'API_TOKEN = "****"')
            st.code(masked, language="python")
            st.markdown("📋 감사 로그 1줄 자동 생성:")
            st.code('{"agent":"sast","action":"scan","outcome":"9 findings"}', language="json")
            st.caption("→ 정책·마스킹·검증·감사가 보장돼요.")
        st.info("**핵심**: 실무 AI는 LLM을 '쓰는' 게 아니라 **'울타리로 가둬 믿게 만드는'** 일! "
                "그 울타리를 만드는 게 = **에이전트 엔지니어링** (이 과정의 진짜 주제) 🎯")
    st.markdown("---")
    st.markdown(
        "| | 😱 그냥 LLM | 😎 에이전트 |\n|---|---|---|\n"
        "| 결과 | 매번 다름 🎲 | 항상 같음 ✅ |\n"
        "| 비밀값 | 줄줄 샘 🔓 | 마스킹 🔒 |\n"
        "| 틀리면 | 그냥 통과 | 재시도/차단 🛡️ |\n"
        "| 위험 행동 | 막 실행 | 사람 승인 ✋ |\n"
        "| 기록 | 없음 | 감사 로그 📋 |"
    )


def render_day2():
    st.subheader("Day 2 · 도구 호출 & 결과 분리")
    st.markdown("#### ① Mini Lab — Toy Tool (Raw JSON ↔ 사람용 결과)")
    fb_path = os.path.join(ROOT, "course/mini_labs/day02_tool_calling/sample_feedback.txt")
    if st.button("🧰 도구 4종 실행", key="d2_toy") and os.path.exists(fb_path):
        text = open(fb_path, encoding="utf-8").read()
        cw = toy.count_words(text)
        kw = toy.extract_keywords(text)
        fb = toy.summarize_feedback(text)
        m1, m2, m3 = st.columns(3)
        m1.metric("단어 수", cw["word_count"])
        m2.metric("긍정 문장", fb["positive_count"])
        m3.metric("부정 문장", fb["negative_count"])
        st.markdown("**키워드 Top 5**")
        st.dataframe(kw, width="stretch", hide_index=True)
        with st.expander("🔧 Raw JSON (기계용) — 사람용 화면과 분리"):
            st.json({"count_words": cw, "extract_keywords": kw, "summarize_feedback": fb})
    st.divider()
    st.markdown("#### ② Main Lab — 보안 도구 (Secret / Dependency)")
    cc1, cc2 = st.columns(2)
    if cc1.button("🔑 Secret 점검", key="d2_sec"):
        res = secret_agent.run("sample_app/")
        st.dataframe([{"파일": os.path.basename(r["file"]), "줄": r["line"],
                       "내용": r["title"], "근거(마스킹됨)": r["evidence"]} for r in res],
                     width="stretch", hide_index=True)
    if cc2.button("📦 Dependency(CVE) 점검", key="d2_dep"):
        res = dependency_agent.run("sample_app/")
        st.dataframe([{"심각도": r["severity"], "CVE": r["cve"], "근거": r["evidence"]} for r in res],
                     width="stretch", hide_index=True)

    st.divider()
    st.markdown("#### 🧠 (보너스) AI 로 'Raw 발견 → 사람용 리포트'")
    st.caption(f"도구가 찾은 Raw 발견을 AI가 사람 말로 해석합니다. 현재 모드: {llm_client.mode_label()}")
    if st.button("🧠 AI 리포트 생성", key="d2_ai"):
        fnd = (sast_agent.run("sample_app/", "policies/CLAUDE.md")
               + secret_agent.run("sample_app/") + dependency_agent.run("sample_app/"))
        st.markdown(llm_client.interpret(fnd))   # 키 없으면 결정론적 fallback 자동
    with st.expander("🎯 개선 과제 (직접 해보기)"):
        st.markdown(
            "- `course/mini_labs/day02_tool_calling/toy_tools.py` 에 새 도구 `count_sentences(text)` 를 추가하고 "
            "`run_toy_tool_demo.py` 결과에 끼워보기\n"
            "- `sample_feedback.txt` 내용을 바꿔 키워드/긍정·부정 분류가 어떻게 달라지는지 관찰\n"
            "- (도전) `agents/secret_agent.py` 에 Slack 토큰(`xoxb-…`) 탐지 규칙 1개 추가"
        )
