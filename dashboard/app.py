import streamlit as st
import pandas as pd
import altair as alt
import os

from utils.api import fetch_report
from utils.helpers import get_status, get_health_status
from utils.recommendations import get_recommendation

st.set_page_config(layout="wide", page_title="PDF Accessibility Dashboard")

# -------------------------------
# LOAD CSS
# -------------------------------

BASE_DIR = os.path.dirname(__file__)
css_path = os.path.join(BASE_DIR, "assets", "styles.css")

if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------

st.markdown(
    "<h1 style='text-align: center;'>📄 PDF Accessibility Dashboard</h1>",
    unsafe_allow_html=True
)

# -------------------------------
# FETCH DATA
# -------------------------------

report = fetch_report()

if "error" in report:
    st.error(report["error"])
    st.stop()

files = report.get("files", [])

# -------------------------------
# DERIVE SCORE
# -------------------------------

if files:
    avg_non_compliance = sum(f.get("nonCompliancePercent", 0) for f in files) / len(files)
    score = round(100 - avg_non_compliance, 2)
else:
    score = 0

status = get_health_status(score)
color = "green" if status == "good" else "orange" if status == "warning" else "red"

st.markdown(
    f"""
    <div style="text-align:center; font-size:20px;">
        Overall Health: <span style="color:{color}; font-weight:bold;">{score}%</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.progress(score / 100 if score else 0)

# -------------------------------
# SUMMARY
# -------------------------------

st.markdown('<div class="card"><h3>📊 System Overview</h3>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

c1.markdown(
    f'<div class="metric">📁<br><b>{report.get("totalFiles", 0)}</b><br>Total Files</div>',
    unsafe_allow_html=True
)
c2.markdown(
    f'<div class="metric" style="border-left: 5px solid red;">⚠️<br><b>{report.get("totalIssues", 0)}</b><br>Total Issues</div>',
    unsafe_allow_html=True
)
c3.markdown(
    f'<div class="metric">📈<br><b>{score}%</b><br>Health Score</div>',
    unsafe_allow_html=True
)

if score < 60:
    st.error("🚨 Critical accessibility issues detected")
elif score < 80:
    st.warning("⚠️ Moderate accessibility issues")
else:
    st.success("✅ Accessibility looks good")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# STATUS DISTRIBUTION
# -------------------------------

st.markdown('<div class="card"><h3>📌 Status Distribution</h3>', unsafe_allow_html=True)

status_df = pd.DataFrame.from_dict(
    report.get("complianceBreakdown", {}),
    orient="index",
    columns=["count"]
).reset_index()

status_df.columns = ["status", "count"]

if not status_df.empty:
    chart = alt.Chart(status_df).mark_arc(innerRadius=70).encode(
        theta="count",
        color=alt.Color("status", scale=alt.Scale(range=["green", "red"]))
    )
    st.altair_chart(chart, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# ISSUE INTELLIGENCE
# -------------------------------

st.markdown('<div class="card"><h3>📈 Issue Intelligence</h3>', unsafe_allow_html=True)

trend_df = pd.DataFrame(report.get("topIssueTypes", []))

if not trend_df.empty:
    trend_df.columns = ["issue", "count"]

    top_issue = trend_df.iloc[0]["issue"]
    st.info(f"🔥 Most common issue: {top_issue}")

    chart = alt.Chart(trend_df).mark_bar().encode(
        x="count",
        y=alt.Y("issue", sort="-x")
    )

    st.altair_chart(chart, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# WORST FILE
# -------------------------------

worst = report.get("worstFile")

if worst:
    st.markdown('<div class="card"><h3>🚨 Worst Performing File</h3>', unsafe_allow_html=True)
    st.error(f"{worst.get('fileName')} ({worst.get('nonCompliancePercent')}% non-compliant)")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# AUTO RECOMMENDATIONS
# -------------------------------

if report.get("topIssueTypes"):
    st.markdown('<div class="card"><h3>💡 Auto Recommendations</h3>', unsafe_allow_html=True)

    for item in report["topIssueTypes"]:
        issue = item.get("issue")
        count = item.get("count")
        st.markdown(f"**{issue} ({count})** → {get_recommendation(issue)}")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# FILE TABLE + SEARCH
# -------------------------------

st.subheader("📂 Accessibility Breakdown")

df = pd.DataFrame(files)

if not df.empty:
    df["score"] = 100 - df["nonCompliancePercent"]
    df["status"] = df["score"].apply(get_status)

    search = st.text_input("🔍 Search file")
    if search:
        df = df[df["fileName"].str.contains(search, case=False)]

    st.dataframe(df, use_container_width=True)
