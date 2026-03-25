import streamlit as st
import requests
import pandas as pd
import altair as alt

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(layout="wide", page_title="PDF Accessibility Dashboard")

# -------------------------------
# Custom CSS (Cards + Styling)
# -------------------------------
st.markdown("""
    <style>
    .card {
        padding: 20px;
        border-radius: 12px;
        background-color: #f0f8ff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        border: 1px solid #000000;      
    }
    .metric {
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 1px 5px rgba(0,0,0,0.1);
        border: 1px solid #000000;    
    }
    .vega-embed {
        border: 1px solid #000000;   /* black border */
        border-radius: 5px;
    }        
    .hackathon-tag {
        position: fixed;
        top: 50px;
        right: 20px;
        font-weight: 600;
        font-size: 14px;
        color: #333;
        background: rgba(59, 130, 246, 0.95);
        padding: 6px 14px;
        border-radius: 8px;
        box-shadow: 0 1px 5px rgba(0,0,0,0.15);
        z-index: 9999999;
    }

    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Render the Floating Text
# -------------------------------
st.markdown(
    '<div class="hackathon-tag">Gemini CLI Technothon - Team_ASV</div>',
    unsafe_allow_html=True
)

# -------------------------------
# CENTER TITLE
# -------------------------------
st.markdown(
    "<h1 style='text-align: center;'>📄 PDF Accessibility Dashboard</h1>",
    unsafe_allow_html=True
)

# -------------------------------
# Fetch API Data
# -------------------------------
try:
    response = requests.get("http://app:8000/report")
    report = response.json()
except:
    st.error("❌ Cannot connect to API. Is FastAPI running?")
    st.stop()

if "message" in report:
    st.warning(report["message"])
    st.stop()

# -------------------------------
# SUMMARY → FULL WIDTH TILE
# -------------------------------
with st.container():
    st.markdown('<div class="card"><h3 style="text-align: center;">📊 Summary</h3>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f'<div class="metric">📁<br><b>{report["total_files"]}</b><br>Total Files</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric">⚠️<br><b>{report["total_issues"]}</b><br>Total Issues</div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric">✅<br><b>{report.get("total_fixed",0)}</b><br>Fixed</div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric">📈<br><b>{report["average_score"]}%</b><br>Avg Score</div>', unsafe_allow_html=True)

    # if report["total_issues"] == 0:
    #     st.success("All files compliant 🎉")
    # else:
    #     st.warning(f"{report['total_issues']} issues detected")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# STATUS + ISSUE TREND ROW
# -------------------------------
col_status, col_trend = st.columns(2)

with col_status:
    with st.container():
            st.markdown('<div class="card"><h3 style="text-align: center;">📌 Status Distribution</h3>', unsafe_allow_html=True)

            status_df = pd.DataFrame.from_dict(
                report["status_summary"], orient="index", columns=["count"]
            ).reset_index()

            status_df.columns = ["status", "count"]

            # ✅ FIX 1: Normalize values
            status_df["status"] = status_df["status"].str.strip().str.lower()

            # ✅ FIX 2: Ensure all categories exist
            all_status = ["compliant", "partial", "non-compliant"]
            status_df = status_df.set_index("status").reindex(all_status, fill_value=0).reset_index()

            # ✅ Calculate percentage
            total = status_df["count"].sum()
            status_df["percentage"] = (status_df["count"] / total * 100).round(1)

            # ✅ Donut Chart
            chart = alt.Chart(status_df).mark_arc(innerRadius=70).encode(
                theta=alt.Theta(field="count", type="quantitative"),
                color=alt.Color("status", scale=alt.Scale(
                    domain=all_status,
                    range=["green", "orange", "red"]
                )),
                tooltip=[
                    alt.Tooltip("status", title="Status"),
                    alt.Tooltip("count", title="Count"),
                    alt.Tooltip("percentage", title="%", format=".1f")
                ]
            ).properties(height=300).configure_legend(orient="top-right")   

            st.altair_chart(chart, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

with col_trend:
    with st.container():
            st.markdown('<div class="card"><h3 style="text-align: center;">📈 Issue Trends</h3>', unsafe_allow_html=True)

            if report.get("issue_trends"):
                trend_df = pd.Series(report["issue_trends"]).reset_index()
                trend_df.columns = ["issue", "count"]

                trend_chart = alt.Chart(trend_df).mark_bar().encode(
                    x=alt.X(
                        "count",
                        title="Count",
                        axis=alt.Axis(format="d", tickMinStep=1)   
                    ),
                    y=alt.Y("issue", sort="-x"),
                    color=alt.value("#4c78a8")
                ).properties(height=300)

                st.altair_chart(trend_chart, use_container_width=True)
            else:
                st.success("No issues found 🎉")

            st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# WORST FILE TILE (LEFT)
# -------------------------------
#col_worst, col_empty = st.columns([1,1])

#with col_worst:
with st.container():
        st.markdown('<div class="card"><h3 style="text-align: center;">⚠️ Error Trend </h3>', unsafe_allow_html=True)
        
        if "files" in report:
            df_trend = pd.DataFrame(report["files"])

            # Convert timestamp
            df_trend["timestamp"] = pd.to_datetime(df_trend["timestamp"])

            # Count issues per file
            df_trend["issue_count"] = df_trend["issues"].apply(len)

            # Aggregate by date
            trend_line_df = df_trend.groupby("timestamp")["issue_count"].sum().reset_index()

            # Line chart
            line_chart = alt.Chart(trend_line_df).mark_line(point=True).encode(
                x=alt.X(
                    "yearmonthdate(timestamp):T",   # ✅ date only
                    title="Date",
                    axis=alt.Axis(format="%Y-%m-%d")  # optional formatting
                ),
                y=alt.Y(
                    "issue_count:Q",
                    title="Total Issues",
                    axis=alt.Axis(format="d", tickMinStep=1)  # integers only
                ),
                tooltip=[
                    alt.Tooltip("timestamp:T", title="Date"),
                    alt.Tooltip("issue_count:Q", title="Issues")
                ]
            ).properties(height=300,width="container")

            st.altair_chart(line_chart, use_container_width=True)

        else:
            st.info("No trend data available")

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# File Details Table (Same)
# -------------------------------
st.divider()
st.subheader("📋 File Details")

if "files" in report:
    df = pd.DataFrame(report["files"])

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    if "timestamp" in df.columns:
        df = df.sort_values(by="timestamp", ascending=False)

    df["status"] = df["score"].apply(
        lambda x: "compliant" if x >= 90 else "partial" if x >= 60 else "non-compliant"
    )

    def highlight_status(val):
        color = "green" if val == "compliant" else "orange" if val == "partial" else "red"
        return f"color: {color}; font-weight: bold"

    st.dataframe(
        df.style.applymap(highlight_status, subset=["status"]),
        use_container_width=True
    )
else:
    st.info("No file-level data available")

# -------------------------------
# Raw JSON (Same)
# -------------------------------
st.subheader("🔍 Full Report")
st.json(report)