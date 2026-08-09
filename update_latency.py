import re
import subprocess
import platform
import time
import socket
import urllib.request
import urllib.error
from pathlib import Path

README_PATH = "README.md"

with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 한국어 헤더로 수정
table_start = content.find("| # | 이름 | 공식 웹사이트 |")
table_end = content.find("\n\n---\n\n## 📚", table_start)
if table_end == -1:
    table_end = content.find("\n\n## 📚", table_start)

table_text = content[table_start:table_end]

row_re = re.compile(
    r"^\|\s*(\d*)\s*\|\s*(.*?)\s*\|\s*\[([^\]]+)\]\((https?://[^)]+)\)\s*"
    r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$",
    re.MULTILINE,
)

providers = []
# 7열 정규식 파싱
for match in row_re.finditer(table_text):
    index_val = match.group(1).strip()
    providers.append({
        "index": int(index_val) if index_val else 0,
        "name": match.group(2).strip(),
        "domain": match.group(3).strip(),
        "homepage": match.group(4).strip(),
        "models": match.group(5).strip(),
        "api_url": match.group(6).strip(),
        "api_latency": match.group(7).strip(),
        "latency": match.group(8).strip(),
    })

print(f"Found {len(providers)} rows to test")

def test_domain(domain):
    try:
        start = time.time()
        sock = socket.create_connection((domain, 443), timeout=5)
        elapsed = int((time.time() - start) * 1000)
        sock.close()
        return elapsed, True
    except:
        pass
    return None, False

new_providers = []
for i, p in enumerate(providers):
    domain = p['domain'].split('/')[0].replace('www.', '')
    
    name_clean = p['name'].lstrip("❌ ").strip()
    while name_clean.startswith("❌"):
        name_clean = name_clean[1:].strip()
    
    latency, ok = test_domain(domain)
    
    if latency is not None:
        latency_str = f"{latency}ms"
        status = "✅"
    else:
        latency_str = "시간 초과"
        name_clean = f"❌ {name_clean}"
        status = "❌"
    
    p['name'] = name_clean
    p['latency'] = latency_str
    new_providers.append(p)
    print(f"{i+1:3d}. {status} {name_clean:<30s} {domain:<35s} {latency if latency else '시간 초과'}ms")
    time.sleep(0.05)

def sort_key(p):
    latency_val = 999999
    if p['latency'] and p['latency'] != "시간 초과" and p['latency'] != "-":
        try:
            latency_val = int(p['latency'].replace("ms", ""))
        except ValueError:
            pass
    homepage_priority = 0 if latency_val < 999999 else 1
    return (homepage_priority, latency_val, p['name'].lower())

providers_sorted = sorted(new_providers, key=sort_key)

header = "| # | 이름 | 공식 웹사이트 | 지원 모델 | Base URL | API 지연 시간 | 공식 웹사이트 지연 시간 |"
align = "|:---:|:---|:---|:---|:---|:---:|:---:|"
new_lines = [header, align]

for i, p in enumerate(providers_sorted, 1):
    line = (
        f"| {i} | {p['name']} | [{p['domain']}]({p['homepage']}) | "
        f"{p['models']} | {p['api_url']} | {p['api_latency']} | {p['latency']} |"
    )
    new_lines.append(line)

new_table = "\n".join(new_lines)
new_content = content[:table_start] + new_table + content[table_end:]

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"\nUpdated {len(new_providers)} entries successfully.")

