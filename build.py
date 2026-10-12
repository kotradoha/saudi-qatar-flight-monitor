#!/usr/bin/env python3
"""Render docs/index.html (Korean / English / Arabic) from data/status.json and template.css.

Run from the repo root:  python3 build.py
Every text field in data/status.json is {"ko": ..., "en": ..., "ar": ...}.
"""
import datetime
import html
import json

E = html.escape
LANGS = ["ko", "en", "ar"]
with open("template.css", encoding="utf-8") as f:
    CSS = f.read()
with open("data/status.json", encoding="utf-8") as f:
    D = json.load(f)

SITE_KR = "https://kotradoha.github.io/qatar-korea-flight-monitor/"
CLS = {"운항": "ok", "예정": "plan", "일부결항": "part", "결항": "cx",
       "폐쇄": "closed", "미정": "unk", "–": "none"}

UI = {
 "ko": {
  "title": "사우디 → 도하 항공편 현황",
  "op": "주카타르한국대사관·도하무역관 운영",
  "kr_btn": "도하 → 한국 항공편 현황 보기",
  "kr_btn_sub": "카타르항공 도하↔인천 운항·지연·결항 현황판 ↗",
  "intro": "사우디아라비아에 체류 중인 우리 국민과 기업인의 도하 이동(대피) 판단을 돕기 위해, 사우디 각 도시와 도하를 잇는 직항의 운항·결항 여부와 사우디 공항 상황을 <b>1시간 단위로 업데이트</b>하여 보여주는 현황판입니다. 도시별로 지금 이용할 수 있는지를 먼저 보여드리고, 향후 약 열흘간의 날짜별 운항 전망과 근거 자료를 함께 제공합니다.",
  "updated": "업데이트 시점 <b>{t}</b> 도하 시각",
  "summary": "핵심 요점",
  "cities": "도시별 — 지금 탈 수 있나",
  "cities_sub": "사우디 출발 → 도하 기준이며, 이용하기 좋은 순서로 놓았습니다.",
  "daily": "날짜별 운항 현황 {span}",
  "daily_sub": "도하 직항이 있는 모든 항공사를 넣었습니다. 오른쪽 숫자는 근거 번호입니다.",
  "th_city": "도시", "th_air": "항공사", "th_ref": "근거",
  "st": {"운항": "운항", "예정": "예정", "일부결항": "일부결항", "결항": "결항", "폐쇄": "폐쇄", "미정": "미정"},
  "lg": {"운항": "실제 운항 확인", "예정": "결항 공지 없음", "일부결항": "일부 편 결항", "결항": "결항 확인", "폐쇄": "공항 폐쇄", "미정": "재개 불확실"},
  "lg_blank": "빈칸 = 운항 요일 아님",
  "nodirect": "도하 직항이 없는 도시",
  "nodirect_sub": "육로로 이동하거나 국내선으로 제다·메디나를 거쳐야 합니다.",
  "road": "육로 참고",
  "sources": "근거 자료",
  "sources_sub": "항공사 공지 · 언론 보도 · 항공편 추적 사이트를 서로 대조했습니다. 추적 사이트 자료는 항공사의 공식 발표가 아닙니다.",
  "kind": {"언론 보도": "언론 보도", "항공편 추적": "항공편 추적", "항공 전문지": "항공 전문지", "경로 안내": "경로 안내", "항공사 공지": "항공사 공지", "정부 발표": "정부 발표"},
  "how_h": "※ 데이터 출처·판단 방식",
  "how": [
   "<b>공항 폐쇄·운영 여부</b> → 사우디 민간항공청(GACA) 발표와 공항 NOTAM(항공고시보)을 전한 주요 통신사(Reuters 등)·항공 전문지 보도를 기준으로 합니다. 공식 재개 일정이 없으면 ‘미정’으로 둡니다.",
   "<b>운항</b> → 항공편 추적 사이트(Flightradar24·Planefinder 등)에서 기체 신호(ADS-B)로 <b>실제 이착륙이 확인된 편</b>만 표시합니다.",
   "<b>결항·일부결항</b> → 항공사 공지, 언론 보도, 또는 추적 사이트의 결항 표시를 근거로 합니다. 추적 사이트 표시는 항공사 공식 발표가 아니므로 근거 번호로 구분해 두었습니다.",
   "<b>예정</b> → 항공사 스케줄상 운항 예정이고, 결항 공지·표시가 없는 편입니다. 운항 보장을 뜻하지 않습니다.",
   "<b>대상 노선</b> → 사우디 각 도시–도하 직항을 운항하는 모든 항공사(카타르항공·사우디아·플라이나스)를 포함합니다. 경유편은 넣지 않았습니다."],
  "notice": "본 페이지는 사우디 내 우리 국민과 기업인의 이동 판단에 도움을 드리고자, Claude와 GitHub을 활용해 공개된 항공사 공지·언론 보도·항공편 추적 정보를 1시간마다 다시 확인해 정리하는 참고용 모니터링 자료입니다. 일시적인 오류나 반영 지연이 있을 수 있고 운항 상황은 수시로 바뀌므로, 예약·변경과 출발 여부는 반드시 해당 항공사({links}) 공식 채널에서 최종 확인해 주시기 바랍니다.",
  "air_links": ["카타르항공 항공편 현황", "사우디아", "플라이나스"],
  "issuer": "작성(클로드 기반): 주카타르대사관·도하무역관",
  "consul": "긴급 시 외교부 영사콜센터 +82-2-3210-0404 (24시간)",
  "visits": "누적 방문:",
  "wd": ["월", "화", "수", "목", "금", "토", "일"],
 },
 "en": {
  "title": "Saudi Arabia → Doha Flight Status",
  "op": "Operated by the Embassy of the Republic of Korea in Qatar · KOTRA Doha",
  "kr_btn": "Doha → Korea Flight Status",
  "kr_btn_sub": "Qatar Airways Doha ↔ Incheon operations, delays and cancellations ↗",
  "intro": "This board helps Korean nationals and business travellers in Saudi Arabia decide how to travel (or evacuate) to Doha. It shows whether direct flights between Saudi cities and Doha are operating or cancelled, along with the status of Saudi airports, and is <b>updated every hour</b>. It first shows whether flights are available from each city now, then the outlook for the next ten days or so, with the sources behind each item.",
  "updated": "Updated <b>{t}</b> Doha time",
  "summary": "Key points",
  "cities": "By city — can you fly now?",
  "cities_sub": "Saudi Arabia → Doha, listed from the most to the least usable.",
  "daily": "Daily flight status, {span}",
  "daily_sub": "Includes every airline flying direct to Doha. Numbers on the right refer to the sources.",
  "th_city": "City", "th_air": "Airline", "th_ref": "Sources",
  "st": {"운항": "Operated", "예정": "Scheduled", "일부결항": "Partial", "결항": "Cancelled", "폐쇄": "Closed", "미정": "TBC"},
  "lg": {"운항": "Operation confirmed", "예정": "No cancellation announced", "일부결항": "Some flights cancelled", "결항": "Cancellation confirmed", "폐쇄": "Airport closed", "미정": "Resumption uncertain"},
  "lg_blank": "Blank = no flight that day",
  "nodirect": "Cities without direct flights to Doha",
  "nodirect_sub": "Travel by road, or take a domestic flight to Jeddah or Madinah first.",
  "road": "Travelling by road",
  "sources": "Sources",
  "sources_sub": "Airline notices, news reports and flight-tracking sites were cross-checked. Flight-tracking data is not an official airline announcement.",
  "kind": {"언론 보도": "News report", "항공편 추적": "Flight tracker", "항공 전문지": "Aviation trade press", "경로 안내": "Route planner", "항공사 공지": "Airline notice", "정부 발표": "Government announcement"},
  "how_h": "※ Sources and how each status is determined",
  "how": [
   "<b>Airport closures and operations</b> → Based on announcements by Saudi Arabia’s General Authority of Civil Aviation (GACA) and airport NOTAMs (notices to airmen), as reported by major news agencies (such as Reuters) and the aviation trade press. If no official reopening date has been given, the status is shown as ‘TBC’.",
   "<b>Operated</b> → Shown only for flights whose <b>actual take-off and landing</b> were confirmed by flight-tracking sites (such as Flightradar24 and Planefinder) using aircraft signals (ADS-B).",
   "<b>Cancelled / Partial</b> → Based on airline notices, news reports, or cancellations shown on flight-tracking sites. Flight-tracking data is not an official airline announcement, so it is identified separately in the source numbers.",
   "<b>Scheduled</b> → Flights in the airline’s schedule for which no cancellation has been announced or shown. This does not guarantee the flight will operate.",
   "<b>Routes covered</b> → All airlines flying direct between Saudi cities and Doha (Qatar Airways, Saudia and flynas). Connecting flights are not included."],
  "notice": "This page is a reference monitoring tool, built with Claude and GitHub, that re-checks public airline notices, news reports and flight-tracking data every hour to help Korean nationals and business travellers in Saudi Arabia plan their travel. There may be temporary errors or delays in updates, and flight operations can change at any time, so please always obtain final confirmation of bookings, changes and departures through the airline’s official channels ({links}).",
  "air_links": ["Qatar Airways flight status", "Saudia", "flynas"],
  "issuer": "Prepared with Claude by the Embassy of the Republic of Korea in Qatar · KOTRA Doha",
  "consul": "In an emergency: Korean MOFA Consular Call Center +82-2-3210-0404 (24 hours)",
  "visits": "Total visits:",
  "wd": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
 },
 "ar": {
  "title": "حالة الرحلات من السعودية إلى الدوحة",
  "op": "تديرها سفارة جمهورية كوريا لدى قطر · كوترا الدوحة",
  "kr_btn": "حالة الرحلات من الدوحة إلى كوريا",
  "kr_btn_sub": "تشغيل رحلات الخطوط الجوية القطرية بين الدوحة وإنتشون وتأخيرها وإلغاؤها ↗",
  "intro": "تساعد هذه اللوحة المواطنين الكوريين ورجال الأعمال الكوريين الموجودين في المملكة العربية السعودية على اتخاذ قرار السفر (أو الإجلاء) إلى الدوحة. وتعرض حالة الرحلات المباشرة بين المدن السعودية والدوحة من حيث التسيير أو الإلغاء، إلى جانب أوضاع المطارات السعودية، <b>وتُحدَّث كل ساعة</b>. وتبيّن أولًا مدى توفر الرحلات حاليًا من كل مدينة، ثم توقعات تسيير الرحلات خلال الأيام العشرة المقبلة تقريبًا، مع المصادر المعتمدة لكل معلومة.",
  "updated": "آخر تحديث <b>{t}</b> بتوقيت الدوحة",
  "summary": "أبرز النقاط",
  "cities": "حسب المدينة — هل يمكنك السفر الآن؟",
  "cities_sub": "من السعودية إلى الدوحة، مرتبة من الأكثر إلى الأقل إتاحة.",
  "daily": "حالة الرحلات اليومية، {span}",
  "daily_sub": "تشمل جميع شركات الطيران التي تسيّر رحلات مباشرة إلى الدوحة. تشير الأرقام في العمود الأخير إلى المصادر.",
  "th_city": "المدينة", "th_air": "شركة الطيران", "th_ref": "المصادر",
  "st": {"운항": "سُيِّرت", "예정": "مجدولة", "일부결항": "إلغاء جزئي", "결항": "ملغاة", "폐쇄": "مغلق", "미정": "غير مؤكدة"},
  "lg": {"운항": "تأكّد تسييرها فعليًا", "예정": "لم يُعلَن إلغاؤها", "일부결항": "إلغاء بعض الرحلات", "결항": "تأكّد إلغاؤها", "폐쇄": "المطار مغلق", "미정": "استئنافها غير مؤكد"},
  "lg_blank": "الخانة الفارغة = لا رحلة في ذلك اليوم",
  "nodirect": "مدن لا توجد منها رحلات مباشرة إلى الدوحة",
  "nodirect_sub": "يجب السفر برًّا، أو التوجّه أولًا إلى جدة أو المدينة المنورة على متن رحلة داخلية.",
  "road": "السفر برًّا",
  "sources": "المصادر",
  "sources_sub": "جرت مقارنة إشعارات شركات الطيران والتقارير الإخبارية ومواقع تتبّع الرحلات. وبيانات مواقع التتبّع ليست إعلانًا رسميًا من شركات الطيران.",
  "kind": {"언론 보도": "تقرير إخباري", "항공편 추적": "موقع تتبّع رحلات", "항공 전문지": "صحافة طيران متخصصة", "경로 안내": "دليل مسارات", "항공사 공지": "إشعار شركة طيران", "정부 발표": "إعلان حكومي"},
  "how_h": "※ مصادر البيانات وطريقة تحديد الحالة",
  "how": [
   "<b>إغلاق المطارات وتشغيلها</b> ← تستند إلى إعلانات الهيئة العامة للطيران المدني السعودية وإشعارات NOTAM (إشعارات الطيارين) الخاصة بالمطارات، كما نقلتها وكالات الأنباء الكبرى (مثل رويترز) والصحافة المتخصصة في الطيران. وإذا لم يُعلَن موعد رسمي لإعادة الفتح، تُعرض الحالة على أنها «غير مؤكدة».",
   "<b>سُيِّرت</b> ← تُعرض فقط للرحلات التي <b>تأكّد إقلاعها وهبوطها فعليًا</b> عبر مواقع تتبّع الرحلات (مثل Flightradar24 وPlanefinder) استنادًا إلى إشارات الطائرات (ADS-B).",
   "<b>ملغاة / إلغاء جزئي</b> ← تستند إلى إشعارات شركات الطيران أو التقارير الإخبارية أو الإلغاءات الظاهرة في مواقع التتبّع. وبما أن بيانات مواقع التتبّع ليست إعلانًا رسميًا من شركات الطيران، فقد مُيِّزت في أرقام المصادر.",
   "<b>مجدولة</b> ← رحلات مدرجة في جدول شركة الطيران ولم يُعلَن أو يظهر إلغاؤها. ولا يعني ذلك ضمان تسييرها.",
   "<b>الخطوط المشمولة</b> ← جميع شركات الطيران التي تسيّر رحلات مباشرة بين المدن السعودية والدوحة (الخطوط الجوية القطرية والخطوط السعودية وطيران ناس). ولا تشمل الرحلات غير المباشرة."],
  "notice": "هذه الصفحة أداة متابعة للاسترشاد، أُنشئت باستخدام Claude وGitHub، تعيد كل ساعة التحقق من إشعارات شركات الطيران والتقارير الإخبارية وبيانات تتبّع الرحلات المتاحة للعموم، لمساعدة المواطنين الكوريين ورجال الأعمال في السعودية على تخطيط سفرهم. وقد تحدث أخطاء أو تأخيرات مؤقتة في التحديث، كما قد يتغير تشغيل الرحلات في أي وقت، لذا يُرجى دائمًا الحصول على التأكيد النهائي للحجز والتعديل والمغادرة عبر القنوات الرسمية لشركة الطيران ({links}).",
  "air_links": ["حالة رحلات الخطوط الجوية القطرية", "الخطوط السعودية", "طيران ناس"],
  "issuer": "أُعدّت باستخدام Claude من قِبل سفارة جمهورية كوريا لدى قطر · كوترا الدوحة",
  "consul": "في حالات الطوارئ: مركز الاتصال القنصلي التابع لوزارة الخارجية الكورية <bdi dir=\"ltr\">+82-2-3210-0404</bdi> (على مدار 24 ساعة)",
  "visits": "إجمالي الزيارات:",
  "wd": ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"],
 },
}
MONTH_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_AR = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
AIR_URLS = ["https://fs.qatarairways.com/", "https://www.saudia.com/", "https://www.flynas.com/"]


def T(x, lang):
    """Pick one language from a {ko,en,ar} field (plain strings pass through)."""
    if isinstance(x, dict):
        v = x.get(lang)
        if not v:
            raise SystemExit(f"missing '{lang}' text: {x}")
        return v
    return x


def fmt_day(d, lang):
    if lang == "ko":
        return f"{d.month}/{d.day}"
    if lang == "en":
        return f"{d.day} {MONTH_EN[d.month - 1]}"
    return f"{d.day} {MONTH_AR[d.month - 1]}"


upd = datetime.datetime.fromisoformat(D["updated_at"])
start = datetime.date.fromisoformat(D["window_start"])
days = [start + datetime.timedelta(days=i) for i in range(len(D["grid"][0]["status"]))]


def render(lang):
    U = UI[lang]
    wd = U["wd"]
    pre = "s" if lang == "ko" else f"s{lang}-"

    def ref(ns):
        return "".join(f'<a class="ref" href="#{pre}{n}">{n}</a>' for n in ns)

    if lang == "ko":
        upd_txt = f"{upd:%Y-%m-%d} ({wd[upd.weekday()]}) {upd:%H:%M}"
        span = f"{fmt_day(days[0], lang)} ~ {fmt_day(days[-1], lang)}"
    elif lang == "en":
        upd_txt = f"{wd[upd.weekday()]} {upd.day} {MONTH_EN[upd.month - 1]} {upd.year}, {upd:%H:%M}"
        span = f"{fmt_day(days[0], lang)} – {fmt_day(days[-1], lang)}"
    else:
        upd_txt = f"{wd[upd.weekday()]} {upd.day} {MONTH_AR[upd.month - 1]} {upd.year}، الساعة {upd:%H:%M}"
        span = f"من {fmt_day(days[0], lang)} إلى {fmt_day(days[-1], lang)}"

    pills = "".join(f'<span class="pill">{T(p["text"], lang)} {ref(p["refs"])}</span>' for p in D["pills"])
    kps = "".join(f'<li>{T(k["html"], lang)} {ref(k["refs"])}</li>' for k in D["key_points"])
    cards = "".join(
        f'<div class="qc {c["cls"]}"><div class="qh">'
        f'<span class="qcity">{E(T(c["city"], lang))} <small>{E(c["iata"])}</small></span>'
        f'<span class="qv">{E(T(c["verdict"], lang))}</span></div>'
        f'<div class="qcar">{E(T(c["carriers"], lang))}</div>'
        f'<div class="qt">{E(T(c["times"], lang))}</div>'
        f'<div class="qn">{E(T(c["note"], lang))} {ref(c["refs"])}</div></div>'
        for c in D["cards"])
    ths = "".join(
        f'<th class="d{" we" if d.weekday() in (4, 5) else ""}">{d.day}<br><span>{wd[d.weekday()]}</span></th>'
        for d in days)
    rows = "".join(
        f'<tr><th class="city">{E(T(r["city"], lang))}</th><td class="air">{E(T(r["airline"], lang))}</td>'
        + "".join(f'<td class="d"><span class="c {CLS[s]}">{"" if s == "–" else E(U["st"][s])}</span></td>'
                  for s in r["status"])
        + f'<td class="rf">{ref(r["refs"])}</td></tr>'
        for r in D["grid"])
    legend = "".join(f'<span><i class="c {CLS[k]}">{E(U["st"][k])}</i>{E(U["lg"][k])}</span>' for k in U["st"])
    nf = "".join(f'<li><b>{E(T(x["city"], lang))}</b> {E(T(x["note"], lang))} {ref(x["refs"])}</li>' for x in D["no_direct"])
    road = "".join(f'<li>{T(x["html"], lang)} {ref(x["refs"])}</li>' for x in D["road"])
    srcs = "".join(
        f'<li id="{pre}{s["n"]}"><span class="sn">{s["n"]}</span><div>'
        f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(T(s["name"], lang))}</a> '
        f'<span class="st">{E(U["kind"].get(s["kind"], s["kind"]))} · <bdi>{E(s["date"])}</bdi></span>'
        f'<div class="sw">{E(T(s["what"], lang))}</div></div></li>'
        for s in D["sources"])
    how = "".join(f"<li>{h}</li>" for h in U["how"])
    links = ", ".join(f'<a href="{u}" target="_blank" rel="noopener">{E(n)}</a>' for n, u in zip(U["air_links"], AIR_URLS))
    attrs = f' id="L-{lang}" lang="{lang}"' + (' dir="rtl"' if lang == "ar" else "") + ("" if lang == "ko" else " hidden")
    return f"""<div class="L"{attrs}>
<a class="krbtn" href="{SITE_KR}" target="_blank" rel="noopener"><span class="krbtn-t">{U["kr_btn"]}</span><span class="krbtn-s">{U["kr_btn_sub"]}</span></a>
<header><div><h1>{U["title"]}</h1><div class="op">{U["op"]}</div></div></header>
<p class="intro">{U["intro"]}</p>
<div class="ts" style="margin-top:8px">{U["updated"].format(t=upd_txt)}</div>
<div class="meta">{pills}</div>
<section class="sum"><h2>{U["summary"]}</h2><ol>{kps}</ol></section>
<h2 class="sec">{U["cities"]}</h2>
<p class="sub">{U["cities_sub"]}</p>
<div class="qgrid">{cards}</div>
<h2 class="sec">{U["daily"].format(span=span)}</h2>
<p class="sub">{U["daily_sub"]}</p>
<div class="card"><div class="legend">{legend}<span>{U["lg_blank"]}</span></div>
<div class="scroll"><table><thead><tr><th class="city">{U["th_city"]}</th><th class="airh">{U["th_air"]}</th>{ths}<th>{U["th_ref"]}</th></tr></thead><tbody>{rows}</tbody></table></div></div>
<div class="two" style="margin-top:12px">
<div class="card"><h3>{U["nodirect"]}</h3><p class="sub">{U["nodirect_sub"]}</p><ul>{nf}</ul></div>
<div class="card"><h3>{U["road"]}</h3><ul>{road}</ul></div>
</div>
<h2 class="sec">{U["sources"]}</h2>
<p class="sub">{U["sources_sub"]}</p>
<ol class="srcs">{srcs}</ol>
<div class="how"><h3>{U["how_h"]}</h3><ul>{how}</ul></div>
<div class="notice">{U["notice"].format(links=links)}</div>
<div class="issuer"><span>{U["issuer"]}</span><span>{U["consul"]}</span></div>
<div class="counter"><span>{U["visits"]}</span><img class="hitsBadge" alt="visitor count"></div>
</div>"""


sections = "\n".join(render(l) for l in LANGS)

SCRIPT = r"""
function ls_get(k){ try { return window.localStorage ? localStorage.getItem(k) : null; } catch(e){ return null; } }
function ls_set(k,v){ try { if (window.localStorage) localStorage.setItem(k,v); } catch(e){} }
function detectLang() {
  var s = ls_get("sqmon_lang");
  if (s === "ko" || s === "en" || s === "ar") return s;
  var n = (navigator.language || "").toLowerCase();
  if (n.indexOf("ko") === 0) return "ko";
  if (n.indexOf("ar") === 0) return "ar";
  return "en";
}
function setLang(l) {
  ["ko","en","ar"].forEach(function(x){
    document.getElementById("L-" + x).hidden = (x !== l);
    document.getElementById("lang" + x.charAt(0).toUpperCase() + x.slice(1)).className = (x === l) ? "on" : "";
  });
  document.documentElement.lang = l;
  document.documentElement.dir = (l === "ar") ? "rtl" : "ltr";
  ls_set("sqmon_lang", l);
}
setLang(detectLang());
(function () {
  var imgs = document.querySelectorAll(".hitsBadge");
  if (!imgs.length) return;
  var base = "https://hits.sh/" + location.hostname +
    location.pathname.replace(/index\.html$/, "") + ".svg?label=visits&color=2a78d6";
  var tries = 0, ok = false, img = imgs[0];
  img.onload = function () { ok = true; for (var i = 1; i < imgs.length; i++) imgs[i].src = img.src; };
  function attempt() {
    if (ok) return;
    tries++;
    img.src = base + (tries > 1 ? "&_=" + Date.now() : "");
    if (tries < 5) {
      setTimeout(function () { if (!ok && !img.complete) attempt(); }, 1200 * tries);
    } else if (!ok) {
      for (var i = 0; i < imgs.length; i++) imgs[i].parentElement.style.display = "none";
    }
  }
  img.onerror = function () { if (!ok && tries < 5) setTimeout(attempt, 500); };
  attempt();
})();
"""

page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>사우디→도하 항공편 현황판 | Saudi Arabia → Doha Flight Status | حالة الرحلات من السعودية إلى الدوحة</title>
<meta name="description" content="사우디아라비아 각 도시에서 도하로 가는 직항의 운항·결항 여부와 공항 상황을 1시간 단위로 업데이트하는 참고용 현황판">
<style>{CSS}</style></head><body><div class="w">
<div class="langrow"><div class="lang">
<button id="langKo" class="on" onclick="setLang('ko')">한국어</button>
<button id="langEn" onclick="setLang('en')">English</button>
<button id="langAr" onclick="setLang('ar')">العربية</button>
</div></div>
{sections}
</div>
<script>{SCRIPT}</script>
</body></html>"""

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(page)
print("built docs/index.html", len(page))
