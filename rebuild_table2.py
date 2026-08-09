"""
새로운 7열 포맷에 맞게 테이블을 재구성합니다:
| # | 이름 | 공식 웹사이트 | 지원 모델 | Base URL | API 지연 시간 | 공식 웹사이트 지연 시간 |
"""
import re
from pathlib import Path

README_PATH = Path(__file__).resolve().parent / "README.md"

with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 한국어 헤더 기준으로 탐색 위치 변경
table_start = content.find("| # | 이름 | 공식 웹사이트 |")
table_end = content.find("\n\n---\n\n## 📚", table_start)
if table_end == -1:
    table_end = content.find("\n\n## 📚", table_start)

table_text = content[table_start:table_end]

lines = table_text.split("\n")

# 한국어 헤더 적용
header = "| # | 이름 | 공식 웹사이트 | 지원 모델 | Base URL | API 지연 시간 | 공식 웹사이트 지연 시간 |"
align = "|:---:|:---|:---|:---|:---|:---:|:---:|"
new_lines = [header, align]

row_re = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*\[([^\]]+)\]\((https?://[^)]+)\)\s*"
    r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$",
    re.MULTILINE,
)

old_row_re = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*\[([^\]]+)\]\((https?://[^)]+)\)\s*"
    r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|$",
    re.MULTILINE,
)

providers = []
for match in row_re.finditer(table_text):
    providers.append({
        "index": int(match.group(1)),
        "name": match.group(2).strip(),
        "domain": match.group(3).strip(),
        "homepage": match.group(4).strip(),
        "models": match.group(5).strip(),
        "api_url": match.group(6).strip(),
        "api_latency": match.group(7).strip(),
        "latency": match.group(8).strip(),
    })

if not providers:
    for match in old_row_re.finditer(table_text):
        providers.append({
            "index": int(match.group(1)),
            "name": match.group(2).strip(),
            "domain": match.group(3).strip(),
            "homepage": match.group(4).strip(),
            "models": match.group(5).strip(),
            "api_url": "확인 필요", 
            "api_latency": "-",
            "latency": match.group(6).strip().replace("超时", "시간 초과"),
        })

# 응답 속도순 자동 정렬 로직 추가
def parse_latency(ms_str):
    if "시간 초과" in ms_str or "超时" in ms_str or "-" in ms_str:
        return float('inf')
    return int(ms_str.replace("ms", "").strip())

providers.sort(key=lambda x: parse_latency(x['latency']))

# 재조립 (번호 재부여)
for i, p in enumerate(providers, 1):
    line = (
        f"| {i} | {p['name']} | [{p['domain']}]({p['homepage']}) | "
        f"{p['models']} | {p['api_url']} | {p['api_latency']} | {p['latency']} |"
    )
    new_lines.append(line)

new_table = "\n".join(new_lines)
new_content = content[:table_start] + new_table + content[table_end:]

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"한국어 포맷으로 {len(providers)}개의 서비스 테이블이 재구성 및 속도순 정렬되었습니다.")
