import re
import os
from pathlib import Path
from datetime import datetime

# 파일명 생성 (안드로이드 파일 시스템 호환을 위해 시간의 ':'는 제외)
# 예: AI API Proxy List 260809 1104.txt
current_time = datetime.now().strftime("%y%m%d %H%M")
filename = f"AI API Proxy List {current_time}.txt"

# 터묵스 다운로드 경로 맵핑
download_dir = Path.home() / "storage/downloads"
if not download_dir.exists():
    print("오류: 저장소 권한이 없습니다. 'termux-setup-storage'를 먼저 실행하세요.")
    exit(1)

file_path = download_dir / filename
readme_path = Path("README.md")

if not readme_path.exists():
    print("오류: README.md 파일을 찾을 수 없습니다. 원본 스크립트를 먼저 실행했는지 확인하세요.")
    exit(1)

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 정규식으로 README 데이터 추출
row_re = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*\[([^\]]+)\]\((https?://[^)]+)\)\s*"
    r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$",
    re.MULTILINE,
)

providers = []
for match in row_re.finditer(content):
    providers.append({
        "name": match.group(2).strip(),
        "domain": match.group(3).strip(),
        "latency": match.group(8).strip(),
    })

# 응답 속도순 정렬 (타임아웃은 후순위 배치)
def parse_latency(ms_str):
    if "超时" in ms_str or "-" in ms_str:
        return float('inf')
    return int(ms_str.replace("ms", "").strip())

providers.sort(key=lambda x: parse_latency(x['latency']))

# 텍스트 파일로 저장
with open(file_path, "w", encoding="utf-8") as f:
    f.write("순위 | 서비스명 | 응답 속도 | 도메인\n")
    f.write("-" * 50 + "\n")
    for i, p in enumerate(providers, 1):
        f.write(f"{i} | {p['name']} | {p['latency']} | {p['domain']}\n")

print(f"다운로드 폴더에 정상적으로 저장되었습니다: {filename}")
