"""
Add meaningful new commercial relay services from>
These are services with proper commercial-style d>
"""
import re

README_PATH = "README.md"

new_entries = [
    ("OfoxAI", "ofox.ai", "다중 모델"),
    ("VVCode", "vvcode.top", "다중 모델"),
    ("MKE AI", "tb-api.mkeai.com", "다중 모델"),
    ("词元流动", "tokenflux.dev", "다중 모델"),
    ("9Router", "9router.com", "다중 모델"),
    ("ABC Relay", "abcrelay.com", "다중 모델"),
    ("OpenCode", "opencode.ai", "다중 모델"),
    ("DuckCoding", "duckcoding.ai", "다중 모델"),
    ("ocool AI", "ocool.ai", "다중 모델"),
    ("NUWA", "nuwaapi.com", "다중 모델"),
    ("极速AI", "aicodee.com", "다중 모델"),
    ("巨量API", "api.yidvps.cn", "다중 모델"),
    ("晴辰云", "gpt.qt.cool", "다중 모델"),
    ("丰思理 AI", "ai.fengsili.online", "다중 모델"),
    ("全球AI", "globalai.vip", "다중 모델"),
    ("ChatGTP", "chatgtp.cn", "다중 모델"),
    ("UniAiX", "uniaix.com", "다중 모델"),
    ("艾可API", "aicanapi.com", "다중 모델"),
    ("简易-API中转站", "jeniya.top", "다중 모델"),
    ("简小智API中转站", "newapi.jianxiaozhi.chat", "다중 모델"),
    ("小智API", "newai.aichat.ink", "다중 모델"),
    ("一叶知秋API", "88996.cloud", "다중 모델"),
    ("AI98", "ai98.vip", "다중 모델"),
    ("Aizex API", "aizex.top", "다중 모델"),
    ("黑与白公益站", "ai.hybgzs.com", "다중 모델"),
    ("AI新境", "aixj.vip", "다중 모델"),
    ("酸枝云", "suanzhi.cloud", "다중 모델"),
    ("MonkingAI", "monking.ai", "다중 모델"),
    ("EnenCloud API", "api.enencloud.top", "다중 모델"),
    ("PackyAPI", "codex-api.packycode.com", "다중 모델"),
    ("HotaruAPI", "api.hotaruapi.top", "다중 모델"),
    ("AiroeAI", "ai.airoe.cn", "다중 모델"),
    ("InstCopilot API", "instcopilot-api.com", "다중 모델"),
    ("GPTBest", "gptbest", "다중 모델"),
    ("F2API", "api.f2api.com", "다중 모델"),
    ("GPTs API", "gptsapi", "다중 모델"),
    ("Smz Ai", "smz6.com", "다중 모델"),
    ("Undy API", "vip.undyingapi.com", "다중 모델"),
    ("NanoGPT", "nano-gpt.com", "다중 모델"),
    ("Yun API", "api.zyai.online", "다중 모델"),
]

with open(README_PATH, "r", encoding="utf-8") as f:
    readme = f.read()

# 한국어 헤더 기준으로 삽입 위치 변경
insert_point = readme.find("\n\n## 📚 데이터 출처")

new_rows = ""
for name, domain, models in new_entries:
    url = f"https://{domain}"
    # 7열 포맷에 맞게 데이터 삽입 (| 번호 | 이름 | 사이트 | 모델 | Base URL | 핑1 | 핑2 |)
    new_rows += f"| | {name} | [{domain}]({url}) | {models} | 확인 필요 | | |\n"

new_readme = readme[:insert_point] + "\n" + new_rows + readme[insert_point:]

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)

print(f"Added {len(new_entries)} new entries to README")
