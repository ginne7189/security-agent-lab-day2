# Day 2 — MCP · 보안 도구 자동화

> ⚠️ **이 가이드는 전체 모노레포(security-agent-lab) 기준 CLI 실습 설명입니다.**
> 단독 Day 저장소에서는 README의 `streamlit run app.py`(버튼 클릭 실습)만 쓰면 됩니다.
> `check_env.py`·`scripts/`·`orchestrator/`·`mcp_servers/` 는 모노레포에만 있습니다(이 저장소에는 없음).
> `agents/`·`course/mini_labs/`·`policies/`·`sample_app/` 명령은 이 저장소에서도 그대로 동작합니다.


## 오늘의 목표
- 도구(함수) 호출 개념과 "Raw JSON / Report 분리" 패턴을 이해한다.
- MCP security-tools 로 보안 도구를 실행하고 결과를 파싱한다.

---

## Mini Lab — Toy Tool Demo
- **목적**: 도구 호출 결과를 기계용 Raw JSON 과 사람용 Report 로 분리하는 패턴 체감
- **실행 명령**
  ```bash
  python course/mini_labs/day02_tool_calling/run_toy_tool_demo.py
  ```
- **산출물**: `reports/tool_calling_raw.json`, `reports/tool_calling_result.md`
- **확인 포인트**: 도구 4종이 모두 호출됐는가? Raw JSON 과 Report 의 역할 차이가 보이는가?
- **본 실습 연결**: Toy Tool Demo 의 Raw/Report 분리가 본 실습의 **lab2_scan_raw.json / lab2_report.md** 분리로 확장된다.
- 자세히: `course/experiments/day02_tool_calling_experiment.md`

---

## Main Lab — MCP security-tools 연결 · 도구 실행 파싱
- **목적**: security-tools 로 SAST/Secret/Dependency 도구를 실행하고 결과를 구조화
- **실행 명령**
  ```bash
  python scripts/run_lab2_mcp_demo.py --target sample_app/   # 도구 3종 (필수)
  python agents/secret_agent.py --target sample_app/         # Secret 단독
  python agents/dependency_agent.py --target sample_app/     # Dependency 단독
  # (확장) claude mcp add security-tools -- python mcp_servers/security_tools_server.py
  ```
- **산출물**: `reports/lab2_report.md`, `reports/lab2_scan_raw.json`, `reports/lab2_secret_report.md`, `reports/lab2_dependency_report.md`
- **확인 포인트**: Raw JSON 과 해석 리포트가 분리됐는가? `memory/audit_log.jsonl` 에 호출 기록이 남았는가?

---

## 선택 보조: Claude/GPT 저토큰 활용
- 전체 코드베이스를 넣지 않는다.
- `python scripts/make_light_context_pack.py --day 2` 로 `reports/context_pack_day2.md` 만 생성해 복사한다.
- "이 lab2_report.md 에서 누락된 도구 설명 3개만 짚어줘" 정도로 가볍게 사용한다.

---

## 완료 체크리스트
- [ ] `reports/tool_calling_raw.json` + `reports/tool_calling_result.md` 생성
- [ ] `reports/lab2_report.md` + `reports/lab2_scan_raw.json` 생성
- [ ] Secret / Dependency 단독 실행 확인
- [ ] Raw JSON 과 Report 분리 개념 이해
