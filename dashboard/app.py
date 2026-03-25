# import sys
# import os
#
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.markdown("<h1 style='text-align: center;'>📄 PDF Accessibility Dashboard</h1>", unsafe_allow_html=True)

# -------------------------------
# FETCH DATA
# -------------------------------
report = fetch_report()

if "error" in report:
    st.error(report["error"])
    st.stop()

# -------------------------------
# HEALTH + PROGRESS
# -------------------------------
score = report["average_score"]
status = get_health_status(score)
color = "green" if status == "good" else "orange" if status == "warning" else "red"

st.markdown(f"""
<div style="text-align:center; font-size:20px;">
Overall Health: <span style="color:{color}; font-weight:bold;">{score}%</span>
</div>
""", unsafe_allow_html=True)

st.progress(score / 100)

# -------------------------------
# SUMMARY
# -------------------------------
st.markdown('<div class="card"><h3>📊 System Overview</h3>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f'<div class="metric">📁<br><b>{report["total_files"]}</b><br>Total Files</div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric" style="border-left: 5px solid red;">⚠️<br><b>{report["total_issues"]}</b><br>Total Issues</div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric">✅<br><b>{report.get("total_fixed",0)}</b><br>Fixed</div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric">📈<br><b>{score}%</b><br>Avg Score</div>', unsafe_allow_html=True)

if score < 60:
    st.error("🚨 Critical accessibility issues detected")
elif score < 80:
    st.warning("⚠️ Moderate accessibility issues")
else:
    st.success("✅ Accessibility looks good")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# STATUS + ISSUE TREND
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card"><h3>📌 Status Distribution</h3>', unsafe_allow_html=True)

    status_df = pd.DataFrame.from_dict(report["status_summary"], orient="index", columns=["count"]).reset_index()
    status_df.columns = ["status", "count"]
    status_df["status"] = status_df["status"].str.lower()

    chart = alt.Chart(status_df).mark_arc(innerRadius=70).encode(
        theta="count",
        color=alt.Color("status", scale=alt.Scale(range=["green", "orange", "red"]))
    )

    st.altair_chart(chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><h3>📈 Issue Intelligence</h3>', unsafe_allow_html=True)

    trend_df = pd.Series(report.get("issue_trends", {})).reset_index()
    trend_df.columns = ["issue", "count"]

    if not trend_df.empty:
        top_issue = trend_df.iloc[0]["issue"]
        st.info(f"🔥 Most common issue: {top_issue}")

        chart = alt.Chart(trend_df).mark_bar().encode(
            x="count",
            y=alt.Y("issue", sort="-x")
        )

        st.altair_chart(chart, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# SCORE TREND
# -------------------------------
if "files" in report:
    df_trend = pd.DataFrame(report["files"])

    if "timestamp" in df_trend.columns:
        df_trend["timestamp"] = pd.to_datetime(df_trend["timestamp"])
        df_trend = df_trend.sort_values("timestamp")

        chart = alt.Chart(df_trend).mark_line(point=True).encode(
            x="timestamp:T",
            y="score:Q",
            tooltip=[
                alt.Tooltip("file_name:N", title="File"),
                alt.Tooltip("score:Q", title="Score")
            ]
        )

        st.markdown('<div class="card"><h3>📉 Score Trend</h3>', unsafe_allow_html=True)
        st.altair_chart(chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# AUTO RECOMMENDATIONS
# -------------------------------
if report.get("issue_trends"):
    st.markdown('<div class="card"><h3>💡 Auto Recommendations</h3>', unsafe_allow_html=True)

    for issue, count in report["issue_trends"].items():
        st.markdown(f"**{issue} ({count})** → {get_recommendation(issue)}")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# FILE TABLE + SEARCH
# -------------------------------
st.subheader("📂 Accessibility Breakdown")

df = pd.DataFrame(report["files"])
df["status"] = df["score"].apply(get_status)

search = st.text_input("🔍 Search file")
if search:
    df = df[df["file_name"].str.contains(search, case=False)]

st.dataframe(df, use_container_width=True)