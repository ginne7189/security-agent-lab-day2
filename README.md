# 2️⃣ security-agent-lab-day2

**Day 2 · 도구 호출 & 결과 분리** — 키 없이 버튼 클릭만으로 돌려보는 Streamlit 실습.

> 5일짜리 `security-agent-lab` 과정 중 **Day 2만** 떼어낸 독립 저장소입니다.
> (다른 Day는 `security-agent-lab-day1` … `day5`, 스캐닝 엔진 코어는 `security-scan-engine` 저장소)

## 무엇을 보여주나
- **Mini Lab** — Toy Tool: Raw JSON(기계용) ↔ 사람용 결과 분리
- **Main Lab** — Secret(비밀값)·Dependency(CVE) 점검
- **보너스** — AI가 Raw 발견을 사람 말 리포트로 해석 (키 없으면 fallback)

## 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저가 열리면 위 탭(개요 · 왜 만드나 · Day 2)을 눌러보세요. **AI 키·외부 API 호출 불필요**.

## 구성
- `app.py` / `dashboard_lib.py` — Day 2 Streamlit 대시보드
- `agents/` — 스캐닝 엔진 코어(규칙 기반, 키 불필요)
- `sample_app/`·`policies/` — 점검 대상과 정책

<!-- NAV -->

## 🔗 관련 저장소 (5일 과정 전체)

| | 저장소 | 내용 |
|---|---|---|
|  | [`security-agent-lab-day1`](https://github.com/ginne7189/security-agent-lab-day1) | Day 1 · 정책이 결과를 바꾼다 |
| 👉 **현재** | [`security-agent-lab-day2`](https://github.com/ginne7189/security-agent-lab-day2) | Day 2 · 도구 호출 & 결과 분리 |
|  | [`security-agent-lab-day3`](https://github.com/ginne7189/security-agent-lab-day3) | Day 3 · 멀티에이전트 = 역할 분리 |
|  | [`security-agent-lab-day4`](https://github.com/ginne7189/security-agent-lab-day4) | Day 4 · 위험도 점수화 |
|  | [`security-agent-lab-day5`](https://github.com/ginne7189/security-agent-lab-day5) | Day 5 · 통합 |
|  | [`security-scan-engine`](https://github.com/ginne7189/security-scan-engine) | 🛠️ 스캐닝 엔진 코어 (SAST·Secret·Dependency·Threat) |
