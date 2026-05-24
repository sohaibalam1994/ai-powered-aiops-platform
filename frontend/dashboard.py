from backend.root_cause_engine import analyze_root_cause
from streamlit_autorefresh import st_autorefresh
import random
import time
import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

df = pd.read_csv("data/logs.csv")

# -----------------------------------
# REAL-TIME METRICS
# -----------------------------------

cpu_usage = random.randint(40, 95)
memory_usage = random.randint(35, 90)
active_alerts = random.randint(1, 12)
health_score = random.randint(70, 99)


# -----------------------------------
# PAGE CONFIG
# -----------------------------------


st.set_page_config(
    page_title="AIOps Guardian",
    layout="wide",
    initial_sidebar_state="expanded"
)
# -----------------------------------
# AUTO REFRESH
# -----------------------------------

st_autorefresh(
    interval=3000,
    limit=None,
    key="live_dashboard"
)

# -----------------------------------
# DARK THEME STYLING
# -----------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.metric-card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

div[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border: 1px solid #333;
    padding: 15px;
    border-radius: 12px;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------

st.title("🚨 AIOps Guardian")
# -----------------------------------
# ALERT BANNER
# -----------------------------------

# -----------------------------------
# SESSION STATE INIT
# -----------------------------------

if "simulate" not in st.session_state:
    st.session_state.simulate = False

if "failed_service" not in st.session_state:
    st.session_state.failed_service = None

if st.session_state.simulate:

    st.markdown(f"""
    <div style="
        background-color:#8B0000;
        padding:15px;
        border-radius:10px;
        margin-bottom:20px;
        text-align:center;
        color:white;
        font-size:20px;
        font-weight:bold;
        animation: pulse 2s infinite;
    ">
    🚨 CRITICAL INCIDENT DETECTED:
    {st.session_state.failed_service}
    failure impacting dependent services
    </div>
    """, unsafe_allow_html=True)
st.caption("AI-Powered Dependency Intelligence Platform")

# -----------------------------------
# LOAD DATA
# -----------------------------------

df = pd.read_csv("data/logs.csv")

# -----------------------------------
# BUILD DEPENDENCY GRAPH
# -----------------------------------

G = nx.DiGraph()

for i in range(len(df) - 1):

    current_service = df.iloc[i]["service"]
    next_service = df.iloc[i + 1]["service"]

    if current_service == "database" and next_service == "auth-service":
        continue

    if current_service != next_service:
        G.add_edge(current_service, next_service)

# -----------------------------------
# SIDEBAR MENU
# -----------------------------------

with st.sidebar:

    selected = option_menu(
        "AIOps Menu",
        ["Dashboard", "Incidents", "Telemetry"],
        icons=["speedometer2", "exclamation-triangle", "database"],
        menu_icon="cpu",
        default_index=0
    )

    st.markdown("---")

    st.subheader("⚠ Failure Simulation")

    failed_service = st.selectbox(
        "Select Failed Service",
        list(G.nodes())
    )

    if "simulate" not in st.session_state:
        st.session_state.simulate = False

    if "failed_service" not in st.session_state:
        st.session_state.failed_service = None

    if st.button("Simulate Failure"):

        st.session_state.simulate = True
        st.session_state.failed_service = failed_service

# -----------------------------------
# BLAST RADIUS
# -----------------------------------

impacted_services = []
root_analysis = None

if st.session_state.simulate:

    failed_service = st.session_state.failed_service

    impacted_services = list(
        nx.descendants(G, failed_service)
    )

    root_analysis = analyze_root_cause(
        failed_service
    )

# -----------------------------------
# DYNAMIC RISK SCORES
# -----------------------------------

risk_scores = {}

for service in G.nodes():

    if (
        st.session_state.simulate
        and service == failed_service
    ):

        risk_scores[service] = random.randint(90, 99)

    elif service in impacted_services:

        risk_scores[service] = random.randint(70, 89)

    else:

        risk_scores[service] = random.randint(20, 60)
# -----------------------------------
# METRICS ROW
# -----------------------------------

st.subheader("📊 Infrastructure Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "CPU Usage",
    f"{cpu_usage}%"
)

col2.metric(
    "Memory Usage",
    f"{memory_usage}%"
)

col3.metric(
    "Active Alerts",
    active_alerts
)

col4.metric(
    "System Health",
    f"{health_score}%"
)

st.markdown("---")

# -----------------------------------
# LIVE MONITORING CHARTS
# -----------------------------------

chart1, chart2 = st.columns(2)

with chart1:

    st.subheader("📈 CPU Trend")

    cpu_data = pd.DataFrame({
        "CPU": [random.randint(30, 95) for _ in range(20)]
    })

    st.line_chart(cpu_data, width='stretch')

with chart2:

    st.subheader("📈 Memory Trend")

    memory_data = pd.DataFrame({
        "Memory": [random.randint(20, 90) for _ in range(20)]
    })

    st.area_chart(memory_data, width='stretch')

# -----------------------------------
# GRAPH + INCIDENT PANEL
# -----------------------------------

left, right = st.columns([2, 1])

# -----------------------------------
# NETWORK GRAPH
# -----------------------------------

with left:

    st.subheader("🔗 Service Dependency Graph")

    pos = nx.spring_layout(G, seed=42)

    edge_x = []
    edge_y = []

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=2),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    node_text = []
    node_colors = []

    for node in G.nodes():

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)

        node_text.append(node)

        if st.session_state.simulate and node == failed_service:
            node_colors.append("red")

        elif st.session_state.simulate and node in impacted_services:
            node_colors.append("orange")

        else:
            node_colors.append("#00CC96")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=35,
            color=node_colors,
            line_width=2
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            height=600
        )
    )

    st.plotly_chart(fig, width='stretch')
# -----------------------------------
# INCIDENT PANEL
# -----------------------------------

with right:

    st.subheader("🚨 Incident Panel")

    if st.session_state.simulate:

        st.error(f"{failed_service} failure detected")

        st.markdown("### Blast Radius")

        for service in impacted_services:
            st.write(f"🔸 {service}")

        st.markdown("---")
        st.subheader("🧠 AI Root Cause Analysis")

        st.error(
            f"Probable Cause: "
            f"{root_analysis['cause']}"
        )

        st.metric(
            "Confidence Score",
            f"{root_analysis['confidence']}%"
        )

        st.info(root_analysis["reason"])
        
        st.markdown("---")

        st.subheader("📝 AI Incident Summary")

        incident_summary = f"""
        High latency and operational degradation detected
        in {failed_service}. The issue is propagating across
        dependent services within the application topology.

        Probable root cause:
        {root_analysis['cause']}.

        Estimated blast radius:
        {len(impacted_services)} impacted services.

        AI recommends immediate remediation to prevent
        cascading failures and SLA breaches.
        """

        st.warning(incident_summary)

        st.subheader("🤖 AI Recommendations")

        recommendations = {
            "payment-service": [
                "Increase timeout threshold",
                "Restart payment pods",
                "Check DB connection pooling"
            ],
            "order-service": [
                "Scale order workers",
                "Optimize queue handling"
            ],
            "database": [
                "Check replication lag",
                "Increase DB connections"
            ]
        }

        fixes = recommendations.get(
            failed_service,
            ["Investigate manually"]
        )

        for fix in fixes:
            st.success(fix)

        st.markdown("---")

        st.subheader("🎫 Auto Ticket")

        st.json({
            "ticket_id": "INC-1001",
            "priority": "HIGH",
            "status": "OPEN",
            "service": failed_service
        })

    else:

        st.success("No active incidents")

# -----------------------------------
# RISK HEATMAP
# -----------------------------------

st.markdown("---")

st.subheader("🔥 Dynamic Risk Heatmap")

for service, risk in risk_scores.items():

    if risk >= 90:
        color = "red"
        status = "🔴 Critical"

    elif risk >= 70:
        color = "orange"
        status = "🟠 High"

    elif risk >= 50:
        color = "yellow"
        status = "🟡 Medium"

    else:
        color = "green"
        status = "🟢 Healthy"

    st.markdown(
        f"""
        <div style="
            background-color:#1E1E1E;
            padding:10px;
            border-radius:10px;
            margin-bottom:10px;
        ">

        <div style="
            display:flex;
            justify-content:space-between;
            color:white;
            font-weight:bold;
        ">
            <span>{service}</span>
            <span>{risk}% {status}</span>
        </div>

        <div style="
            background-color:#333;
            border-radius:10px;
            height:15px;
            margin-top:8px;
        ">

        <div style="
            width:{risk}%;
            background-color:{color};
            height:15px;
            border-radius:10px;
        "></div>

        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------
# SERVICE HEALTH
# -----------------------------------

st.markdown("---")

st.subheader("🟢 Service Health Status")

health_data = pd.DataFrame({
    "Service": list(G.nodes()),
    "Health": [
        random.randint(75, 100)
        for _ in range(len(G.nodes()))
    ],
    "Status": [
        random.choice(["Healthy", "Warning", "Critical"])
        for _ in range(len(G.nodes()))
    ]
})

st.dataframe(
    health_data,
    width='stretch'
)

# -----------------------------------
# TELEMETRY TABLE
# -----------------------------------

st.markdown("---")

st.subheader("📄 Live Telemetry Logs")

st.dataframe(
    df.tail(20),
    width='stretch'
)