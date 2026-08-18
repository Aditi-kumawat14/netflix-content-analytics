import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Netflix Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONSTANTS
# ============================================================

RED = "#E50914"
DARK_RED = "#B20710"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "netflix_cleaned1.csv",
        encoding="utf-8"
    )

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # Date
    if "date_added" in df.columns:

        df["date_added"] = pd.to_datetime(
            df["date_added"],
            errors="coerce"
        )

    # Year added
    if "year_added" not in df.columns:

        if "date_added" in df.columns:

            df["year_added"] = (
                df["date_added"]
                .dt.year
            )

    # Release year
    if "release_year" in df.columns:

        df["release_year"] = pd.to_numeric(
            df["release_year"],
            errors="coerce"
        )

    return df


df = load_data()


# ============================================================
# CHECK DATA
# ============================================================

if "title" not in df.columns or "type" not in df.columns:

    st.error(
        """
        Your dataset must contain at least:

        - title
        - type
        """
    )

    st.stop()


# ============================================================
# GLOBAL CSS
# ============================================================

st.html(
    f"""
    <style>

    /* ========================================================
       FONT AWESOME
       ======================================================== */

    @import url(
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css"
    );


    /* ========================================================
       GENERAL
       ======================================================== */

    .netflix-header {{
        padding: 10px 0 25px 0;
        margin-bottom: 25px;

        border-bottom:
            1px solid
            rgba(128,128,128,0.25);
    }}


    .brand {{
        font-size: 38px;
        font-weight: 900;
        letter-spacing: -1px;
        line-height: 1.1;
    }}


    .brand-red {{
        color: {RED};
    }}


    .brand-normal {{
        color: inherit;
    }}


    .subtitle {{
        margin-top: 8px;
        font-size: 15px;
        opacity: 0.65;
    }}


    /* ========================================================
       KPI CARDS
       ======================================================== */

    .kpi-container {{
        display: flex;
        flex-direction: column;

        min-height: 150px;

        padding: 20px;

        border-radius: 14px;

        background:
            rgba(128,128,128,0.08);

        border:
            1px solid
            rgba(128,128,128,0.20);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }}


    .kpi-container:hover {{
        transform: translateY(-3px);

        border-color:
            {RED};
    }}


    .kpi-icon {{
        font-size: 26px;
        margin-bottom: 10px;
    }}


    .kpi-label {{
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;

        opacity: 0.60;
    }}


    .kpi-value {{
        font-size: 30px;
        font-weight: 800;

        margin-top: 5px;
    }}


    .kpi-description {{
        font-size: 12px;

        color: {RED};

        margin-top: 5px;
    }}


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {{
        font-size: 23px;
        font-weight: 750;

        margin-top: 30px;
        margin-bottom: 15px;
    }}


    .section-icon {{
        color: {RED};
    }}


    /* ========================================================
       INSIGHT CARDS
       ======================================================== */

    .insight-card {{
        padding: 18px;

        margin-bottom: 15px;

        border-radius: 12px;

        background:
            rgba(128,128,128,0.08);

        border:
            1px solid
            rgba(128,128,128,0.18);

        border-left:
            4px solid
            {RED};
    }}


    .insight-title {{
        font-size: 16px;
        font-weight: 700;
    }}


    .insight-text {{
        margin-top: 7px;

        font-size: 14px;

        line-height: 1.6;

        opacity: 0.70;
    }}


    /* ========================================================
       ABOUT CARD
       ======================================================== */

    .about-card {{
        padding: 25px;

        border-radius: 14px;

        background:
            rgba(128,128,128,0.08);

        border:
            1px solid
            rgba(128,128,128,0.18);
    }}


    /* ========================================================
       PREMIUM SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {{

        border-right:
            1px solid
            rgba(128,128,128,0.16);

        background:
            transparent;
    }}


    [data-testid="stSidebar"] > div:first-child {{

        padding-top: 1rem;

        padding-left: 0.65rem;

        padding-right: 0.65rem;
    }}


    /* ========================================================
       SIDEBAR BRAND
       ======================================================== */

    .sidebar-brand {{

        padding:
            5px
            7px
            20px
            7px;
    }}


    .sidebar-brand-top {{

        display: flex;

        align-items: center;

        gap: 13px;
    }}


    /* Netflix N */

    .sidebar-logo-mark {{

        width: 42px;

        height: 47px;

        display: flex;

        align-items: center;

        justify-content: center;

        color: {RED};

        font-size: 43px;

        font-weight: 950;

        line-height: 1;

        border-left:
            3px solid
            {RED};

        letter-spacing: -5px;

        text-shadow:
            0 0 12px
            rgba(229,9,20,0.15);
    }}


    .sidebar-brand-text {{

        display: flex;

        flex-direction: column;
    }}


    .sidebar-brand-name {{

        font-size: 17px;

        font-weight: 850;

        letter-spacing: 1.8px;

        line-height: 1;
    }}


    .sidebar-brand-product {{

        color: {RED};

        font-size: 9px;

        font-weight: 750;

        letter-spacing: 2.8px;

        margin-top: 7px;
    }}


    /* ========================================================
       SIDEBAR STATUS
       ======================================================== */

    .sidebar-status {{

        display: flex;

        align-items: center;

        gap: 7px;

        margin-top: 15px;

        font-size: 8px;

        font-weight: 700;

        letter-spacing: 1.4px;

        opacity: 0.40;
    }}


    .status-dot {{

        width: 6px;

        height: 6px;

        border-radius: 50%;

        background: {RED};

        box-shadow:
            0 0 8px
            rgba(229,9,20,0.7);
    }}


    /* ========================================================
       NAVIGATION HEADING
       ======================================================== */

    .sidebar-nav-heading {{

        margin:
            4px
            8px
            9px
            8px;

        font-size: 9px;

        font-weight: 800;

        letter-spacing: 2px;

        opacity: 0.38;
    }}


    /* ========================================================
       RADIO CONTAINER
       ======================================================== */

    [data-testid="stSidebar"]
    [data-testid="stRadio"] {{

        gap: 3px;
    }}


    /* ========================================================
       HIDE RADIO CIRCLE
       ======================================================== */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label > div:first-child {{

        display: none;
    }}


    /* ========================================================
       NAVIGATION ITEMS
       ======================================================== */

    [data-testid="stSidebar"]
    [data-testid="stRadio"] label {{

        position: relative;

        display: flex;

        align-items: center;

        min-height: 40px;

        padding:
            5px
            10px
            5px
            43px;

        margin:
            2px
            0;

        border-radius: 9px;

        cursor: pointer;

        transition:
            background 0.2s ease,
            transform 0.2s ease;
    }}


    /* ========================================================
       NAVIGATION TEXT
       ======================================================== */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label p {{

        margin: 0;

        font-size: 13px;

        font-weight: 550;

        letter-spacing: 0.1px;

        transition:
            color 0.2s ease;
    }}


    /* ========================================================
       FONT AWESOME ICONS
       ======================================================== */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label::before {{

        position: absolute;

        left: 16px;

        width: 20px;

        text-align: center;

        font-family:
            "Font Awesome 6 Free";

        font-weight: 900;

        font-size: 14px;

        opacity: 0.55;

        transition:
            color 0.2s ease,
            transform 0.2s ease;
    }}


    /* Dashboard */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:nth-child(1)::before {{

        content: "\\f3fd";
    }}


    /* Trends */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:nth-child(2)::before {{

        content: "\\f201";
    }}


    /* Content Analysis */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:nth-child(3)::before {{

        content: "\\f200";
    }}


    /* Ratings */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:nth-child(4)::before {{

        content: "\\f005";
    }}


    /* Countries */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:nth-child(5)::before {{

        content: "\\f57d";
    }}


    /* Explore */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:nth-child(6)::before {{

        content: "\\f002";
    }}


    /* Insights */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:nth-child(7)::before {{

        content: "\\f0eb";
    }}


    /* About */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:nth-child(8)::before {{

        content: "\\f05a";
    }}


    /* ========================================================
       HOVER
       ======================================================== */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:hover {{

        background:
            rgba(229,9,20,0.065);

        transform:
            translateX(3px);
    }}


    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:hover::before {{

        color: {RED};

        opacity: 1;

        transform:
            scale(1.08);
    }}


    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:hover p {{

        color: {RED};
    }}


    /* ========================================================
       ACTIVE ITEM
       ======================================================== */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:has(input:checked) {{

        background:
            linear-gradient(
                90deg,
                rgba(229,9,20,0.13),
                rgba(229,9,20,0.035)
            );
    }}


    /* Active red bar */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:has(input:checked)::after {{

        content: "";

        position: absolute;

        left: 0;

        top: 6px;

        bottom: 6px;

        width: 3px;

        border-radius:
            0 4px 4px 0;

        background: {RED};

        box-shadow:
            0 0 8px
            rgba(229,9,20,0.45);
    }}


    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:has(input:checked)::before {{

        color: {RED};

        opacity: 1;

        transform:
            scale(1.05);
    }}


    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:has(input:checked) p {{

        color: {RED};

        font-weight: 700;
    }}


    /* ========================================================
       DIVIDER
       ======================================================== */

    .sidebar-divider {{

        height: 1px;

        margin:
            18px
            5px;

        background:
            rgba(128,128,128,0.16);
    }}


    /* ========================================================
       DATASET HEADING
       ======================================================== */

    .sidebar-dataset-heading {{

        margin:
            0
            8px
            9px
            8px;

        font-size: 9px;

        font-weight: 800;

        letter-spacing: 2px;

        opacity: 0.38;
    }}


    /* ========================================================
       DATASET CARD
       ======================================================== */

    .sidebar-dataset-card {{

        display: flex;

        align-items: center;

        gap: 11px;

        padding: 12px;

        margin:
            0
            3px;

        border-radius: 10px;

        background:
            rgba(128,128,128,0.055);

        border:
            1px solid
            rgba(128,128,128,0.13);

        transition:
            all 0.2s ease;
    }}


    .sidebar-dataset-card:hover {{

        border-color:
            rgba(229,9,20,0.35);

        background:
            rgba(229,9,20,0.045);
    }}


    .dataset-icon {{

        width: 31px;

        height: 31px;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 8px;

        color: {RED};

        background:
            rgba(229,9,20,0.10);

        font-size: 17px;

        font-weight: 800;
    }}


    .dataset-content {{

        display: flex;

        flex-direction: column;
    }}


    .dataset-title {{

        font-size: 11px;

        font-weight: 700;
    }}


    .dataset-description {{

        font-size: 9px;

        margin-top: 3px;

        opacity: 0.45;
    }}


    /* ========================================================
       SIDEBAR FOOTER
       ======================================================== */

    .sidebar-footer {{

        margin-top: 22px;

        padding:
            0
            6px
            8px
            6px;

        text-align: center;
    }}


    .sidebar-footer-line {{

        width: 28px;

        height: 2px;

        margin:
            0
            auto
            10px;

        background: {RED};

        border-radius: 2px;
    }}


    .sidebar-footer-text {{

        font-size: 7px;

        font-weight: 750;

        letter-spacing: 1.5px;

        opacity: 0.30;
    }}


    .sidebar-footer-tech {{

        font-size: 6px;

        letter-spacing: 0.8px;

        margin-top: 6px;

        opacity: 0.20;
    }}


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {{

        text-align: center;

        padding: 45px 0 15px 0;

        font-size: 12px;

        opacity: 0.45;
    }}


    .footer-logo {{

        color: {RED};

        font-size: 25px;

        margin-bottom: 5px;
    }}

    </style>
    """
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def html_card(
    icon,
    title,
    value,
    description
):

    st.html(
        f"""
        <div class="kpi-container">

            <div class="kpi-icon">
                {icon}
            </div>

            <div class="kpi-label">
                {title}
            </div>

            <div class="kpi-value">
                {value}
            </div>

            <div class="kpi-description">
                {description}
            </div>

        </div>
        """
    )


def section_title(
    icon,
    title
):

    st.html(
        f"""
        <div class="section-title">

            <span class="section-icon">
                {icon}
            </span>

            {title}

        </div>
        """
    )


def chart_style(fig):

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=30
        ),

        font=dict(
            size=12
        ),

        title=dict(
            font=dict(
                size=16
            )
        )

    )

    return fig


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.html(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-top">

                <div class="sidebar-logo-mark">
                    N
                </div>

                <div class="sidebar-brand-text">

                    <div class="sidebar-brand-name">
                        NETFLIX
                    </div>

                    <div class="sidebar-brand-product">
                        ANALYTICS
                    </div>

                </div>

            </div>


            <div class="sidebar-status">

                <span class="status-dot"></span>

                CONTENT INTELLIGENCE

            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # NAVIGATION HEADING
    # --------------------------------------------------------

    st.html(
        """
        <div class="sidebar-nav-heading">
            EXPLORE
        </div>
        """
    )


    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Trends",
            "Content Analysis",
            "Ratings",
            "Countries",
            "Explore Titles",
            "Key Insights",
            "About Project"
        ],
        label_visibility="collapsed"
    )


    # --------------------------------------------------------
    # SIDEBAR DIVIDER
    # --------------------------------------------------------

    st.html(
        """
        <div class="sidebar-divider"></div>
        """
    )


    # --------------------------------------------------------
    # DATASET INFORMATION
    # --------------------------------------------------------

    st.html(
        """
        <div class="sidebar-dataset-heading">
            DATASET
        </div>


        <div class="sidebar-dataset-card">

            <div class="dataset-icon">
                <i class="fa-solid fa-database"></i>
            </div>

            <div class="dataset-content">

                <div class="dataset-title">
                    Netflix Library
                </div>

                <div class="dataset-description">
                    Movies & TV Shows
                </div>

            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # SIDEBAR FOOTER
    # --------------------------------------------------------

    st.html(
        """
        <div class="sidebar-footer">

            <div class="sidebar-footer-line"></div>

            <div class="sidebar-footer-text">
                DATA ANALYTICS DASHBOARD
            </div>

            <div class="sidebar-footer-tech">
                PYTHON&nbsp;&nbsp;•&nbsp;&nbsp;PANDAS&nbsp;&nbsp;•&nbsp;&nbsp;PLOTLY
            </div>

        </div>
        """
    )


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="netflix-header">

        <div class="brand">

            <span class="brand-red">
                NETFLIX
            </span>

            <span class="brand-normal">
                ANALYTICS
            </span>

        </div>

        <div class="subtitle">
            Explore the Netflix Content Library
        </div>

    </div>
    """
)


# ============================================================
# BASIC DATA
# ============================================================

total_titles = df["title"].nunique()

movie_count = (
    df["type"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("movie")
    .sum()
)

tv_count = (
    df["type"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("tv show")
    .sum()
)

movie_percentage = (
    movie_count / total_titles * 100
    if total_titles > 0
    else 0
)

tv_percentage = (
    tv_count / total_titles * 100
    if total_titles > 0
    else 0
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        html_card(
            "🎬",
            "Total Titles",
            f"{total_titles:,}",
            "Movies + TV Shows"
        )

    with c2:

        html_card(
            "🎥",
            "Movies",
            f"{movie_count:,}",
            f"{movie_percentage:.1f}% of library"
        )

    with c3:

        html_card(
            "📺",
            "TV Shows",
            f"{tv_count:,}",
            f"{tv_percentage:.1f}% of library"
        )

    with c4:

        if "release_year" in df.columns:

            release_years = (
                pd.to_numeric(
                    df["release_year"],
                    errors="coerce"
                )
                .dropna()
            )

            if len(release_years) > 0:

                latest_release = int(
                    release_years.max()
                )

            else:

                latest_release = "N/A"

        else:

            latest_release = "N/A"

        html_card(
            "📅",
            "Latest Release",
            latest_release,
            "Most recent release year"
        )


    # --------------------------------------------------------
    # TREND
    # --------------------------------------------------------

    section_title(
        "📈",
        "Titles Added Over Time"
    )

    col1, col2 = st.columns(
        [2, 1]
    )


    # --------------------------------------------------------
    # TITLES ADDED
    # --------------------------------------------------------

    with col1:

        if "year_added" in df.columns:

            yearly = (
                df
                .dropna(
                    subset=["year_added"]
                )
                .groupby("year_added")
                .size()
                .reset_index(
                    name="Titles"
                )
            )

            yearly["year_added"] = (
                pd.to_numeric(
                    yearly["year_added"],
                    errors="coerce"
                )
            )

            yearly = yearly.dropna()

            fig = px.area(
                yearly,
                x="year_added",
                y="Titles",
                markers=True,
                title="Titles Added by Year"
            )

            fig.update_traces(
                line_color=RED,
                marker_color=RED,
                fillcolor="rgba(229,9,20,0.15)"
            )

            fig = chart_style(fig)

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info(
                "year_added column is not available."
            )


    # --------------------------------------------------------
    # MOVIES VS TV SHOWS
    # --------------------------------------------------------

    with col2:

        type_data = (
            df["type"]
            .value_counts()
            .reset_index()
        )

        type_data.columns = [
            "Type",
            "Count"
        ]

        fig = px.pie(
            type_data,
            names="Type",
            values="Count",
            hole=0.55,
            title="Movies vs TV Shows"
        )

        fig = chart_style(fig)

        st.plotly_chart(
            fig,
            width="stretch"
        )


    # --------------------------------------------------------
    # THREE CHARTS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # COUNTRIES
    # --------------------------------------------------------

    with col1:

        if "country" in df.columns:

            country_data = (
                df["country"]
                .dropna()
                .astype(str)
                .str.split(", ")
                .explode()
                .value_counts()
                .head(10)
                .sort_values()
                .reset_index()
            )

            country_data.columns = [
                "Country",
                "Titles"
            ]

            fig = px.bar(
                country_data,
                x="Titles",
                y="Country",
                orientation="h",
                title="Top Countries"
            )

            fig.update_traces(
                marker_color=RED
            )

            fig = chart_style(fig)

            st.plotly_chart(
                fig,
                width="stretch"
            )


    # --------------------------------------------------------
    # RATINGS
    # --------------------------------------------------------

    with col2:

        if "rating" in df.columns:

            rating_data = (
                df["rating"]
                .dropna()
                .astype(str)
                .value_counts()
                .head(10)
                .reset_index()
            )

            rating_data.columns = [
                "Rating",
                "Titles"
            ]

            fig = px.bar(
                rating_data,
                x="Rating",
                y="Titles",
                title="Top Ratings"
            )

            fig.update_traces(
                marker_color=RED
            )

            fig = chart_style(fig)

            st.plotly_chart(
                fig,
                width="stretch"
            )


    # --------------------------------------------------------
    # GENRES
    # --------------------------------------------------------

    with col3:

        if "listed_in" in df.columns:

            genre_data = (
                df["listed_in"]
                .dropna()
                .astype(str)
                .str.split(", ")
                .explode()
                .value_counts()
                .head(8)
                .reset_index()
            )

            genre_data.columns = [
                "Genre",
                "Titles"
            ]

            fig = px.pie(
                genre_data,
                names="Genre",
                values="Titles",
                hole=0.55,
                title="Top Genres"
            )

            fig = chart_style(fig)

            st.plotly_chart(
                fig,
                width="stretch"
            )


    # --------------------------------------------------------
    # QUICK SEARCH
    # --------------------------------------------------------

    section_title(
        "🔎",
        "Quick Explore"
    )

    search = st.text_input(
        "Search Netflix titles",
        placeholder="Search for a title...",
        label_visibility="collapsed"
    )

    if search:

        search_columns = [
            "title",
            "director",
            "cast",
            "country",
            "listed_in",
            "description"
        ]

        search_columns = [
            column
            for column in search_columns
            if column in df.columns
        ]

        mask = pd.Series(
            False,
            index=df.index
        )

        for column in search_columns:

            mask = (
                mask |
                df[column]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            )

        results = df[mask]

        st.write(
            f"**{len(results):,}** results found"
        )

        st.dataframe(
            results.head(50),
            width="stretch",
            hide_index=True
        )


# ============================================================
# TRENDS
# ============================================================

elif page == "Trends":

    section_title(
        "📈",
        "Netflix Content Trends"
    )

    if "year_added" not in df.columns:

        st.warning(
            "year_added column is not available."
        )

    else:

        trend_type = st.selectbox(
            "Select Content Type",
            [
                "All",
                "Movie",
                "TV Show"
            ]
        )

        trend_df = df.copy()

        if trend_type != "All":

            trend_df = trend_df[
                trend_df["type"]
                .astype(str)
                .str.strip()
                .str.lower()
                ==
                trend_type.lower()
            ]

        yearly = (
            trend_df
            .dropna(
                subset=["year_added"]
            )
            .groupby("year_added")
            .size()
            .reset_index(
                name="Titles"
            )
        )

        fig = px.line(
            yearly,
            x="year_added",
            y="Titles",
            markers=True,
            title=f"Titles Added — {trend_type}"
        )

        fig.update_traces(
            line_color=RED,
            marker_color=RED,
            line_width=3
        )

        fig = chart_style(fig)

        st.plotly_chart(
            fig,
            width="stretch"
        )


# ============================================================
# CONTENT ANALYSIS
# ============================================================

elif page == "Content Analysis":

    section_title(
        "🎭",
        "Content Analysis"
    )

    c1, c2 = st.columns(2)

    with c1:

        html_card(
            "🎥",
            "Movies",
            f"{movie_count:,}",
            "Movies available"
        )

    with c2:

        html_card(
            "📺",
            "TV Shows",
            f"{tv_count:,}",
            "TV Shows available"
        )


    # --------------------------------------------------------
    # MOVIE DURATION
    # --------------------------------------------------------

    if "duration" in df.columns:

        section_title(
            "⏱️",
            "Movie Duration Distribution"
        )

        movie_duration = df[
            df["type"]
            .astype(str)
            .str.lower()
            .eq("movie")
        ].copy()

        movie_duration["duration_number"] = (
            movie_duration["duration"]
            .astype(str)
            .str.extract(
                r"(\d+)"
            )[0]
        )

        movie_duration[
            "duration_number"
        ] = pd.to_numeric(
            movie_duration[
                "duration_number"
            ],
            errors="coerce"
        )

        movie_duration = movie_duration.dropna(
            subset=["duration_number"]
        )

        if len(movie_duration) > 0:

            fig = px.histogram(
                movie_duration,
                x="duration_number",
                nbins=40,
                title="Movie Duration in Minutes"
            )

            fig.update_traces(
                marker_color=RED
            )

            fig = chart_style(fig)

            st.plotly_chart(
                fig,
                width="stretch"
            )


# ============================================================
# RATINGS
# ============================================================

elif page == "Ratings":

    section_title(
        "⭐",
        "Netflix Ratings"
    )

    if "rating" not in df.columns:

        st.warning(
            "rating column is not available."
        )

    else:

        rating_data = (
            df["rating"]
            .dropna()
            .astype(str)
            .value_counts()
            .reset_index()
        )

        rating_data.columns = [
            "Rating",
            "Titles"
        ]

        fig = px.bar(
            rating_data,
            x="Rating",
            y="Titles",
            title="Rating Distribution"
        )

        fig.update_traces(
            marker_color=RED
        )

        fig = chart_style(fig)

        st.plotly_chart(
            fig,
            width="stretch"
        )


# ============================================================
# COUNTRIES
# ============================================================

elif page == "Countries":

    section_title(
        "🌍",
        "Netflix Countries"
    )

    if "country" not in df.columns:

        st.warning(
            "country column is not available."
        )

    else:

        country_data = (
            df["country"]
            .dropna()
            .astype(str)
            .str.split(", ")
            .explode()
            .value_counts()
            .head(15)
            .sort_values()
            .reset_index()
        )

        country_data.columns = [
            "Country",
            "Titles"
        ]

        fig = px.bar(
            country_data,
            x="Titles",
            y="Country",
            orientation="h",
            title="Top 15 Countries"
        )

        fig.update_traces(
            marker_color=RED
        )

        fig = chart_style(fig)

        st.plotly_chart(
            fig,
            width="stretch"
        )


# ============================================================
# EXPLORE TITLES
# ============================================================

elif page == "Explore Titles":

    section_title(
        "🔎",
        "Explore Netflix Titles"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        search = st.text_input(
            "Search Title",
            placeholder="e.g. Stranger Things"
        )

    with col2:

        type_filter = st.selectbox(
            "Content Type",
            [
                "All",
                "Movie",
                "TV Show"
            ]
        )

    with col3:

        if "rating" in df.columns:

            rating_options = (
                df["rating"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            rating_options.sort()

            rating_filter = st.selectbox(
                "Rating",
                ["All"] + rating_options
            )

        else:

            rating_filter = "All"


    filtered = df.copy()


    # Search
    if search:

        filtered = filtered[
            filtered["title"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    # Type
    if type_filter != "All":

        filtered = filtered[
            filtered["type"]
            .astype(str)
            .str.lower()
            ==
            type_filter.lower()
        ]


    # Rating
    if (
        rating_filter != "All"
        and "rating" in filtered.columns
    ):

        filtered = filtered[
            filtered["rating"]
            .astype(str)
            ==
            rating_filter
        ]


    st.html(
        f"""
        <div style="
            margin:20px 0;
            font-size:14px;
            opacity:0.65;
        ">

            Showing

            <span style="
                color:{RED};
                font-size:22px;
                font-weight:800;
            ">
                {len(filtered):,}
            </span>

            titles

        </div>
        """
    )


    st.dataframe(
        filtered,
        width="stretch",
        hide_index=True
    )


    # Download
    csv_data = filtered.to_csv(
        index=False
    )

    st.download_button(
        "⬇️ Download Filtered Data",
        data=csv_data,
        file_name="netflix_filtered.csv",
        mime="text/csv",
        width="stretch"
    )


# ============================================================
# KEY INSIGHTS
# ============================================================

elif page == "Key Insights":

    section_title(
        "💡",
        "Key Insights"
    )


    # --------------------------------------------------------
    # CONTENT MIX
    # --------------------------------------------------------

    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                🎬 Content Mix
            </div>

            <div class="insight-text">

                Movies represent approximately

                <b style="
                    color:{RED};
                    font-size:16px;
                ">
                    {movie_percentage:.1f}%
                </b>

                of all titles in this dataset.

            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # MOST COMMON RATING
    # --------------------------------------------------------

    if "rating" in df.columns:

        ratings = (
            df["rating"]
            .dropna()
            .astype(str)
            .value_counts()
        )

        if len(ratings) > 0:

            common_rating = ratings.index[0]

            st.html(
                f"""
                <div class="insight-card">

                    <div class="insight-title">
                        ⭐ Most Common Rating
                    </div>

                    <div class="insight-text">

                        The most frequently occurring
                        rating is

                        <b style="
                            color:{RED};
                            font-size:16px;
                        ">
                            {common_rating}
                        </b>.

                    </div>

                </div>
                """
            )


    # --------------------------------------------------------
    # PEAK YEAR
    # --------------------------------------------------------

    if "year_added" in df.columns:

        yearly = (
            df
            .dropna(
                subset=["year_added"]
            )
            .groupby("year_added")
            .size()
        )

        if len(yearly) > 0:

            peak_year = int(
                yearly.idxmax()
            )

            peak_count = int(
                yearly.max()
            )

            st.html(
                f"""
                <div class="insight-card">

                    <div class="insight-title">
                        📈 Peak Content Addition
                    </div>

                    <div class="insight-text">

                        The highest number of titles
                        were added in

                        <b style="
                            color:{RED};
                            font-size:16px;
                        ">
                            {peak_year}
                        </b>

                        with

                        <b style="
                            color:{RED};
                            font-size:16px;
                        ">
                            {peak_count:,}
                        </b>

                        titles.

                    </div>

                </div>
                """
            )


    # --------------------------------------------------------
    # DATASET SIZE
    # --------------------------------------------------------

    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                📊 Dataset Size
            </div>

            <div class="insight-text">

                The cleaned dataset contains

                <b style="
                    color:{RED};
                    font-size:16px;
                ">
                    {len(df):,}
                </b>

                rows.

            </div>

        </div>
        """
    )


# ============================================================
# ABOUT
# ============================================================

elif page == "About Project":

    section_title(
        "ℹ️",
        "About Project"
    )

    st.html(
        f"""
        <div class="about-card">

            <h2 style="
                color:{RED};
                margin-top:0;
            ">
                🎬 Netflix Content Analytics
            </h2>


            <p style="
                line-height:1.7;
                opacity:0.70;
            ">

                An interactive data analytics dashboard
                created to explore the Netflix Movies
                and TV Shows content library.

            </p>


            <hr>


            <h4>
                🛠️ Technologies
            </h4>

            <p style="opacity:0.70;">

                Python • Pandas • Plotly • Streamlit

            </p>


            <h4>
                📊 Data Analysis
            </h4>

            <p style="
                opacity:0.70;
                line-height:1.8;
            ">

                ✓ Data Cleaning<br>
                ✓ Exploratory Data Analysis<br>
                ✓ Data Visualization<br>
                ✓ Interactive Filtering<br>
                ✓ Search<br>
                ✓ Statistical Insights

            </p>


            <h4>
                ✨ Dashboard Features
            </h4>

            <p style="
                opacity:0.70;
                line-height:1.8;
            ">

                ✓ Dashboard<br>
                ✓ KPI Cards<br>
                ✓ Trends<br>
                ✓ Content Analysis<br>
                ✓ Ratings<br>
                ✓ Countries<br>
                ✓ Explore Titles<br>
                ✓ Key Insights<br>
                ✓ Data Download

            </p>

        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    f"""
    <div class="footer">

        <div class="footer-logo">
            N
        </div>

        <div style="
            font-size:14px;
            font-weight:700;
            margin-bottom:5px;
        ">
            Netflix Analytics Dashboard
        </div>

        <div style="
            font-size:11px;
            opacity:0.65;
        ">
            Built with Python • Pandas • Plotly • Streamlit
        </div>

        <div style="
            margin-top:10px;
            font-size:12px;
            opacity:0.65;
        ">
            Created by
            <span style="
                color:{RED};
                font-weight:700;
            ">
                Aditi Kumawat
            </span>
        </div>

    </div>
    """
)