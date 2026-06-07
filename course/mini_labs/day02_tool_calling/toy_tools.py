"""
Toy Tools (course/mini_labs/day02_tool_calling/toy_tools.py) — Day 2 Mini Lab

MCP 에 들어가기 전에 "도구(함수) 호출" 개념을 가장 단순하게 체감하기 위한 도구 모음.
각 함수는 입력을 받아 JSON 직렬화 가능한 결과를 돌려준다.

- 외부 API 호출 없음 / LLM 호출 없음 / Python 표준 라이브러리만 사용
"""
import re
from collections import Counter

# 한국어/영어에서 흔한 불용어(키워드 추출 시 제외)
_STOPWORDS = {
    "그리고", "하지만", "조금", "특히", "있는", "같습니다", "좋았습니다", "것", "수",
    "the", "a", "an", "and", "but", "to", "of", "is", "it", "for",
}
_WORD_RE = re.compile(r"[0-9A-Za-z가-힣]+")


def count_words(text):
    """텍스트의 단어/문장/문자 수를 센다."""
    words = _WORD_RE.findall(text or "")
    sentences = [s for s in re.split(r"[.!?。\n]", text or "") if s.strip()]
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "char_count": len(text or ""),
    }


def extract_keywords(text, top_n=5):
    """불용어를 제거하고 가장 자주 등장하는 단어 top_n 개를 반환."""
    words = [w.lower() for w in _WORD_RE.findall(text or "") if len(w) > 1]
    words = [w for w in words if w not in _STOPWORDS]
    counter = Counter(words)
    return [{"word": w, "count": c} for w, c in counter.most_common(top_n)]


def compare_lists(list_a, list_b):
    """두 리스트의 교집합/차집합을 계산(도구가 구조화된 결과를 돌려줌을 보여줌)."""
    set_a, set_b = set(list_a or []), set(list_b or [])
    return {
        "only_in_a": sorted(set_a - set_b),
        "only_in_b": sorted(set_b - set_a),
        "in_both": sorted(set_a & set_b),
    }


def summarize_feedback(text):
    """피드백을 긍정/부정 문장으로 아주 단순하게 분류한다(규칙 기반)."""
    pos_markers = ("좋", "유용", "만족", "편", "직관", "명확", "깔끔")
    neg_markers = ("부족", "불안", "불친절", "빠진", "오타", "에러", "어렵", "길어")
    positives, negatives, neutral = [], [], []
    for raw in re.split(r"(?<=[.!?。])\s*|\n", text or ""):
        s = raw.strip()
        if not s:
            continue
        has_neg = any(m in s for m in neg_markers)
        has_pos = any(m in s for m in pos_markers)
        if has_neg:
            negatives.append(s)
        elif has_pos:
            positives.append(s)
        else:
            neutral.append(s)
    return {
        "positive": positives,
        "negative": negatives,
        "neutral": neutral,
        "positive_count": len(positives),
        "negative_count": len(negatives),
    }
