import streamlit as st
import requests
import pandas as pd

# -------------------------------
# Config
# -------------------------------
st.set_page_config(layout="wide", page_title="PDF Accessibility Dashboard")

st.title("📄 PDF Accessibility Dashboard")

# -------------------------------
# Fetch API Data
# -------------------------------
try:
    # response = requests.get("http://localhost:8000/report")
    response = requests.get("http://app:8000/report")
    report = response.json()
except:
    st.error("❌ Cannot connect to API. Is FastAPI running?")
    st.stop()

if "message" in report:
    st.warning(report["message"])
    st.stop()

# -------------------------------
# TOP ROW → Summary + Status
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Files", report["total_files"])
    c2.metric("Total Issues", report["total_issues"])
    c3.metric("Fixed Issues", report.get("total_fixed", 0))
    c4.metric("Avg Score", f'{report["average_score"]}%')

    if report["total_issues"] == 0:
        st.success("All files compliant 🎉")
    else:
        st.warning(f"{report['total_issues']} issues detected")

with col2:
    st.subheader("📌 Status Distribution")

    status_df = pd.DataFrame.from_dict(
        report["status_summary"], orient="index", columns=["count"]
    )

    st.bar_chart(status_df)

# -------------------------------
# BOTTOM ROW → Worst + Trends
# -------------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("⚠️ Worst File")
    st.error(report["worst_file"])

with col4:
    st.subheader("📈 Issue Trends")

    if report.get("issue_trends"):
        st.bar_chart(pd.Series(report["issue_trends"]))
    else:
        st.success("No issues found 🎉")

    st.caption("Most common accessibility issues")

# -------------------------------
# FULL WIDTH → File Details
# -------------------------------
st.divider()
st.subheader("📋 File Details")

if "files" in report:
    df = pd.DataFrame(report["files"])

    df["status"] = df["score"].apply(
        lambda x: "compliant" if x >= 90 else "partial" if x >= 60 else "non-compliant"
    )

    st.dataframe(df, use_container_width=True)
else:
    st.info("No file-level data available")

# -------------------------------
# FULL WIDTH → Raw JSON
# -------------------------------
st.subheader("🔍 Full Report")
st.json(report)