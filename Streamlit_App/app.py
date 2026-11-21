import html
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from google_sheets_connection import load_live_sales_data
from live_sales_intelligence import analyze_followups

st.set_page_config(
    page_title="REVENUEOS | Sales Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA = Path(__file__).resolve().parent / "data"


@st.cache_data
def read_data(filename):
    path = DATA / filename
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


sales = read_data("sales_revenue_intelligence.csv")
logs = read_data("enhanced_decision_logs.csv")
regional_summary = read_data("regional_revenue_summary.csv")
product_summary = read_data("product_revenue_summary.csv")
agent_summary = read_data("agent_revenue_summary.csv")
risk_summary = read_data("risk_revenue_summary.csv")

# Merge regional information from decision logs
if not sales.empty and not logs.empty:
    if "opportunity_id" in sales and "opportunity_id" in logs:
        extras = [
            c for c in [
                "regional_office",
                "decision_method",
                "rule_version",
                "assessment_timestamp_utc"
            ]
            if c in logs and c not in sales
        ]

        if extras:
            lookup = (
                logs[["opportunity_id"] + extras]
                .drop_duplicates("opportunity_id")
            )

            sales = sales.merge(
                lookup,
                on="opportunity_id",
                how="left",
                validate="many_to_one"
            )

if not sales.empty:
    for c in [
        "sales_price",
        "win_probability_pct",
        "weighted_pipeline_value",
        "data_quality_score"
    ]:
        if c in sales:
            sales[c] = pd.to_numeric(
                sales[c], errors="coerce"
            )

    needed = {"sales_price", "win_probability_pct"}

    if (
        "weighted_pipeline_value" not in sales
        and needed.issubset(sales.columns)
    ):
        sales["weighted_pipeline_value"] = (
            sales["sales_price"]
            * sales["win_probability_pct"] / 100
        )

# ==========================================================
# APPLICATION DESIGN
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, .stApp {
    font-family: 'DM Sans', sans-serif;
    color: #E6EDFA;
}

.stApp {
    background:
        radial-gradient(
            ellipse at 92% 2%,
            #201b3c 0%,
            transparent 40%
        ),
        #0A101D;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.7rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#151C30,#0D1423);
    border-right: 1px solid #303A52;
}

[data-testid="stSidebar"] .stButton button {
    min-height: 42px;
    text-align: left;
    justify-content: flex-start;
    border-radius: 10px;
    font-size: 13px;
}

[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: #3D305E;
    color: white;
    border: 1px solid #8665C9;
    box-shadow: inset 3px 0 0 #BDA5FF;
}

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 10px 0 22px;
    border-bottom: 1px solid #303A52;
    margin-bottom: 15px;
}

.brand-icon {
    background: linear-gradient(135deg,#A78BFA,#6D45D6);
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 24px;
    color: white;
}

.brand-title {
    font: 700 23px 'Space Grotesk',sans-serif;
    color: white;
}

.brand-sub {
    font-size: 9px;
    letter-spacing: 1.3px;
    color: #B6C3DC;
}

.eyebrow {
    font-size: 11px;
    letter-spacing: 2px;
    color: #BCA7FF;
    font-weight: 700;
    margin-bottom: 14px;
}

.hero {
    background:
        radial-gradient(
            circle at 87% 15%,
            #4D397D70,
            transparent 45%
        ),
        linear-gradient(110deg,#1B2745,#171B33);
    border: 1px solid #454469;
    border-radius: 20px;
    padding: 35px;
    margin-bottom: 22px;
}

.hero-tag {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 30px;
    background: #8B5CF624;
    color: #D8C8FF;
    border: 1px solid #8B5CF655;
    font-size: 10px;
    margin-bottom: 15px;
}

.hero h1 {
    font: 700 42px 'Space Grotesk',sans-serif;
    color: white;
    margin: 0 0 14px;
}

.hero p {
    font-size: 14px;
    line-height: 1.85;
    color: #B7C6DE;
    max-width: 800px;
}

.section {
    font: 700 22px 'Space Grotesk',sans-serif;
    color: white;
    margin: 25px 0 6px;
}

.sub {
    font-size: 13px;
    color: #9AACC8;
    margin-bottom: 16px;
}

.feature {
    background: linear-gradient(135deg,#1B2842,#151D30);
    border: 1px solid #35425E;
    border-radius: 15px;
    padding: 20px;
    min-height: 138px;
    margin-bottom: 10px;
}

.feature strong {
    color: #F8FAFC;
    font-size: 15px;
}

.feature p {
    font-size: 12px;
    color: #A5B6CE;
    line-height: 1.7;
    margin: 10px 0 0;
}

.feature .symbol {
    font-size: 23px;
    color: #BDA5FF;
    margin-bottom: 12px;
}

.note {
    background: #18233B;
    border: 1px solid #344360;
    border-left: 3px solid #BDA5FF;
    padding: 17px 20px;
    border-radius: 12px;
    color: #C6D3E8;
    font-size: 13px;
    line-height: 1.8;
    margin: 14px 0;
}

.status {
    background: #1A253C;
    border: 1px solid #354360;
    border-radius: 12px;
    padding: 15px;
    color: #B5C6E0;
    font-size: 12px;
    line-height: 1.8;
    margin-top: 20px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #34415D;
    border-radius: 12px;
    overflow: hidden;
}

@media(max-width:750px) {
    .hero {padding: 23px;}
    .hero h1 {font-size: 29px;}
    .feature {min-height: 0;}
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# REUSABLE FUNCTIONS
# ==========================================================

def h(value):
    return html.escape(str(value))


def markup(content):
    st.markdown(content, unsafe_allow_html=True)


def hero(tag, title, description):
    markup(
        f'<div class="hero">'
        f'<span class="hero-tag">{h(tag)}</span>'
        f'<h1>{h(title)}</h1>'
        f'<p>{h(description)}</p>'
        f'</div>'
    )


def section(title, subtitle=""):
    markup(
        f'<div class="section">{h(title)}</div>'
        f'<div class="sub">{h(subtitle)}</div>'
    )


def note(title, message):
    markup(
        f'<div class="note">'
        f'<strong>{h(title)}</strong>'
        f'<div>{h(message)}</div>'
        f'</div>'
    )


def table(frame, name, columns=None):
    if frame is None or frame.empty:
        st.info("No matching records available.")
        return

    shown = (
        frame[[c for c in columns if c in frame]]
        if columns else frame
    )

    st.dataframe(
        shown,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download filtered CSV",
        shown.to_csv(index=False).encode(),
        f"{name}.csv",
        "text/csv",
        key=f"download_{name}"
    )


def bar(frame, category, metric, title, horizontal=False):
    if (
        frame.empty
        or category not in frame
        or metric not in frame
    ):
        st.info("No chart data for this selection.")
        return

    base = alt.Chart(frame).mark_bar(
        cornerRadiusEnd=6,
        color="#A78BFA"
    )

    if horizontal:
        chart = base.encode(
            y=alt.Y(
                f"{category}:N",
                sort="-x",
                title=None
            ),
            x=alt.X(
                f"{metric}:Q",
                title=title
            ),
            tooltip=[
                category,
                alt.Tooltip(metric, format=",.2f")
            ]
        )
    else:
        chart = base.encode(
            x=alt.X(
                f"{category}:N",
                sort="-y",
                title=None
            ),
            y=alt.Y(
                f"{metric}:Q",
                title=title
            ),
            tooltip=[
                category,
                alt.Tooltip(metric, format=",.2f")
            ]
        )

    st.altair_chart(
        chart.properties(height=350),
        use_container_width=True
    )


def options(frame, column):
    if column not in frame:
        return []

    return sorted(
        frame[column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


def sales_filters(frame, prefix):
    with st.expander(
        "Filter sales opportunities",
        expanded=False
    ):
        c1, c2, c3 = st.columns(3)

        with c1:
            region = st.multiselect(
                "Regional office",
                options(frame, "regional_office"),
                default=options(frame, "regional_office"),
                key=prefix + "region"
            )

        with c2:
            agent = st.multiselect(
                "Sales agent",
                options(frame, "sales_agent"),
                default=options(frame, "sales_agent"),
                key=prefix + "agent"
            )

        with c3:
            risk = st.multiselect(
                "Deal risk",
                options(frame, "deal_risk_level"),
                default=options(frame, "deal_risk_level"),
                key=prefix + "risk"
            )

    result = frame.copy()

    for col, chosen in [
        ("regional_office", region),
        ("sales_agent", agent),
        ("deal_risk_level", risk)
    ]:
        if col in result:
            result = result[
                result[col].astype(str).isin(chosen)
            ]

    return result


def aggregate(frame, by):
    columns = [
        by,
        "opportunities",
        "pipeline_value",
        "weighted_value"
    ]

    if frame.empty or by not in frame:
        return pd.DataFrame(columns=columns)

    result = (
        frame.groupby(by, dropna=False)
        .agg(
            opportunities=("opportunity_id", "count"),
            pipeline_value=("sales_price", "sum"),
            weighted_value=(
                "weighted_pipeline_value", "sum"
            )
        )
        .reset_index()
    )

    return result.sort_values(
        "pipeline_value",
        ascending=False
    )


# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================



NAV = [
    "Executive Overview",
    "Decision Intelligence",
    "Revenue Analytics",
    "Sales Performance",
    "Deal Risk Monitor",
    "Decision Audit Center",
    "Sales Strategy & Decision Center",
    "Live Sales Operations"
]


if "page" not in st.session_state:
    st.session_state.page = NAV[0]

with st.sidebar:
    markup(
        '<div class="brand">'
        '<div class="brand-icon">◆</div>'
        '<div>'
        '<div class="brand-title">REVENUEOS</div>'
        '<div class="brand-sub">'
        'SALES INTELLIGENCE SUITE'
        '</div>'
        '</div>'
        '</div>'
    )

    markup('<div class="eyebrow">WORKSPACE</div>')

    symbols = ["◈", "✦", "▥", "◎", "◇", "≡", "◉", "●"]


    for label, symbol in zip(NAV, symbols):
        selected = st.session_state.page == label

        if st.button(
            f"{symbol}  {label}",
            key="nav_" + label,
            type="primary" if selected else "secondary",
            use_container_width=True
        ):
            st.session_state.page = label
            st.rerun()

    markup(
        '<div class="status">'
        '<strong>Workspace ready</strong>'
        '<div>Historical sales intelligence'
        '<p>Portfolio edition · Experimental predictions</p>'
        '</div>'
        '</div>'
    )

page = st.session_state.page

markup(
    '<div class="eyebrow">'
    'REVENUEOS / INTELLIGENCE WORKSPACE'
    '</div>'
)

# ==========================================================
# DATA VALIDATION
# ==========================================================

if sales.empty:
    st.error(
        "sales_revenue_intelligence.csv is missing or empty. "
        "Put the six exported CSV files inside "
        "Streamlit_App/data/."
    )
    st.stop()

required = {
    "opportunity_id",
    "sales_agent",
    "sales_price",
    "win_probability_pct",
    "deal_risk_level",
    "weighted_pipeline_value"
}

missing = required - set(sales.columns)

if missing:
    st.error(
        "The sales CSV is missing required columns: "
        + ", ".join(sorted(missing))
    )
    st.stop()


# ==========================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ==========================================================

if page == "Executive Overview":
    hero(
        "SALES INTELLIGENCE PLATFORM",
        "Every opportunity matters. Every decision counts.",
        "Understand sales performance, evaluate opportunities "
        "and prioritize the next best actions in one "
        "connected workspace."
    )

    section(
        "Explore the workspace",
        "Seven connected areas of sales and revenue intelligence"
    )

    cards = [
        (
            "✦",
            "Decision Intelligence",
            "Experimental win probabilities and recommendations"
        ),
        (
            "▥",
            "Revenue Analytics",
            "Regional, product and risk-based pipeline comparisons"
        ),
        (
            "◎",
            "Sales Performance",
            "Explore agent portfolios and contribution"
        ),
        (
            "◇",
            "Deal Risk Monitor",
            "Review risk levels and data quality"
        ),
        (
            "≡",
            "Decision Audit Center",
            "Review recorded assessments and decision history"
        ),
        (
            "◉",
            "Sales Strategy",
            "Business priorities and recommended actions"
        )
    ]

    for start in range(0, len(cards), 3):
        cols = st.columns(3)

        for col, (symbol, title, description) in zip(
            cols, cards[start:start + 3]
        ):
            with col:
                markup(
                    '<div class="feature">'
                    f'<div class="symbol">{h(symbol)}</div>'
                    f'<strong>{h(title)}</strong>'
                    f'<p>{h(description)}</p>'
                    '</div>'
                )

    section(
        "Sales filters",
        "The chart and table respond to the same selection"
    )

    filtered = sales_filters(sales, "overview_")

    section(
        "Regional revenue distribution",
        "Filtered historical active pipeline"
    )

    regional = aggregate(filtered, "regional_office")

    bar(
        regional,
        "regional_office",
        "pipeline_value",
        "Pipeline value ($)"
    )

    if not regional.empty:
        leader = regional.iloc[0]

        note(
            "Regional insight",
            f"{leader['regional_office']} has the largest "
            f"pipeline in the current selection "
            f"(${leader['pipeline_value']:,.0f}). "
            "This measures opportunity value, not realized revenue."
        )

    section(
        "Opportunity Explorer",
        "Search and export filtered opportunity records"
    )

    q = st.text_input(
        "Search opportunity ID",
        placeholder="Enter opportunity ID",
        key="overview_search"
    )

    if q:
        filtered = filtered[
            filtered["opportunity_id"]
            .astype(str)
            .str.contains(
                q,
                case=False,
                regex=False,
                na=False
            )
        ]

    st.caption(
        f"Showing {len(filtered):,} of "
        f"{len(sales):,} historical active opportunities"
    )

    table(filtered, "overview_opportunities")


# ==========================================================
# PAGE 2 — DECISION INTELLIGENCE
# ==========================================================

elif page == "Decision Intelligence":
    hero(
        "DECISION SUPPORT",
        "Decision Intelligence",
        "Inspect experimental win probabilities, risk "
        "classifications and recommended follow-up actions."
    )

    filtered = sales_filters(sales, "decision_")

    section(
        "Opportunity decisions",
        "Prioritize follow-ups and inspect model outputs"
    )

    columns = [
        "opportunity_id",
        "sales_agent",
        "account",
        "product",
        "sales_price",
        "win_probability_pct",
        "deal_risk_level",
        "review_priority",
        "sales_action_recommendation"
    ]

    table(
        filtered,
        "decision_intelligence",
        columns
    )

    note(
        "Model limitation",
        "The existing model has weak validation performance. "
        "Probabilities and risk thresholds are experimental "
        "and must not be treated as reliable win/loss predictions."
    )


# ==========================================================
# PAGE 3 — REVENUE ANALYTICS
# ==========================================================

elif page == "Revenue Analytics":
    hero(
        "REVENUE PERFORMANCE",
        "Revenue Analytics",
        "Compare pipeline value, experimental weighted value "
        "and opportunity volume across business dimensions."
    )

    filtered = sales_filters(sales, "revenue_")

    measure = st.segmented_control(
        "Analysis measure",
        [
            "Pipeline Value",
            "Weighted Pipeline Value",
            "Opportunity Count"
        ],
        default="Pipeline Value",
        key="revenue_measure"
    )

    measure_col = {
        "Pipeline Value": "pipeline_value",
        "Weighted Pipeline Value": "weighted_value",
        "Opportunity Count": "opportunities"
    }[measure]

    tabs = st.tabs([
        "Regional performance",
        "Product performance",
        "Risk distribution"
    ])

    dimensions = [
        "regional_office",
        "product",
        "deal_risk_level"
    ]

    titles = [
        "Regional",
        "Product",
        "Risk group"
    ]

    for tab, dim, title in zip(
        tabs, dimensions, titles
    ):
        with tab:
            grouped = aggregate(filtered, dim)

            section(
                f"{title} comparison",
                f"Showing {measure.lower()} for current filters"
            )

            bar(
                grouped,
                dim,
                measure_col,
                measure,
                horizontal=(dim == "product")
            )

            table(
                grouped,
                "revenue_" + dim
            )

    note(
        "Interpretation",
        "Pipeline value is potential deal value. "
        "Weighted pipeline uses experimental win probabilities; "
        "it is not a validated revenue forecast or booked revenue."
    )


# ==========================================================
# PAGE 4 — SALES PERFORMANCE
# ==========================================================

elif page == "Sales Performance":
    hero(
        "TEAM PERFORMANCE",
        "Sales Performance",
        "Review opportunity distribution and pipeline "
        "contribution across sales agents."
    )

    filtered = sales_filters(sales, "performance_")

    agent = aggregate(
        filtered,
        "sales_agent"
    )

    section(
        "Top agents by pipeline",
        "Historical active opportunity value, not closed sales"
    )

    bar(
        agent.head(12),
        "sales_agent",
        "pipeline_value",
        "Pipeline value ($)",
        horizontal=True
    )

    table(
        agent,
        "agent_performance"
    )


# ==========================================================
# PAGE 5 — DEAL RISK MONITOR
# ==========================================================

elif page == "Deal Risk Monitor":
    hero(
        "RISK REVIEW",
        "Deal Risk Monitor",
        "Find opportunities needing attention and identify "
        "customer data quality issues."
    )

    filtered = sales_filters(sales, "risk_")

    if "review_priority" in filtered:
        choice = st.selectbox(
            "Data quality review priority",
            ["All"] + options(
                filtered,
                "review_priority"
            )
        )

        if choice != "All":
            filtered = filtered[
                filtered["review_priority"].astype(str)
                == choice
            ]

    section(
        "Risk register",
        "Risk and data quality priority are different measures"
    )

    table(
        filtered,
        "risk_register",
        [
            "opportunity_id",
            "sales_agent",
            "deal_stage",
            "sales_price",
            "win_probability_pct",
            "deal_risk_level",
            "data_quality_score",
            "review_priority",
            "sales_action_recommendation"
        ]
    )

    note(
        "Risk definition",
        "Deal risk comes from experimental model probabilities. "
        "Review priority comes from rules-based customer data "
        "quality checks; the two may disagree."
    )


# ==========================================================
# PAGE 6 — DECISION AUDIT CENTER
# ==========================================================

elif page == "Decision Audit Center":
    hero(
        "DECISION TRANSPARENCY",
        "Decision Audit Center",
        "Inspect recorded rules-based assessments, timestamps "
        "and enhanced opportunity decisions."
    )

    if logs.empty:
        st.warning(
            "enhanced_decision_logs.csv is missing or empty."
        )
    else:
        q = st.text_input(
            "Search opportunity ID",
            key="audit_search"
        )

        selected = logs.copy()

        if q:
            selected = selected[
                selected["opportunity_id"]
                .astype(str)
                .str.contains(
                    q,
                    case=False,
                    regex=False,
                    na=False
                )
            ]

        section(
            "Decision history",
            f"{len(selected):,} matching records"
        )

        table(
            selected,
            "decision_audit"
        )

        note(
            "Audit timing",
            "Assessment timestamps may refer to the original "
            "rules-based assessment rather than the later "
            "prediction or enrichment time."
        )


# ==========================================================
# PAGE 7 — SALES STRATEGY & DECISION CENTER
# ==========================================================

elif page == "Sales Strategy & Decision Center":
    hero(
        "BUSINESS STRATEGY",
        "Sales Strategy & Decision Center",
        "Understand what is happening in the pipeline, "
        "where attention is needed, and which actions "
        "could improve sales execution."
    )

    filtered = sales_filters(
        sales,
        "strategy_"
    )

    if filtered.empty:
        st.info(
            "No opportunities match the selected filters."
        )

    else:
        total = len(filtered)

        pipeline = filtered[
            "sales_price"
        ].sum()

        weighted = filtered[
            "weighted_pipeline_value"
        ].sum()

        high = filtered[
            filtered["deal_risk_level"]
            .astype(str)
            .str.lower() == "high"
        ]

        priority_column = filtered.get(
            "review_priority",
            pd.Series("", index=filtered.index)
        )

        high_priority = filtered[
            priority_column.astype(str).str.lower() == "high"
        ]

        region = aggregate(
            filtered,
            "regional_office"
        )

        product = aggregate(
            filtered,
            "product"
        )

        # BUSINESS DIAGNOSIS

        section(
            "What is happening in sales?",
            "Evidence from historical active opportunities"
        )

        leader = (
            region.iloc[0]["regional_office"]
            if not region.empty else "Unavailable"
        )

        top_product = (
            product.iloc[0]["product"]
            if not product.empty else "Unavailable"
        )

        note(
            "Pipeline diagnosis",
            f"There are {total:,} active opportunities "
            f"worth ${pipeline:,.0f} in potential pipeline. "
            f"The experimental probability-weighted value "
            f"is ${weighted:,.0f}. "
            f"{len(high):,} opportunities are labeled high risk, "
            f"and {len(high_priority):,} require high-priority "
            f"data quality review. "
            f"Largest pipeline region: {leader}. "
            f"Largest pipeline product: {top_product}."
        )

        # BUSINESS RECOMMENDATIONS

        section(
            "Where should the business focus?",
            "Priorities generated from transparent rules"
        )

        if len(high):
            note(
                "1 · High-risk deal review",
                f"Review {len(high):,} high-risk opportunities. "
                "Contact customers, confirm buying needs "
                "and update follow-up plans. "
                "These risk labels are experimental."
            )

        if len(high_priority):
            note(
                "2 · Customer information quality",
                f"Resolve missing or questionable information "
                f"for {len(high_priority):,} high-priority records "
                "before relying on downstream decisions."
            )

        if not region.empty:
            note(
                "3 · Regional execution",
                f"{leader} has the largest pipeline value "
                "in this selection. Review conversion activity "
                "and sales capacity there. Pipeline size alone "
                "does not prove superior performance."
            )

        if not product.empty:
            note(
                "4 · Product opportunity",
                f"{top_product} has the largest active pipeline "
                "by value. Check whether sales enablement, "
                "customer follow-ups and product expertise "
                "match that demand."
            )

        # WIN / LOSS OUTLOOK

        section(
            "Win / loss outlook by opportunity",
            "Experimental model-based assessment"
        )

        choices = (
            filtered["opportunity_id"]
            .dropna()
            .astype(str)
            .tolist()
        )

        selected_id = st.selectbox(
            "Choose an opportunity",
            choices,
            key="strategy_deal"
        )

        deal = filtered[
            filtered["opportunity_id"]
            .astype(str) == selected_id
        ].iloc[0]

        probability = float(
            deal["win_probability_pct"]
        )

        loss_proxy = 100 - probability

        outcome = pd.DataFrame({
            "Outcome": [
                "Model-estimated win",
                "Model-estimated loss"
            ],
            "Probability (%)": [
                probability,
                loss_proxy
            ]
        })

        bar(
            outcome,
            "Outcome",
            "Probability (%)",
            "Experimental probability (%)"
        )

        st.markdown(
            f"**Opportunity:** `{h(selected_id)}`  ·  "
            f"**Deal risk:** "
            f"{h(deal.get('deal_risk_level', 'Unknown'))}  ·  "
            f"**Value:** ${float(deal['sales_price']):,.2f}"
        )

        recommendation = str(
            deal.get(
                "sales_action_recommendation",
                "Review customer engagement and "
                "agree on a next action."
            )
        )

        note(
            "Recommended next action",
            recommendation
        )

        note(
            "Decision limitation",
            "The loss percentage is calculated as 100 minus "
            "the model's estimated win percentage. "
            "This is not a reliable prediction of a real deal "
            "outcome, nor evidence that a contract will be "
            "awarded or lost. The active opportunities contain "
            "no verified final project-award decision."
        )

        # PRIORITY DEALS

        section(
            "Deals to review first",
            "High-risk opportunities ordered by potential value"
        )

        review = high.sort_values(
            "sales_price",
            ascending=False
        )

        table(
            review,
            "strategy_priority_deals",
            [
                "opportunity_id",
                "sales_agent",
                "account",
                "product",
                "regional_office",
                "sales_price",
                "win_probability_pct",
                "deal_risk_level",
                "review_priority",
                "sales_action_recommendation"
            ]
        )


# ==========================================================
# PAGE 8 — LIVE SALES OPERATIONS
# ==========================================================

elif page == "Live Sales Operations":

    hero(
        "LIVE SALES INTELLIGENCE",
        "Live Sales Operations",
        "Monitor sales opportunities submitted through "
        "Google Forms and stored in Google Sheets."
    )

    st.caption(
        "Data source: Google Sheets — Sales_Analytics"
    )

    if st.button("Refresh Live Sales Data", key="refresh_live"):
        st.rerun()

    try:
        live_sales = load_live_sales_data()

        # Analyze follow-up dates
        live_sales = analyze_followups(live_sales)
    

        st.success("Google Sheets connected successfully!")

        section(
            "Live Sales Records",
            f"{len(live_sales):,} records retrieved from Google Sheets"
        )

        if live_sales.empty:
            st.info("No live sales opportunities available.")

        else:
            search = st.text_input(
                "Search Opportunity ID",
                placeholder="Enter an opportunity ID",
                key="live_sales_search"
            )

            if search:
                live_sales = live_sales[
                    live_sales["Opportunity ID"]
                    .astype(str)
                    .str.contains(
                        search,
                        case=False,
                        regex=False,
                        na=False
                    )
                ]

            # Follow-up status filter
            st.subheader("Follow-up Monitoring")

            status_options = [
                "All",
                "Overdue",
                "Due Today",
                "Upcoming",
                "Scheduled Later",
                "Date Missing"
            ]

            selected_status = st.selectbox(
                "Filter by Follow-up Status",
                status_options,
                key="live_followup_filter"
            )

            if selected_status != "All":
                live_sales = live_sales[
                    live_sales["Follow-up Status"] == selected_status
                ]

            # Sales Priority Monitoring
            st.subheader("Sales Priority Monitoring")

            priority_options = [
                "All",
                "High",
                "Medium",
                "Low"
            ]

            selected_priority = st.selectbox(
                "Filter by Sales Priority",
                priority_options,
                key="live_priority_filter"
            )

            if selected_priority != "All":
                live_sales = live_sales[
                    live_sales["Sales Priority"]
                    .astype(str)
                    .str.strip()
                    .str.lower() == selected_priority.lower()
                ]

            display_columns = [
                "Opportunity ID",
                "Sales Agent",
                "Customer Account",
                "Product",
                "Deal Stage",
                "Deal Value",
                "Regional Office",
                "Sales Priority",
                "Next Follow-up Date",
                "Days Until Follow-up",
                "Follow-up Status"
            ]

            st.caption(
                f"Showing {len(live_sales):,} matching records"
            )

            # HTML table used because the interactive
            # dataframe did not render in the earlier test.
            if live_sales.empty:
                st.info(
                    "No sales opportunities match the selected filters."
                )
            else:
                table_html = live_sales[
                    display_columns
                ].to_html(
                    index=False,
                    escape=True
                )

                st.markdown(
                    table_html,
                    unsafe_allow_html=True
                )
            st.download_button(
                "Download Live Sales CSV",
                data=live_sales.to_csv(index=False).encode("utf-8"),
                file_name="revenueos_live_sales.csv",
                mime="text/csv",
                key="download_live_sales"
            )

    except Exception as error:
        st.error("Unable to load live sales data.")
        st.error(str(error))

# ==========================================================
# FOOTER
# ==========================================================

markup(
    '<div style="text-align:center;'
    'color:#8594AF;font-size:11px;'
    'border-top:1px solid #29354D;'
    'margin-top:42px;padding-top:20px">'
    'REVENUEOS · SALES INTELLIGENCE & DECISION PLATFORM'
    '<p>Historical portfolio case study · '
    'Experimental predictive analytics</p>'
    '</div>'
)
