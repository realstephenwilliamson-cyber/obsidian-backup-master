---
type: prompt
updated: 2026-10-21
---
# Calendar scripts

The method and scripts behind `Calendar/` (the panchang and the Shabbat and Yom Tov tables that Home's date box reads), copied from the 4 Oct 2026 record so a later run can extend or redo them. Used by [[Extend the calendar tables|Extend the calendar tables]].

These scripts produced `Calendar/Panchang <year> (Hickory).md` and `Calendar/Shabbat and Yom Tov times 2026-2029.md` (4 Oct 2026). Use them to extend the tables past 2029, or to change the places.

- Environment: Python 3 venv with `pyswisseph` (Swiss Ephemeris, Moshier mode, no data files) and `pyluach`. On Debian-style systems pyswisseph has to be built in a venv with fresh setuptools.
- Places: Hickory, NC (35.7332 N, 81.3412 W) and New York (40.71427 N, 74.00597 W, Hebcal geonameid 5128581); time zone America/New_York.
- Conventions:
  - **Panchang:** Lahiri ayanāṃśa; sunrise and sunset at the upper limb with refraction; amānta months named from the Sun's sidereal sign at the new moon (Adhika when no saṅkrānti); VS / Śaka / Saptarṣi turn at Caitra Śukla Pratipadā.
  - **Festival column (fest.py):** Ekādaśī, Pūrṇimā, Amāvāsyā on the day the tithi is current at sunrise (kṣaya tithi on the day it falls in); Saṅkrānti at the Sun's sidereal ingress, with time. Named festivals by time of day: sunrise (Navreh/Caitra Navarātri, Guru Pūrṇimā, Śāradīya Navarātri, Durgāṣṭamī, Mahānavamī, Vasanta Pañcamī), midday (Rāma Navamī, Gaṇeśa Caturthī), afternoon at 0.7 of daylight (Vijayādaśamī), pradoṣa at 0.1 of the night (Dīpāvalī, Holikā Dahan; Holī the next day), niśītha at the middle of the night (Janmāṣṭamī, Herath, Mahāśivarātri; if both nights qualify, the second). A tithi that begins after a new moon belongs to the next month.
  - **Shabbat:** Hebcal defaults. Candles 18 min before sunset, truncated to the minute. Havdalah when the Sun is 8.5° below the horizon (true altitude), rounded to the nearest minute.
  - **Yom Tov:** diaspora days from pyluach (`festival(israel=False, include_working_days=False)`).
- Checks:
  - New and full moons for Sep–Nov 2026 matched published times.
  - 4 Oct 2026 tithi, nakṣatra, yoga and karaṇa ends matched a published Delhi panchang to the minute.
  - New York candle lighting matched Hebcal-based times for Oct 2026 to Jan 2027.
  - Festivals: Drik Panchang's New York dates for autumn 2026 agree for Navarātri, Durgāṣṭamī, Mahānavamī, Vijayādaśamī, Dīpāvalī and the Ekādaśīs of 6 Oct, 21 Oct, 4 Nov (Drik puts Mokṣadā Ekādaśī on 19 Dec, the table on 20 Dec). CalendarLabs' 2027 dates (India) agree for Vasanta Pañcamī, Mahāśivarātri, Holikā Dahan, Holī, Ugādi, Guru Pūrṇimā, Navarātri and Dussehra; Rāma Navamī, Janmāṣṭamī, Gaṇeśa Caturthī, Durgāṣṭamī and Dīpāvalī fall a day earlier in Hickory, as expected for a western location.
- To extend: change `start, stop` in compute.py, run it, then fest.py, then gen.py. Copy the output notes into `Calendar/`; Home's date box reads them by year (column 11 is the festival column).

The `Calendar/` notes and Home's date box script (`Templates/Views/today-header/view.js`) are the deployed results.

## compute.py

```python
import swisseph as swe, datetime as dt, json, math
from zoneinfo import ZoneInfo
from pyluach import dates as hd
swe.set_ephe_path(None)
EF = swe.FLG_MOSEPH
swe.set_sid_mode(swe.SIDM_LAHIRI)
TZ = ZoneInfo('America/New_York')
PLACES = {'Hickory': (-81.3412, 35.7332, 350.0, 18), 'New York': (-74.00597, 40.71427, 10.0, 18)}
UTC = dt.timezone.utc
def jd_of(t):  # aware datetime -> jd UT
    u = t.astimezone(UTC); return swe.julday(u.year, u.month, u.day, u.hour + u.minute/60 + u.second/3600 + u.microsecond/3.6e9)
def dt_of(jd):
    y, m, d, h = swe.revjul(jd); base = dt.datetime(y, m, d, tzinfo=UTC); return (base + dt.timedelta(hours=h)).astimezone(TZ)
def lon(jd, body, sid=False):
    return swe.calc_ut(jd, body, EF | (swe.FLG_SIDEREAL if sid else 0))[0][0]
def elong(jd): return (lon(jd, swe.MOON) - lon(jd, swe.SUN)) % 360
def nak_l(jd): return lon(jd, swe.MOON, True)
def yoga_l(jd): return (lon(jd, swe.MOON, True) + lon(jd, swe.SUN, True)) % 360
def rise(jd0, place, which):
    lo, la, al, _ = place
    r, t = swe.rise_trans(jd0, swe.SUN, which, (lo, la, al), 1013.25, 15.0, EF)
    return t[0]
def alt(jd, place):
    lo, la, al, _ = place
    x = swe.calc_ut(jd, swe.SUN, EF)[0]
    return swe.azalt(jd, swe.ECL2HOR, (lo, la, al), 1013.25, 15.0, (x[0], x[1], x[2]))[1]  # true altitude
def tzeit(jd_sunset, place, depth=-8.5):
    a, b = jd_sunset, jd_sunset + 0.12
    for _ in range(50):
        m = (a + b) / 2
        if alt(m, place) > depth: a = m
        else: b = m
    return (a + b) / 2
def crossing(f, target, t0, step=0.1, span=3.0):
    """first time after t0 when angle f crosses target (increasing)."""
    g = lambda t: ((f(t) - target + 180) % 360) - 180
    a = t0; ga = g(a); t = t0
    while t < t0 + span:
        t += step; gt = g(t)
        if ga < 0 <= gt and gt - ga < 90:
            lo_, hi = t - step, t
            for _ in range(45):
                m = (lo_ + hi) / 2
                if g(m) < 0: lo_ = m
                else: hi = m
            return (lo_ + hi) / 2
        ga = gt
    return None

TITHI = ['Pratipadā','Dvitīyā','Tṛtīyā','Caturthī','Pañcamī','Ṣaṣṭhī','Saptamī','Aṣṭamī','Navamī','Daśamī','Ekādaśī','Dvādaśī','Trayodaśī','Caturdaśī']
def tithi_name(i):  # i 1..30
    if i == 15: return 'Śukla Pūrṇimā'
    if i == 30: return 'Kṛṣṇa Amāvāsyā'
    return ('Śukla ' if i < 15 else 'Kṛṣṇa ') + TITHI[(i - 1) % 15]
NAK = ['Aśvinī','Bharaṇī','Kṛttikā','Rohiṇī','Mṛgaśirā','Ārdrā','Punarvasu','Puṣya','Āśleṣā','Maghā','Pūrva Phalgunī','Uttara Phalgunī','Hasta','Citrā','Svātī','Viśākhā','Anurādhā','Jyeṣṭhā','Mūla','Pūrva Āṣāḍhā','Uttara Āṣāḍhā','Śravaṇa','Dhaniṣṭhā','Śatabhiṣā','Pūrva Bhādrapadā','Uttara Bhādrapadā','Revatī']
YOGA = ['Viṣkambha','Prīti','Āyuṣmān','Saubhāgya','Śobhana','Atigaṇḍa','Sukarman','Dhṛti','Śūla','Gaṇḍa','Vṛddhi','Dhruva','Vyāghāta','Harṣaṇa','Vajra','Siddhi','Vyatīpāta','Varīyān','Parigha','Śiva','Siddha','Sādhya','Śubha','Śukla','Brahman','Indra','Vaidhṛti']
MOV = ['Bava','Bālava','Kaulava','Taitila','Gara','Vaṇija','Viṣṭi']
def karana_name(k):  # k 0..59
    if k == 0: return 'Kiṃstughna'
    if k >= 57: return ['Śakuni','Catuṣpāda','Nāga'][k - 57]
    return MOV[(k - 1) % 7]
VARA = ['Somavāra','Maṅgalavāra','Budhavāra','Guruvāra','Śukravāra','Śanivāra','Ravivāra']  # python weekday 0=Mon
MASA = ['Caitra','Vaiśākha','Jyeṣṭha','Āṣāḍha','Śrāvaṇa','Bhādrapada','Āśvina','Kārttika','Mārgaśīrṣa','Pauṣa','Māgha','Phālguna']

def spans(f, unit, t0, t1, namef, count):
    """segments of an angular quantity between sunrise t0 and next sunrise t1: [(name, end_jd)]"""
    out = []; t = t0
    while True:
        k = int(f(t + 1e-6) // unit) % count
        end = crossing(f, ((k + 1) * unit) % 360, t + 1e-6, step=0.05)
        out.append((namef(k), end))
        if end is None or end >= t1: break
        t = end
    return out

start, stop = dt.date(2026, 9, 25), dt.date(2030, 1, 2)
# new moons for month naming
nms = []; t = jd_of(dt.datetime(2026, 2, 1, tzinfo=UTC))
while t < jd_of(dt.datetime(2030, 3, 1, tzinfo=UTC)):
    n = crossing(elong, 0.0, t, step=0.5, span=40); nms.append(n); t = n + 1
rasi = [int(lon(n, swe.SUN, True) // 30) for n in nms]
months = []  # (start_jd, name, adhika)
for i in range(len(nms) - 1):
    mi = (rasi[i] + 1) % 12; adh = rasi[i] == rasi[i + 1]
    months.append((nms[i], mi, adh))
def month_at(jd):
    m = [x for x in months if x[0] <= jd][-1]; return m
def chaitra_start(jd):
    c = [x for x in months if x[0] <= jd and x[1] == 0 and not x[2]][-1]; return dt_of(c[0]).year
HK = PLACES['Hickory']
rows = []; d = start
while d <= stop:
    mid = jd_of(dt.datetime(d.year, d.month, d.day, tzinfo=TZ))
    sr = rise(mid, HK, swe.CALC_RISE); ss = rise(sr, HK, swe.CALC_SET)
    sr2 = rise(sr + 0.5, HK, swe.CALC_RISE)
    ti = spans(elong, 12.0, sr, sr2, lambda k: tithi_name(k + 1), 30)
    na = spans(nak_l, 360 / 27, sr, sr2, lambda k: NAK[k], 27)
    yo = spans(yoga_l, 360 / 27, sr, sr2, lambda k: YOGA[k], 27)
    ka = spans(elong, 6.0, sr, sr2, karana_name, 60)
    tnum = int(elong(sr) // 12) + 1
    mstart, mi, adh = month_at(sr)
    am = ('Adhika ' if adh else '') + MASA[mi]
    pm = MASA[(mi + 1) % 12] if tnum > 15 and not adh else am
    yr = chaitra_start(sr)
    h = hd.GregorianDate(d.year, d.month, d.day).to_heb()
    rows.append(dict(date=d.isoformat(), vara=VARA[d.weekday()], sunrise=dt_of(sr), sunset=dt_of(ss),
                     tithi=ti, nak=na, yoga=yo, karana=ka, paksha='Śukla' if tnum <= 15 else 'Kṛṣṇa',
                     amanta=am, purnimanta=pm, vs=yr + 57, saka=yr - 78, saptarsi=yr + 3076,
                     heb=f'{h.day} {h.month_name()} {h.year}', hebnext=None))
    d += dt.timedelta(days=1)
import pickle; pickle.dump(rows, open('/tmp/cal/rows.pkl', 'wb'))
print(len(rows), rows[9]['date'], rows[9]['tithi'], rows[9]['nak'])

```

## fest.py

```python
exec(open('compute.py').read().split("start, stop =")[0])
import pickle
rows = pickle.load(open('rows.pkl', 'rb'))
NUM = {tithi_name(i): i for i in range(1, 31)}
J = lambda t: jd_of(t)
def tat(jd): return int(elong(jd) // 12) + 1
RASI = ['Meṣa','Vṛṣabha','Mithuna','Karka','Siṃha','Kanyā','Tulā','Vṛścika','Dhanus','Makara','Kumbha','Mīna']
def hm(t): return t.strftime('%I:%M %p').lstrip('0').lower()
def when(jd, day):
    t = dt_of(jd); s = hm(t)
    if t.date() != day: s += ' ' + t.strftime('%a')
    return s
N = len(rows) - 1
info = []
for i in range(N):
    r = rows[i]; sr = J(r['sunrise']); ss = J(r['sunset']); sr2 = J(rows[i + 1]['sunrise'])
    present = [NUM[n] for n, e in r['tithi']]
    mom = {'sunrise': sr, 'madhyahna': sr + (ss - sr) * 0.5, 'aparahna': sr + (ss - sr) * 0.7,
           'pradosha': ss + (sr2 - ss) * 0.1, 'nishitha': ss + (sr2 - ss) * 0.5}
    info.append(dict(i=i, day=dt.date.fromisoformat(r['date']), sr=sr, ss=ss, sr2=sr2, present=present,
                     at={k: tat(v) for k, v in mom.items()}, month=r['amanta']))
marks = {i: [] for i in range(N)}
# generic tithis: Ekadashi, Purnima, Amavasya (day the tithi prevails at sunrise; a kshaya tithi goes on the day it falls in)
GEN = {11: 'Śukla Ekādaśī', 26: 'Kṛṣṇa Ekādaśī', 15: 'Pūrṇimā', 30: 'Amāvāsyā'}
for x in info:
    i = x['i']
    for n, lab in GEN.items():
        if n not in x['present']: continue
        at_sr = x['at']['sunrise'] == n
        prev = info[i - 1]['at']['sunrise'] == n if i > 0 else False
        kshaya = not at_sr and tat(x['sr2']) != n
        if (at_sr and not prev) or kshaya:
            m = x['month'].replace('Adhika ', 'Adhika ')
            marks[i].append(f"{m} {lab}" if n in (15, 30) else lab)
# sankranti
for x in info:
    a = int(lon(x['sr'], swe.SUN, True) // 30); b = int(lon(x['sr2'], swe.SUN, True) // 30)
    if a != b:
        t = crossing(lambda j: lon(j, swe.SUN, True), b * 30.0 % 360, x['sr'], step=0.05, span=1.5)
        marks[x['i']].append(f"{RASI[b]} Saṅkrānti ({when(t, x['day'])})")
# named festivals
FEST = [('Caitra', 1, 'sunrise', 'Navreh (Kashmiri new year) · Caitra Navarātri begins'),
        ('Caitra', 9, 'madhyahna', 'Rāma Navamī'),
        ('Āṣāḍha', 15, 'sunrise', 'Guru Pūrṇimā'),
        ('Śrāvaṇa', 23, 'nishitha', 'Kṛṣṇa Janmāṣṭamī'),
        ('Bhādrapada', 4, 'madhyahna', 'Gaṇeśa Caturthī'),
        ('Āśvina', 1, 'sunrise', 'Śāradīya Navarātri begins'),
        ('Āśvina', 8, 'sunrise', 'Durgāṣṭamī'),
        ('Āśvina', 9, 'sunrise', 'Mahānavamī'),
        ('Āśvina', 10, 'aparahna', 'Vijayādaśamī'),
        ('Āśvina', 30, 'pradosha', 'Dīpāvalī (Lakṣmī Pūjā)'),
        ('Māgha', 5, 'sunrise', 'Vasanta Pañcamī'),
        ('Māgha', 28, 'nishitha', 'Herath (Kashmiri Śivarātri)'),
        ('Māgha', 29, 'nishitha', 'Mahāśivarātri'),
        ('Phālguna', 15, 'pradosha', 'Holikā Dahan')]
log = []
for month, n, rule, lab in FEST:
    def tmonth(x):  # month the tithi n belongs to on day x (a tithi that starts after a new moon belongs to the next month)
        if x['at']['sunrise'] > n and x['i'] + 1 < N: return info[x['i'] + 1]['month']
        return x['month']
    cands = [x for x in info if n in x['present'] and tmonth(x) == month]
    groups = []
    for x in cands:
        if groups and x['i'] - groups[-1][-1]['i'] <= 1: groups[-1].append(x)
        else: groups.append([x])
    for g in groups:
        hit = [x for x in g if x['at'][rule] == n]
        if len(hit) == 1: pick = hit[0]; why = rule
        elif len(hit) > 1: pick = hit[-1] if rule == 'nishitha' else hit[0]; why = rule + ' (both days)'
        else:
            s = [x for x in g if x['at']['sunrise'] == n]; pick = s[0] if s else g[0]; why = 'fallback sunrise'
        marks[pick['i']].append(lab)
        if lab == 'Holikā Dahan' and pick['i'] + 1 < N: marks[pick['i'] + 1].append('Holī')
        log.append((pick['day'].isoformat(), lab, why, [x['day'].isoformat() for x in g]))
pickle.dump({rows[i]['date']: v for i, v in marks.items() if v}, open('marks.pkl', 'wb'))
for l in sorted(log): print(l)

```

## gen.py

```python
exec(open('compute.py').read().split("start, stop =")[0])
import pickle
from pyluach import dates as hd
rows = pickle.load(open('rows.pkl', 'rb'))
MARKS = pickle.load(open('marks.pkl', 'rb'))
def hm(t): s = t.strftime('%I:%M %p').lstrip('0').lower(); return s
def until(jd, day):
    t = dt_of(jd); s = hm(t)
    if t.date() != day: s += ' ' + t.strftime('%a')
    return s
def seg(lst, day):
    parts = []
    for i, (n, e) in enumerate(lst):
        if i < len(lst) - 1: parts.append(f'{n} until {until(e, day)}')
        else: parts.append(n)
    return '; '.join(parts)
years = {}
for r in rows:
    d = dt.date.fromisoformat(r['date'])
    if d < dt.date(2026, 10, 1) or d > dt.date(2029, 12, 31): continue
    masa = r['amanta'] if r['amanta'] == r['purnimanta'] else f"{r['amanta']} (amānta) · {r['purnimanta']} (pūrṇimānta)"
    line = f"| {r['date']} | {r['vara']} | {hm(r['sunrise'])} | {hm(r['sunset'])} | {seg(r['tithi'], d)} | {seg(r['nak'], d)} | {seg(r['yoga'], d)} | {seg(r['karana'], d)} | {masa} | VS {r['vs']} · Śaka {r['saka']} · Saptarṣi {r['saptarsi']} | {'; '.join(MARKS.get(r['date'], []))} |"
    years.setdefault(d.year, []).append(line)
head = '''---
type: data
place: "Hickory, NC (35.733 N, 81.341 W)"
cssclasses:
  - wide
---
# Panchang {Y} (Hickory)

One row per day, for the day that begins at sunrise in Hickory, North Carolina. Times are local (Eastern, with daylight saving). Each limb gives what is current at sunrise and when it ends; "then" items follow within the same day. Home reads today's row.

How it was computed (4 Oct 2026): Swiss Ephemeris (Moshier), sidereal positions with the Lahiri ayanāṃśa, sunrise and sunset at the upper limb with standard refraction. Tithi from the Moon–Sun elongation (12° steps), karaṇa in 6° steps, nakṣatra from the Moon's sidereal longitude, yoga from the sum of the sidereal longitudes (13°20′ steps). Months are amānta, named for the Sun's sidereal sign at the new moon that begins them (a month with no saṅkrānti is Adhika); in the dark fortnight the pūrṇimānta name is given too. Vikrama, Śaka and the Kashmiri Saptarṣi (Laukika) years turn at Caitra Śukla Pratipadā. Checked against a published Delhi panchang for 4 Oct 2026: tithi, nakṣatra, yoga and karaṇa ends agree to the minute.

Festival column (added 4 Oct 2026): Ekādaśī, Pūrṇimā and Amāvāsyā go on the day the tithi is current at sunrise; a tithi that begins and ends between two sunrises goes on the day it falls in. Saṅkrānti is the moment the Sun enters a sidereal sign. Named festivals follow the usual time of day for each: sunrise (Navreh and Caitra Navarātri, Guru Pūrṇimā, Śāradīya Navarātri, Durgāṣṭamī, Mahānavamī, Vasanta Pañcamī), midday (Rāma Navamī, Gaṇeśa Caturthī), afternoon (Vijayādaśamī), early evening (Dīpāvalī, Holikā Dahan) and midnight (Janmāṣṭamī, Herath, Mahāśivarātri; if the tithi covers midnight on two nights, the second). The dates are for Hickory, so some fall a day earlier than in calendars made for India. Vaiṣṇava Ekādaśī rules and local custom can differ. Checked against Drik Panchang's New York dates for autumn 2026: Navarātri, Durgāṣṭamī, Mahānavamī, Vijayādaśamī, Dīpāvalī and the Ekādaśīs of 6 Oct, 21 Oct and 4 Nov agree; Drik lists Mokṣadā Ekādaśī on 19 Dec, a day before this table.

| Date | Vāra | Sunrise | Sunset | Tithi | Nakṣatra | Yoga | Karaṇa | Māsa | Saṃvat | Festival |
|---|---|---|---|---|---|---|---|---|---|---|
'''
for y, ls in years.items():
    open(f'out/Panchang {y} (Hickory).md', 'w', encoding='utf-8').write(head.replace('{Y}', str(y)) + '\n'.join(ls) + '\n')
    print(y, len(ls))
# ---- Shabbat and Yom Tov
NAMES = {'Rosh Hashana': 'Rosh Hashanah', 'Yom Kippur': 'Yom Kippur', 'Succos': 'Sukkot', 'Shmini Atzeres': 'Shemini Atzeret', 'Simchas Torah': 'Simchat Torah', 'Pesach': 'Pesach', 'Shavuos': 'Shavuot'}
rest = []
d = dt.date(2026, 9, 25)
while d <= dt.date(2029, 12, 31):
    h = hd.GregorianDate(d.year, d.month, d.day).to_heb()
    f = h.festival(israel=False, include_working_days=False)
    labs = []
    if f: labs.append(NAMES.get(f, f))
    if d.weekday() == 5: labs.append('Shabbat')
    if labs: rest.append((d, labs))
    d += dt.timedelta(days=1)
blocks = []
for d, labs in rest:
    if blocks and (d - blocks[-1][1]).days == 1: blocks[-1][1] = d; blocks[-1][2] += labs
    else: blocks.append([d, d, labs])
def sunset(day, place):
    mid = jd_of(dt.datetime(day.year, day.month, day.day, tzinfo=TZ)); sr = rise(mid, place, swe.CALC_RISE); return rise(sr, place, swe.CALC_SET)
def floor_min(t): return t.replace(second=0, microsecond=0)
def round_min(t): return (t + dt.timedelta(seconds=30)).replace(second=0, microsecond=0)
lines = []
for a, b, labs in blocks:
    eve = a - dt.timedelta(days=1)
    seen = []; [seen.append(x) for x in labs if x not in seen]
    occ = ', '.join(seen)
    c = {}; e = {}
    for nm, pl in PLACES.items():
        c[nm] = floor_min(dt_of(sunset(eve, pl) - pl[3] / 1440)); e[nm] = round_min(dt_of(tzeit(sunset(b, pl), pl)))
    if a < dt.date(2026, 10, 1) and b < dt.date(2026, 10, 1): continue
    lines.append(f"| {a.isoformat()} | {b.isoformat()} | {occ} | {c['Hickory'].strftime('%Y-%m-%d %H:%M')} | {e['Hickory'].strftime('%Y-%m-%d %H:%M')} | {c['New York'].strftime('%Y-%m-%d %H:%M')} | {e['New York'].strftime('%Y-%m-%d %H:%M')} |")
sh = '''---
type: data
places:
  - "Hickory, NC"
  - "New York, NY"
cssclasses:
  - wide
---
# Shabbat and Yom Tov times 2026-2029

Every Shabbat and every diaspora Yom Tov (Rosh Hashanah, Yom Kippur, the first two and last two days of Sukkot and Pesach, Shemini Atzeret, Simchat Torah, Shavuot), joined into one row when they run together. Home reads this table to show when Shabbat or Yom Tov begins and ends for you and for your study partner in New York.

Hebcal's default convention: candle lighting 18 minutes before sunset on the eve; the end (havdalah) when the sun is 8.5° below the horizon after sunset on the last day. Sunset is the upper limb at the horizon with standard refraction. Times are Eastern local time, 24-hour, as Home expects. Computed 4 Oct 2026 with Swiss Ephemeris and the pyluach Hebrew calendar; candle-lighting times checked against Hebcal-derived New York times for Oct 2026 to Jan 2027 (all agree to the minute). Check with your community for local custom.

| From | To | Occasion | Hickory begins | Hickory ends | New York begins | New York ends |
|---|---|---|---|---|---|---|
'''
open('out/Shabbat and Yom Tov times 2026-2029.md', 'w', encoding='utf-8').write(sh + '\n'.join(lines) + '\n')
print('blocks', len(lines)); print('\n'.join(lines[:4]))

```

## dafyomi.py

Added 21 Oct 2026 (orientation chat, T25). Writes `Calendar/Daf Yomi <first>-<last>.md`, the page of the Babylonian Talmud read each day in the Daf Yomi cycle, read by `today-header` (Home's date line and the Calendar note's box). Pure arithmetic, no data files: the 2,711 dapim in the cycle's order from the cycle's first day (cycle 14 from 5 Jan 2020, cycle 15 from 8 Jun 2027). Run `python3 dafyomi.py 2030-01-01 2032-12-31 > "Daf Yomi 2030-2032.md"` for a new range, check three dates against Sefaria's calendar (`https://www.sefaria.org/api/calendars?year=…&month=…&day=…`, the *Daf Yomi* item), put the file in `Calendar/` and point `const DAF` in `today-header/view.js` at it. The checks made on 21 Oct 2026 are listed at the top of the table.

```python
# dafyomi.py — writes Calendar/Daf Yomi <first>-<last>.md: one row per day with the day's daf (Babylonian Talmud, the Daf Yomi order),
# a Sefaria link and the name the vault's Talmud note will have. 21 Oct 2026. Usage: python3 dafyomi.py 2026-10-01 2029-12-31 > "Daf Yomi 2026-2029.md"
import sys, datetime as dt

# The 37 tractate stretches of the cycle in order, with the last daf of each; every tractate starts at daf 2, except that
# Kinnim (23-25), Tamid (26-33) and Middot (34-37) continue Meilah's page numbers, as the printed Vilna volume does. 2,711 dapim.
TRACTATES = [("Berakhot", 64), ("Shabbat", 157), ("Eruvin", 105), ("Pesachim", 121), ("Shekalim", 22), ("Yoma", 88), ("Sukkah", 56),
    ("Beitzah", 40), ("Rosh Hashanah", 35), ("Taanit", 31), ("Megillah", 32), ("Moed Katan", 29), ("Chagigah", 27), ("Yevamot", 122),
    ("Ketubot", 112), ("Nedarim", 91), ("Nazir", 66), ("Sotah", 49), ("Gittin", 90), ("Kiddushin", 82), ("Bava Kamma", 119),
    ("Bava Metzia", 119), ("Bava Batra", 176), ("Sanhedrin", 113), ("Makkot", 24), ("Shevuot", 49), ("Avodah Zarah", 76), ("Horayot", 14),
    ("Zevachim", 120), ("Menachot", 110), ("Chullin", 142), ("Bekhorot", 61), ("Arakhin", 34), ("Temurah", 34), ("Keritot", 28),
    ("Meilah", 22), ("Kinnim", 25), ("Tamid", 33), ("Middot", 37), ("Niddah", 73)]
FIRST = {"Kinnim": 23, "Tamid": 26, "Middot": 34}
SEQ = [(n, d) for n, last in TRACTATES for d in range(FIRST.get(n, 2), last + 1)]
assert len(SEQ) == 2711, len(SEQ)
CYCLE_14 = dt.date(2020, 1, 5)   # Berakhot 2 (Sefaria's calendar for that date)
CYCLE_15 = dt.date(2027, 6, 8)   # the day after Niddah 73 (7 Jun 2027 on Sefaria's calendar); My Jewish Learning: cycle 15 runs 8 Jun 2027 - 8 Nov 2034

def daf_for(d):
    start, cyc = (CYCLE_15, 15) if d >= CYCLE_15 else (CYCLE_14, 14)
    return SEQ[(d - start).days % len(SEQ)], cyc

def sefaria(name, daf):
    if name == "Shekalim": return "https://www.sefaria.org/Jerusalem_Talmud_Shekalim"   # the cycle reads the Yerushalmi Shekalim; Sefaria files it by chapter
    if name in ("Kinnim", "Middot"): return f"https://www.sefaria.org/Mishnah_{name}"      # Mishnah only; Sefaria files them by chapter
    return f"https://www.sefaria.org/{name.replace(' ', '_')}.{daf}"

a, b = (dt.date.fromisoformat(sys.argv[1]), dt.date.fromisoformat(sys.argv[2])) if len(sys.argv) > 2 else (dt.date(2026, 10, 1), dt.date(2029, 12, 31))
rows = []
d = a
while d <= b:
    (name, daf), cyc = daf_for(d)
    rows.append(f"| {d.isoformat()} | {name} {daf} | [Sefaria]({sefaria(name, daf)}) | {name} {daf} | {cyc} |")
    d += dt.timedelta(1)
head = f"""---
type: data
cssclasses:
  - wide
---
# Daf Yomi {a.year}-{b.year}

The page of the Babylonian Talmud read each day in the Daf Yomi cycle, from {a.strftime('%-d %b %Y')} to {b.strftime('%-d %b %Y')}. Home's date line and the Calendar note's box show the day's daf; the row's last-but-one column is the name the vault's Talmud note will have (one note per daf, *Tractate daf*), which the date box links as soon as a note of that name exists, and until then the Sefaria link stands in.

Computed 21 Oct 2026 with `dafyomi.py` (in [[Calendar scripts]]): the 2,711 dapim of the cycle in the Daf Yomi order (each tractate from daf 2 to its last; Shekalim is the Yerushalmi's 22 dapim; Kinnim 23–25, Tamid 26–33 and Middot 34–37 continue Meilah's numbering, as in the printed volume), one a day from the cycle's first day. Cycle 14 began on 5 January 2020 and ends on 7 June 2027; cycle 15 begins on 8 June 2027 and ends on 8 November 2034 (the same arithmetic). Checked against Sefaria's calendar (`https://www.sefaria.org/api/calendars?year=…&month=…&day=…`) on 21 Oct 2026 for 5 Jan 2020 (Berakhot 2), 23 Mar 2021 (Shekalim 2), 21 Oct 2026 (Bekhorot 33), 19 Nov 2026 (Arakhin 2), 22 Dec 2026 (Temurah 2), 24 Jan 2027 (Keritot 2), 20 Feb 2027 (Meilah 2), 13 Mar 2027 (Kinnim), 16 Mar 2027 (Tamid 26), 24 Mar 2027 (Middot), 28 Mar 2027 (Niddah 2) and 7 Jun 2027 (Niddah 73), all as the table has them; Sefaria's calendar carries no Daf Yomi after cycle 14, so cycle 15 rests on the arithmetic and on the published dates ([My Jewish Learning, *Daf Yomi Calendar*](https://www.myjewishlearning.com/article/daf-yomi-calendar/): cycle 15, 8 June 2027 to 8 November 2034). A missed day does not move the cycle.

| Date | Daf | Sefaria | Note | Cycle |
|---|---|---|---|---|
"""
sys.stdout.write(head + "\n".join(rows) + "\n")
```
