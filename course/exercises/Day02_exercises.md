# Day 2 과제 — 도구/MCP (Tool Calling · Context Budget · Hooks)
> PPT 개념: Tool Calling · Context Budget · Hooks

## 🎬 시나리오
보안 도구 결과가 사람마다 다르게 정리된다.
도구를 **표준화**하고, 반복 작업을 **슬래시 커맨드/훅으로 자동화**하라.

## 🟢 기본 과제 (5~10분)
1. `course/mini_labs/day02_tool_calling/toy_tools.py` 에 새 도구 `count_sentences(text)` 추가
   → `run_toy_tool_demo.py` 결과(또는 대시보드)에 끼워보기.
2. `sample_feedback.txt` 내용을 바꿔 키워드/긍정·부정 분류가 어떻게 달라지는지 관찰.
3. `python scripts/run_lab2_mcp_demo.py --target sample_app/` 로 Raw JSON ↔ Report 분리 재확인.

## 🏗 생성형 과제 — '코드를 만드는 코드' (10~20분)
1. 새 보안 도구 에이전트 보일러플레이트 생성:
   ```bash
   python scripts/new_agent.py httpcheck \
     --cwe CWE-319 --title "평문 HTTP 사용" --pattern "http://"
   python agents/httpcheck_agent.py --target sample_app/
   ```
2. **슬래시 커맨드 생성**: `.claude/commands/scan.md`
   ```markdown
   ---
   description: sample_app 점검 후 5줄 요약
   ---
   sample_app 을 SAST·Secret·Dependency 로 점검하고 결과를 5줄로 요약해줘.
   ```

## ⚙️ 자동화 과제 (Hooks)
`.claude/settings.json` 에 훅 추가 — 파일 저장 시 마스킹 테스트 자동 실행:
```json
{ "hooks": { "PostToolUse": [
  { "matcher": "Edit|Write",
    "hooks": [{ "type": "command", "command": "python -m pytest tests/test_masking_contract.py -q" }] } ] } }
```

## 🔥 도전 과제
`agents/secret_agent.py` 에 **Slack 토큰(`xoxb-…`) 탐지 규칙** 1개 추가.

## ✅ 완료 체크
- [ ] 새 도구/에이전트 생성
- [ ] 슬래시 커맨드 또는 훅 1개 만들기
- [ ] Raw/Report 분리 개념 확인
