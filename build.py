#!/usr/bin/env python3
"""Render docs/index.html from data/status.json and template.css.

Run from the repo root:  python3 build.py
"""
import datetime
import html
import json

E = html.escape
CSS = open("template.css", encoding="utf-8").read()
D = json.load(open("data/status.json", encoding="utf-8"))

SITE_KR = "https://kotradoha.github.io/qatar-korea-flight-monitor/"
CLS = {"운항": "ok", "예정": "plan", "일부결항": "part", "결항": "cx",
       "폐쇄": "closed", "미정": "unk", "–": "none"}
WD = ["월", "화", "수", "목", "금", "토", "일"]


def ref(ns):
    return "".join(f'<a class="ref" href="#s{n}">{n}</a>' for n in ns)


upd = datetime.datetime.fromisoformat(D["updated_at"])
upd_txt = f"{upd:%Y-%m-%d} ({WD[upd.weekday()]}) {upd:%H:%M}"
start = datetime.date.fromisoformat(D["window_start"])
days = [start + datetime.timedelta(days=i) for i in range(len(D["grid"][0]["status"]))]
span = f"{days[0].month}/{days[0].day} ~ {days[-1].month}/{days[-1].day}"

pills = "".join(f'<span class="pill">{p["text"]} {ref(p["refs"])}</span>' for p in D["pills"])
kps = "".join(f'<li>{k["html"]} {ref(k["refs"])}</li>' for k in D["key_points"])

card_parts = []
for c in D["cards"]:
    card_parts.append(
        f'<div class="qc {c["cls"]}"><div class="qh">'
        f'<span class="qcity">{E(c["city"])} <small>{E(c["iata"])}</small></span>'
        f'<span class="qv">{E(c["verdict"])}</span></div>'
        f'<div class="qcar">{E(c["carriers"])}</div>'
        f'<div class="qt">{E(c["times"])}</div>'
        f'<div class="qn">{E(c["note"])} {ref(c["refs"])}</div></div>')
cards = "".join(card_parts)

ths = "".join(
    f'<th class="d{" we" if d.weekday() in (4, 5) else ""}">{d.day}<br><span>{WD[d.weekday()]}</span></th>'
    for d in days)

row_parts = []
for r in D["grid"]:
    cells = "".join(
        f'<td class="d"><span class="c {CLS[s]}">{"" if s == "–" else E(s)}</span></td>'
        for s in r["status"])
    row_parts.append(
        f'<tr><th class="city">{E(r["city"])}</th><td class="air">{E(r["airline"])}</td>'
        f'{cells}<td class="rf">{ref(r["refs"])}</td></tr>')
rows = "".join(row_parts)

nf = "".join(f'<li><b>{E(x["city"])}</b> {E(x["note"])} {ref(x["refs"])}</li>' for x in D["no_direct"])
road = "".join(f'<li>{x["html"]} {ref(x["refs"])}</li>' for x in D["road"])
srcs = "".join(
    f'<li id="s{s["n"]}"><span class="sn">{s["n"]}</span><div>'
    f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["name"])}</a> '
    f'<span class="st">{E(s["kind"])} · {E(s["date"])}</span>'
    f'<div class="sw">{E(s["what"])}</div></div></li>'
    for s in D["sources"])

page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>사우디→도하 항공편 현황판 | Saudi Arabia → Doha Flight Status</title>
<meta name="description" content="사우디아라비아 각 도시에서 도하로 가는 직항의 운항·결항 여부와 공항 상황을 1시간 단위로 업데이트하는 참고용 현황판">
<style>{CSS}</style></head><body><div class="w">
<a class="krbtn" href="{SITE_KR}" target="_blank" rel="noopener"><span class="krbtn-t">도하 → 한국 항공편 현황 보기</span><span class="krbtn-s">카타르항공 도하↔인천 운항·지연·결항 현황판 ↗</span></a>
<header><div><h1>사우디 → 도하 항공편 현황</h1></div></header>
<p class="intro">사우디아라비아에 체류 중인 우리 국민과 기업인의 도하 이동(대피) 판단을 돕기 위해, 사우디 각 도시와 도하를 잇는 직항의 운항·결항 여부와 사우디 공항 상황을 <b>1시간 단위로 업데이트</b>하여 보여주는 현황판입니다. 도시별로 지금 이용할 수 있는지를 먼저 보여드리고, 향후 약 열흘간의 날짜별 운항 전망과 근거 자료를 함께 제공합니다.</p>
<div class="ts" style="margin-top:8px">업데이트 시점 <b>{upd_txt}</b> 도하 시각</div>
<div class="meta">{pills}</div>

<section class="sum"><h2>핵심 요점</h2><ol>{kps}</ol></section>

<h2 class="sec">도시별 — 지금 탈 수 있나</h2>
<p class="sub">사우디 출발 → 도하 기준이며, 이용하기 좋은 순서로 놓았습니다.</p>
<div class="qgrid">{cards}</div>

<h2 class="sec">날짜별 운항 현황 {span}</h2>
<p class="sub">도하 직항이 있는 모든 항공사를 넣었습니다. 오른쪽 숫자는 근거 번호입니다.</p>
<div class="card"><div class="legend">
<span><i class="c ok">운항</i>실제 운항 확인</span><span><i class="c plan">예정</i>결항 공지 없음</span><span><i class="c part">일부결항</i>일부 편 결항</span><span><i class="c cx">결항</i>결항 확인</span><span><i class="c closed">폐쇄</i>공항 폐쇄</span><span><i class="c unk">미정</i>재개 불확실</span><span>빈칸 = 운항 요일 아님</span></div>
<div class="scroll"><table><thead><tr><th class="city">도시</th><th style="text-align:left">항공사</th>{ths}<th>근거</th></tr></thead><tbody>{rows}</tbody></table></div></div>

<div class="two" style="margin-top:12px">
<div class="card"><h3>도하 직항이 없는 도시</h3><p class="sub">육로로 이동하거나 국내선으로 제다·메디나를 거쳐야 합니다.</p><ul>{nf}</ul></div>
<div class="card"><h3>육로 참고</h3><ul>{road}</ul></div>
</div>

<h2 class="sec">근거 자료</h2>
<p class="sub">항공사 공지 · 언론 보도 · 항공편 추적 사이트를 서로 대조했습니다. 추적 사이트 자료는 항공사의 공식 발표가 아닙니다.</p>
<ol class="srcs">{srcs}</ol>

<div class="how"><h3>※ 데이터 출처·판단 방식</h3><ul>
<li><b>공항 폐쇄·운영 여부</b> → 사우디 민간항공청(GACA) 발표와 공항 NOTAM(항공고시보)을 전한 주요 통신사(Reuters 등)·항공 전문지 보도를 기준으로 합니다. 공식 재개 일정이 없으면 ‘미정’으로 둡니다.</li>
<li><b>운항</b> → 항공편 추적 사이트(Flightradar24·Planefinder 등)에서 기체 신호(ADS-B)로 <b>실제 이착륙이 확인된 편</b>만 표시합니다.</li>
<li><b>결항·일부결항</b> → 항공사 공지, 언론 보도, 또는 추적 사이트의 결항 표시를 근거로 합니다. 추적 사이트 표시는 항공사 공식 발표가 아니므로 근거 번호로 구분해 두었습니다.</li>
<li><b>예정</b> → 항공사 스케줄상 운항 예정이고, 결항 공지·표시가 없는 편입니다. 운항 보장을 뜻하지 않습니다.</li>
<li><b>대상 노선</b> → 사우디 각 도시–도하 직항을 운항하는 모든 항공사(카타르항공·사우디아·플라이나스)를 포함합니다. 경유편은 넣지 않았습니다.</li>
</ul></div>

<div class="notice">본 페이지는 사우디 내 우리 국민과 기업인의 이동 판단에 도움을 드리고자, Claude와 GitHub을 활용해 공개된 항공사 공지·언론 보도·항공편 추적 정보를 1시간마다 다시 확인해 정리하는 참고용 모니터링 자료입니다. 일시적인 오류나 반영 지연이 있을 수 있고 운항 상황은 수시로 바뀌므로, 예약·변경과 출발 여부는 반드시 해당 항공사(<a href="https://fs.qatarairways.com/" target="_blank" rel="noopener">카타르항공 항공편 현황</a>, <a href="https://www.saudia.com/" target="_blank" rel="noopener">사우디아</a>, <a href="https://www.flynas.com/" target="_blank" rel="noopener">플라이나스</a>) 공식 채널에서 최종 확인해 주시기 바랍니다.</div>
<div class="issuer"><span>작성(클로드 기반): 주카타르대사관·도하무역관</span><span>긴급 시 외교부 영사콜센터 +82-2-3210-0404 (24시간)</span></div>
</div></body></html>"""

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(page)
print("built docs/index.html", len(page))
