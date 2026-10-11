import os, base64, sqlite3, random, datetime as dt
import pandas as pd
import streamlit as st
from pathlib import Path

LOGO = Path(__file__).parent / "assets" / "logo.png"

# Oromia Bank logo embedded so it always shows, even if the image file was not uploaded to GitHub
LOGO_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAssAAAGtCAMAAADXk8kzAAABjFBMVEX///+UyT1ZYqpfaa6kzjmhzTuezDuUyT+cyzyv0TZia6+n"
    "zziZyj2TyD+pzzit0TZocbNUXaJZZKu00zRqc7SSyDhRW6dRWp1NVZVPWaaMxSbn6PJKVKSPxzDy+er9/vru9uHMzuPx8vj5/PPg"
    "78nv8Pfa3Oymqs/6+v3W2OnR5rTCxd7w8ffo89eyttbF4ZqcocuczUuMksNET6J0e7fM5aep02qEir+i0Fu5vNq424KAhr2jp87l"
    "8MDh78yu1nG/3pKrzx7C3X+61yvP5JPT6LLM5aWHwxG/2mXr88nK32qx0RSaySNqd5pfZ6NDSZRUXLFmcZ9ug4k5Rp7U5Zu11ly7"
    "2FbK4Hri7rGarnq/3XyhtWm92E+92EN7iZqiuWGuxmCJmZN7hqKUpouguHpreIynw2J9jodXX5qlx0x/kn6OpHyAj5aBjanb399f"
    "bZWVu0+Gp3GSpJRtg3+KrWtdbodZZZGgsa+Snqlgfn+3wMeJt1RylXyHsmBreaeqwmOrup3E17bP3M2ry4QSnT92AAAgAElEQVR4"
    "nO2diX8aR7bvWWxJJpKNEN1K0+w7wiDACLFIgC2hsRPZsjPyEm+Z7F5yb5yMJ++960nm3fv+8Vdbd1dVdyNAyPLE5/uZcSQEvfGr"
    "U6dOnTrl8QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHyAJDImicR5XwwATE8ik9w93n/88ObNm/dNbrYGj28c71aQ"
    "rM/7+gBgEpK7Bw8frF2/fv0K4fLly58QLhAOEfXHmxuV875MABgHssYPnyEZX7p06Yqjki8SFi5euLCw1NqqxM/7ggHAicSt/Ztr"
    "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"
    "fKydDOWeXTisIFGzqxSCZyTXQArsnVy2Uxz1OybJZVzWQQk2UZ4elkar/O1I7s6m4BZYHj6/TgsNSQUD7JwkRxfuSj58+2wNs2SW"
    "kZCb29UJBnhFvVPrhf0+q17ihOmfrlpe//ToTqNj+TOZ5Ea3vaiQVDley5P7WaJm3qEuI8BXMY23vO1uP+7J10KrP2LRmO7hwEVs"
    "BGnkxr7KkZf/CFnpKi5DVazrFvsLK2/JnokkJsl5M1KsxOoUXIeEGHE2kb8daSUYaizcII/LE+HSKpRFBwNMH4FtpkTQ/K6tOkJy"
    "4m9yIop+Xsf+0Ha1NIFbgaswqz6x7KegZd8sWsYrso+O/qjyeqtsdL0RoQTzFMEcsQhF/Tb2f6rcsXHNZ73Tu3b3+3e4CzBTBMal"
    "v3tsq1pJsQixahAtMmHP36RIxtYtSQ5r7kDuIKT8PfOzwlS3vEJXeA680KUSGCSKwb/iFLyeJklO0Hzc9mDnnF2k+y3PoreTmmCQ"
    "p6dqQT9SsTydLdvl0AxaRmImhRIbKZ07Y2VzsBIz5TzFjJGUj/H2Lp6m9Bdor1NM63l0K2r07vdviRCtQIMUS0tKhxXtLTJU8gJk"
    "9iV1XcyhmBmquCXJYZ/EliQnqkFZYdHfxJazvCjOleQSyS1pNST2l3gtW9E2fn3UlugGWwFLe5Ic/75l/BYpv/bU+4IJUC3j6svV"
    "ScZ56XKj6QudaonJeLts5HO16MQAAB9zSURBVHreaZSvWqdNxDcGrALz4hRalupfxX4kA1PVF+5tN7Z7zaBPUzXf7bd0UoxLlxAj"
    "El5bQpdUS1HO72VleFyt+8jFG5eqy2Djau8BxPoHSqzd3TzYHLYW+RelZWTilI1ysIU4wJvRyds7ZKV7V4z9nfiRBxqSCgZ4aJzG"
    "niQnTEWSQHxGzOabb1ZGMYAMbLNW1k9+K57j8HOVEk+n5VUtek3z+X3atahm1zKW86eNDb7dZrJDZJ1XvI5lAVyQC1/8865qpUCh"
    "f+6G/v47+0L5zB+3WkMG4xdpGIEJabLNLUluaL4uLfuXZ0roKmb7euqYvOJPHlTJK8VYeUa5NAt1jKTM6q1+Mp7MbnJNpZ50SZLj"
    "l3cpddxCH9t9eNHtcyxXMjvp0mSzIMU8ci38UmaGu7scGi9lZA6//vIl2ZLn5Xe/fnFP1WxapgVfHgslEbPDdmQaJ0sWnfLupzt3"
    "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"
)

def show_logo():
    """Logo: use a file next to app.py if present, otherwise the logo embedded in this file."""
    for p in (LOGO, Path(__file__).parent / "logo.png", Path(__file__).parent / "Oromia_bank.png"):
        if p.exists():
            st.image(str(p)); return
    try:
        st.image(base64.b64decode(LOGO_B64))
    except Exception:
        st.markdown("## 🏦 Oromia Bank")

GREEN, BLUE = "#8DC63F", "#5557A8"
DB = str(Path(__file__).parent / "pension.db")
st.set_page_config(page_title="Oromia Bank Pension System", page_icon="🏦", layout="wide")

# ---------------- Translations ----------------
T = {
 "English": {"home": "My Summary", "pay": "My Payments", "pol": "Proof of Life", "loc": "Branch & Agent Locator",
             "sup": "Support", "prof": "My Profile", "hello": "Welcome", "next": "Next payment"},
 "Afaan Oromo": {"home": "Cuunfaa Koo", "pay": "Kaffaltii Koo", "pol": "Mirkaneessa Jiraachuu", "loc": "Damee fi Ejensii Barbaadi",
             "sup": "Deeggarsa", "prof": "Piroofaayilii Koo", "hello": "Baga nagaan dhufte", "next": "Kaffaltii itti aanu"},
 "አማርኛ": {"home": "ማጠቃለያ", "pay": "ክፍያዎቼ", "pol": "ሕይወት ማረጋገጫ", "loc": "ቅርንጫፍና ወኪል ፈልግ",
             "sup": "ድጋፍ", "prof": "መገለጫዬ", "hello": "እንኳን ደህና መጡ", "next": "ቀጣይ ክፍያ"},
}
STAFF = {"officer": ("Branch Officer", "1234"), "maker": ("Payroll Officer (Maker)", "1234"),
         "checker": ("Payroll Approver (Checker)", "1234"), "fraud": ("Fraud Analyst", "1234"),
         "admin": ("System Admin", "1234")}
BRANCHES = ["Finfinne Main", "Adama", "Jimma", "Bishoftu", "Nekemte", "Shashamane", "Ambo", "Asella"]

# ---------------- Database (Supabase PostgreSQL, SQLite fallback) ----------------
def _db_url():
    try:
        if "DATABASE_URL" in st.secrets:
            return str(st.secrets["DATABASE_URL"])
    except Exception:
        pass
    return os.environ.get("DATABASE_URL", "")

DB_URL = _db_url()
USE_PG = DB_URL.startswith("postgres")
if USE_PG:
    import psycopg2

@st.cache_resource
def _pg():
    c = psycopg2.connect(DB_URL, connect_timeout=15)
    c.autocommit = True
    return c

def _clean(p):
    return tuple(x.item() if hasattr(x, "item") else x for x in p)

def _exec(sql, p=(), fetch=False, many=False):
    if USE_PG:
        sql = sql.replace("?", "%s")
        for attempt in (1, 2):
            try:
                cur = _pg().cursor()
                if many:
                    cur.executemany(sql, [_clean(r) for r in p])
                else:
                    cur.execute(sql, _clean(p) or None)
                if fetch:
                    return pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description])
                return None
            except (psycopg2.OperationalError, psycopg2.InterfaceError):
                _pg.clear()            # connection dropped: reconnect once
                if attempt == 2:
                    raise
    c = sqlite3.connect(DB, check_same_thread=False)
    try:
        cur = c.cursor()
        if many:
            cur.executemany(sql, [_clean(r) for r in p])
        else:
            cur.execute(sql, _clean(p))
        c.commit()
        if fetch:
            return pd.DataFrame(cur.fetchall(), columns=[d[0] for d in cur.description])
    finally:
        c.close()

def q(sql, p=()):
    return _exec(sql, p, fetch=True)

def run(sql, p=()):
    _exec(sql, p)

def run_many(sql, rows):
    _exec(sql, rows, many=True)

@st.cache_resource
def init_db():
    pk = "SERIAL PRIMARY KEY" if USE_PG else "INTEGER PRIMARY KEY AUTOINCREMENT"
    num = "DOUBLE PRECISION" if USE_PG else "REAL"
    for ddl in (
        f"CREATE TABLE IF NOT EXISTS pensioners(id TEXT PRIMARY KEY,name TEXT,nid TEXT,phone TEXT,gender TEXT,dob TEXT,"
        f"branch TEXT,amount {num},status TEXT,channel TEXT,account TEXT,last_pol TEXT,lang TEXT)",
        f"CREATE TABLE IF NOT EXISTS batches(id {pk},month TEXT,eligible INT,excluded INT,"
        f"total {num},status TEXT,maker TEXT,checker TEXT,created TEXT)",
        f"CREATE TABLE IF NOT EXISTS payments(id {pk},batch INT,pid TEXT,amount {num},status TEXT,date TEXT)",
        f"CREATE TABLE IF NOT EXISTS tickets(id {pk},pid TEXT,type TEXT,msg TEXT,status TEXT,created TEXT)",
        f'CREATE TABLE IF NOT EXISTS audit(id {pk},ts TEXT,"user" TEXT,action TEXT)',
    ):
        run(ddl)
    if int(q("SELECT COUNT(*) AS n FROM pensioners").iloc[0, 0]) == 0:
        random.seed(7)
        first = ["Abebe", "Chaltu", "Dida", "Gemechu", "Hawi", "Jaalala", "Kadir", "Lensa", "Mulu", "Nuuraa", "Obsaa", "Tolasa", "Ukkee", "Bekele", "Tigist"]
        last = ["Tadesse", "Bulti", "Gudina", "Kebede", "Lemma", "Fufa", "Wakjira", "Dinsa", "Negasa", "Hirpa"]
        today = dt.date.today()
        rows = []
        for i in range(1, 61):
            st_ = random.choices(["Active", "Suspended", "Deceased"], [80, 12, 8])[0]
            pol = today - dt.timedelta(days=random.randint(10, 500))
            rows.append((f"P{i:04d}", f"{random.choice(first)} {random.choice(last)}", f"ID{random.randint(10**9, 10**10-1)}",
                         f"09{random.randint(10000000, 99999999)}", random.choice(["M", "F"]), str(dt.date(random.randint(1938, 1964), random.randint(1, 12), random.randint(1, 28))),
                         random.choice(BRANCHES), random.randint(1500, 9500), st_, random.choice(["Bank Account", "Agent Cash-out", "Wallet"]),
                         f"1000{random.randint(10**8, 10**9-1)}", str(pol), random.choice(["Afaan Oromo", "አማርኛ", "English"])))
        run_many("INSERT INTO pensioners VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
        run("UPDATE pensioners SET phone=(SELECT phone FROM pensioners WHERE id='P0001') WHERE id='P0002'")  # seeded fraud example

def db_badge():
    """Show which database the app is really using (so a silent SQLite fallback is obvious)."""
    if USE_PG:
        st.caption("🟢 Database: Supabase (PostgreSQL) - data is saved permanently")
    else:
        st.caption("🟠 Database: local SQLite (temporary) - DATABASE_URL secret NOT found, nothing is saved to Supabase")

def log(action):
    run('INSERT INTO audit(ts,"user",action) VALUES(?,?,?)', (dt.datetime.now().strftime("%Y-%m-%d %H:%M"), st.session_state.get("user", "-"), action))

def pol_due(d):
    return (dt.date.today() - dt.date.fromisoformat(d)).days > 365

# ---------------- Styling ----------------
def style(large=False):
    fs = "1.35rem" if large else "1rem"
    st.markdown(f"""<style>
    html, body, [class*="css"] {{ font-size:{fs}; }}
    .hdr {{background:linear-gradient(90deg,{GREEN},{BLUE});padding:14px 20px;border-radius:12px;color:white;margin-bottom:14px}}
    .hdr h2 {{margin:0;color:white}}
    .card {{background:#F1F7E6;border-left:6px solid {GREEN};padding:14px;border-radius:10px;margin-bottom:10px}}
    div.stButton>button {{background:{BLUE};color:white;border-radius:8px;border:0}}
    div.stButton>button:hover {{background:{GREEN};color:#222}}
    </style>""", unsafe_allow_html=True)

def header(title, sub=""):
    st.markdown(f'<div class="hdr"><h2>{title}</h2><span>{sub}</span></div>', unsafe_allow_html=True)

# ---------------- Login ----------------
def login():
    style()
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        show_logo()
        st.markdown("### Pension Payment System · Sirna Kaffaltii Fayyadaa")
        role = st.radio("Sign in as", ["Pensioner", "Bank Staff"], horizontal=True)
        if role == "Pensioner":
            pid = st.text_input("Pension ID (e.g. P0001)")
            pin = st.text_input("PIN (demo: 1234)", type="password")
            if st.button("Sign in", use_container_width=True):
                r = q("SELECT * FROM pensioners WHERE id=?", (pid.strip().upper(),))
                if len(r) and pin == "1234":
                    st.session_state.update(role="pensioner", user=r.iloc[0]["id"]); st.rerun()
                else:
                    st.error("Invalid ID or PIN")
        else:
            u = st.selectbox("Staff user", list(STAFF))
            pin = st.text_input("Password (demo: 1234)", type="password")
            if st.button("Sign in", use_container_width=True):
                if pin == STAFF[u][1]:
                    st.session_state.update(role="staff", user=u); log("Login"); st.rerun()
                else:
                    st.error("Wrong password")
        st.caption("Demo system with sample data only. Try pensioner P0001 / 1234.")
        db_badge()
        st.caption("🗄️ Database: " + ("Supabase PostgreSQL" if USE_PG else "SQLite (local demo, resets on restart)"))

# ---------------- Pensioner portal ----------------
def pensioner_portal():
    p = q("SELECT * FROM pensioners WHERE id=?", (st.session_state.user,)).iloc[0]
    with st.sidebar:
        show_logo()
        lang = st.selectbox("Language / Afaan / ቋንቋ", list(T), index=list(T).index(p["lang"]))
        large = st.toggle("Large text", value=True)
        t = T[lang]
        page = st.radio("Menu", [t[k] for k in ["home", "pay", "pol", "loc", "sup", "prof"]])
        if st.button("Sign out"): st.session_state.clear(); st.rerun()
    style(large)
    header(f"{t['hello']}, {p['name']}", f"Pension ID {p['id']} · {p['branch']} branch")
    if page == t["home"]:
        c1, c2, c3 = st.columns(3)
        c1.metric("Monthly pension (ETB)", f"{p['amount']:,.0f}")
        c2.metric("Status", p["status"])
        c3.metric(t["next"], (dt.date.today().replace(day=28)).strftime("%d %b %Y"))
        if pol_due(p["last_pol"]):
            st.warning("⚠️ Your proof of life is overdue. Visit a branch or agent to avoid suspension.")
        else:
            st.success("✅ Proof of life is up to date.")
        st.info("Never share your PIN. Bank staff and agents never ask for fees to process pensions.")
    elif page == t["pay"]:
        df = q("SELECT date,amount,status,batch FROM payments WHERE pid=? ORDER BY id DESC", (p["id"],))
        if df.empty: st.info("No payments yet. Payments appear after the monthly payroll is approved.")
        else:
            st.dataframe(df, use_container_width=True)
            st.download_button("Download statement (CSV)", df.to_csv(index=False), "statement.csv")
        if st.button("Report wrong or missing payment"):
            run("INSERT INTO tickets(pid,type,msg,status,created) VALUES(?,?,?,?,?)", (p["id"], "Missing payment", "Reported from payments page", "Open", str(dt.date.today())))
            st.success("Ticket opened. You will receive an SMS update.")
    elif page == t["pol"]:
        st.markdown(f'<div class="card">Last verified: <b>{p["last_pol"]}</b><br>Due before: <b>{dt.date.fromisoformat(p["last_pol"]) + dt.timedelta(days=365)}</b></div>', unsafe_allow_html=True)
        m = st.radio("Verification method", ["Branch / agent (fingerprint)", "Selfie with liveness check", "Home visit (bedridden)", "Trusted witness"])
        if m.startswith("Selfie"):
            img = st.camera_input("Take a clear selfie")
            if img and st.button("Submit selfie"):
                run("UPDATE pensioners SET last_pol=? WHERE id=?", (str(dt.date.today()), p["id"])); st.success("Proof of life recorded. Thank you!"); st.rerun()
        elif st.button("Request this method"):
            run("INSERT INTO tickets(pid,type,msg,status,created) VALUES(?,?,?,?,?)", (p["id"], "PoL request", m, "Open", str(dt.date.today())))
            st.success("Request sent. A bank officer will contact you.")
    elif page == t["loc"]:
        town = st.selectbox("Town", BRANCHES)
        st.markdown(f'<div class="card"><b>Oromia Bank – {town} Branch</b><br>Mon–Fri 8:30–17:00 · Services: PoL, cash-out, onboarding</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><b>Agent – {town} Kebele 02</b><br>Cash available · Services: cash-out, PoL</div>', unsafe_allow_html=True)
    elif page == t["sup"]:
        with st.form("tk"):
            typ = st.selectbox("Issue", ["Missing payment", "Wrong amount", "PoL issue", "Profile change", "Survivor claim", "Fraud report"])
            msg = st.text_area("Describe the problem")
            if st.form_submit_button("Submit"):
                run("INSERT INTO tickets(pid,type,msg,status,created) VALUES(?,?,?,?,?)", (p["id"], typ, msg, "Open", str(dt.date.today()))); st.success("Ticket created")
        st.dataframe(q("SELECT id,type,status,created FROM tickets WHERE pid=?", (p["id"],)), use_container_width=True)
    else:
        st.write({"Name": p["name"], "National ID": p["nid"], "Phone": p["phone"], "Payout channel": p["channel"], "Account": p["account"]})
        ch = st.selectbox("Request payout channel change", ["Bank Account", "Agent Cash-out", "Wallet"])
        if st.button("Submit for approval"):
            run("INSERT INTO tickets(pid,type,msg,status,created) VALUES(?,?,?,?,?)", (p["id"], "Profile change", f"Channel -> {ch}", "Pending approval", str(dt.date.today()))); st.success("Sent for maker-checker approval")

# ---------------- Staff console ----------------
def staff_console():
    u = st.session_state.user; role = STAFF[u][0]
    with st.sidebar:
        show_logo(); st.caption(f"👤 {role}")
        page = st.radio("Menu", ["Dashboard", "Pensioner Admin", "Payroll", "Proof of Life", "Fraud & Risk", "Support Console", "Reports", "Audit Log"])
        if st.button("Sign out"): st.session_state.clear(); st.rerun()
    style(); header(page, role)
    P = q("SELECT * FROM pensioners ORDER BY id")
    if page == "Dashboard":
        P["due"] = P["last_pol"].apply(pol_due)
        c = st.columns(4)
        c[0].metric("Pensioners", len(P)); c[1].metric("Active", int((P.status == "Active").sum()))
        c[2].metric("PoL overdue", int(P.due.sum())); c[3].metric("Monthly liability (ETB)", f"{P[P.status=='Active'].amount.sum():,.0f}")
        a, b = st.columns(2)
        a.subheader("By branch"); a.bar_chart(P.groupby("branch").size())
        b.subheader("By status"); b.bar_chart(P.groupby("status").size())
    elif page == "Pensioner Admin":
        s = st.text_input("Search name / ID / phone / national ID")
        d = P[P.apply(lambda r: s.lower() in " ".join(map(str, r.values)).lower(), axis=1)] if s else P
        st.dataframe(d, use_container_width=True, height=300)
        with st.expander("➕ Register new pensioner"):
            with st.form("reg"):
                n = st.text_input("Full name"); nid = st.text_input("National ID"); ph = st.text_input("Phone")
                g = st.selectbox("Gender", ["M", "F"]); dob = st.date_input("Date of birth", dt.date(1955, 1, 1), min_value=dt.date(1920, 1, 1))
                br = st.selectbox("Branch", BRANCHES); am = st.number_input("Monthly pension (ETB)", 500, 50000, 3000)
                ch = st.selectbox("Channel", ["Bank Account", "Agent Cash-out", "Wallet"]); lg = st.selectbox("Language", list(T))
                if st.form_submit_button("Register"):
                    if (P.nid == nid).any() or (P.phone == ph).any(): st.error("Duplicate National ID or phone detected")
                    elif not n or not nid: st.error("Name and National ID required")
                    else:
                        pid = f"P{len(P)+1:04d}"
                        run("INSERT INTO pensioners VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (pid, n, nid, ph, g, str(dob), br, am, "Active", ch, f"1000{random.randint(10**8,10**9-1)}", str(dt.date.today()), lg))
                        log(f"Registered {pid}"); st.success(f"Registered {pid}"); st.rerun()
        c1, c2, c3 = st.columns(3)
        pid = c1.selectbox("Change status of", P.id); ns = c2.selectbox("New status", ["Active", "Suspended", "Deceased", "Closed"])
        if c3.button("Apply"): run("UPDATE pensioners SET status=? WHERE id=?", (ns, pid)); log(f"{pid} -> {ns}"); st.rerun()
    elif page == "Payroll":
        st.caption("Maker prepares the batch; a different user (checker) approves. No one can approve their own batch.")
        month = st.text_input("Payroll month", dt.date.today().strftime("%B %Y"))
        if u == "maker" and st.button("Prepare payroll batch"):
            el = P[(P.status == "Active") & (~P.last_pol.apply(pol_due))]
            run("INSERT INTO batches(month,eligible,excluded,total,status,maker,created) VALUES(?,?,?,?,?,?,?)", (month, len(el), len(P) - len(el), float(el.amount.sum()), "Pending approval", u, str(dt.date.today())))
            log(f"Prepared batch {month}"); st.rerun()
        elif u != "maker": st.info("Log in as 'maker' to prepare batches and 'checker' to approve.")
        B = q("SELECT * FROM batches ORDER BY id DESC"); st.dataframe(B, use_container_width=True)
        pend = B[B.status == "Pending approval"]
        if u == "checker" and len(pend):
            bid = st.selectbox("Batch to review", pend.id)
            if st.button("✅ Approve & credit"):
                el = P[(P.status == "Active") & (~P.last_pol.apply(pol_due))]
                for _, r in el.iterrows():
                    run("INSERT INTO payments(batch,pid,amount,status,date) VALUES(?,?,?,?,?)", (int(bid), r.id, r.amount, random.choices(["Credited", "Failed"], [96, 4])[0], str(dt.date.today())))
                run("UPDATE batches SET status='Approved',checker=? WHERE id=?", (u, int(bid))); log(f"Approved batch {bid}"); st.success("Batch approved and payments credited"); st.rerun()
        st.subheader("Exclusions preview")
        ex = P[(P.status != "Active") | (P.last_pol.apply(pol_due))].copy()
        ex["reason"] = ex.apply(lambda r: r.status if r.status != "Active" else "PoL overdue", axis=1)
        st.dataframe(ex[["id", "name", "branch", "reason"]], use_container_width=True)
    elif page == "Proof of Life":
        P["due"] = P.last_pol.apply(pol_due); od = P[(P.due) & (P.status == "Active")]
        st.metric("Overdue (active)", len(od)); st.dataframe(od[["id", "name", "phone", "branch", "last_pol"]], use_container_width=True)
        pid = st.selectbox("Record PoL for", P.id); m = st.selectbox("Method", ["Fingerprint", "Face", "Trusted witness", "Home visit"])
        if st.button("Record verification"): run("UPDATE pensioners SET last_pol=? WHERE id=?", (str(dt.date.today()), pid)); log(f"PoL {pid} via {m}"); st.rerun()
    elif page == "Fraud & Risk":
        pay = q("SELECT pid FROM payments"); al = []
        for ph, g in P.groupby("phone"):
            if len(g) > 1: al.append(("High", "Same phone on multiple pensioners", ", ".join(g.id)))
        for acc, g in P.groupby("account"):
            if len(g) > 1: al.append(("High", "Shared account", ", ".join(g.id)))
        for i in P[(P.status == "Deceased") & P.id.isin(pay.pid)].id: al.append(("Critical", "Payment to deceased pensioner", i))
        for i in P[(P.status == "Active") & P.last_pol.apply(pol_due)].id[:10]: al.append(("Medium", "Active with expired PoL", i))
        st.dataframe(pd.DataFrame(al, columns=["Severity", "Rule", "Pensioner(s)"]), use_container_width=True)
    elif page == "Support Console":
        T_ = q("SELECT * FROM tickets ORDER BY id DESC"); st.dataframe(T_, use_container_width=True)
        if len(T_):
            tid = st.selectbox("Ticket", T_.id); ns = st.selectbox("Set status", ["In progress", "Resolved", "Escalated"])
            if st.button("Update ticket"): run("UPDATE tickets SET status=? WHERE id=?", (ns, int(tid))); log(f"Ticket {tid} {ns}"); st.rerun()
    elif page == "Reports":
        pay = q("SELECT status,COUNT(*) n,SUM(amount) total FROM payments GROUP BY status"); st.subheader("Payment reconciliation"); st.dataframe(pay)
        for name, df in [("pensioners", P), ("payments", q("SELECT * FROM payments ORDER BY id"))]:
            st.download_button(f"Export {name} (CSV)", df.to_csv(index=False), f"{name}.csv")
    else:
        st.dataframe(q("SELECT * FROM audit ORDER BY id DESC"), use_container_width=True)

# ---------------- Router ----------------
try:
    init_db()
except Exception as e:          # show the real reason instead of a blank "error" page
    msg = f"{type(e).__name__}: {e}"
    try:
        from urllib.parse import urlparse, unquote
        pw = urlparse(DB_URL).password
        for secret in filter(None, (pw, unquote(pw or ""))):
            msg = msg.replace(secret, "***")
    except Exception:
        pass
    st.error("Could not connect to the database. Check the DATABASE_URL secret (Session pooler string, correct password).")
    st.code(msg)
    st.stop()
r = st.session_state.get("role")
if r == "pensioner": pensioner_portal()
elif r == "staff": staff_console()
else: login()
