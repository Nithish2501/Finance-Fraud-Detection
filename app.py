"""
Main Entry Point for AI-Powered Financial Fraud Detection System.
Streamlit application orchestrating multi-page routing, authentication, and state management.
"""

import sys
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import init_directories, DATABASE_PATH
from database.schema import init_db
from database import crud
from models.model_manager import get_model_manager
from authentication.auth import (
    init_session_state,
    is_authenticated,
    get_current_user,
    logout_user,
    seed_demo_user,
    authenticate_user,
    login_user
)
from dashboard.components import inject_custom_css

# Page modules
from pages import (
    home,
    dashboard,
    fraud_detection,
    transaction_history,
    analytics,
    model_performance,
    settings,
    about,
    api_docs,
    portal
)

# 1. Page Configuration (Must be first Streamlit call)
st.set_page_config(
    page_title="FraudSentinel AI — Financial Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. First-Run Graceful Setup
init_directories()
if not DATABASE_PATH.exists():
    init_db()
    seed_demo_user()

# 3. Inject CSS Styling
inject_custom_css()

# 4. Initialize Session State
init_session_state()

# Helper for programmatic navigation
def navigate_to(page_name: str) -> None:
    """Safely updates active navigation state and triggers rerun."""
    st.session_state["active_page"] = page_name
    st.session_state["main_nav_radio"] = page_name
    st.session_state["nav_pending_sync"] = True
    st.rerun()

# 5. Master Navigation Catalog
NAV_PAGES = [
    "Home",
    "Dashboard",
    "Fraud Detection",
    "Transaction History",
    "Analytics",
    "Model Performance",
    "REST API Docs",
    "Settings",
    "About",
    "Analyst Portal"
]

if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Home"

if st.session_state["active_page"] not in NAV_PAGES:
    st.session_state["active_page"] = "Home"

# Sync programmatic page updates if triggered externally
if st.session_state.get("nav_pending_sync"):
    st.session_state["main_nav_radio"] = st.session_state["active_page"]
    st.session_state["nav_pending_sync"] = False

if "main_nav_radio" not in st.session_state or st.session_state["main_nav_radio"] not in NAV_PAGES:
    st.session_state["main_nav_radio"] = st.session_state["active_page"]

# Sidebar Header Branding
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 0.4rem 0 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 1rem;">
        <div style="font-size: 2.2rem; margin-bottom: 0.2rem;">🛡️</div>
        <h2 style="margin: 0; font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em; color: #f8fafc;">
            FraudSentinel AI
        </h2>
        <div style="font-size: 0.72rem; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; margin-top: 0.2rem;">
            Enterprise Risk Intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# User Session Status Card in Sidebar
user = get_current_user()
auth_status = is_authenticated()

if auth_status and user:
    role_color = "#38bdf8" if user.get("role") == "admin" else "#34d399"
    st.sidebar.markdown(
        f"""
        <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 10px; padding: 0.75rem 0.9rem; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.72rem; color: #94a3b8; font-weight: 700; letter-spacing: 0.05em;">ACTIVE OPERATOR</span>
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #10b981; display: inline-block;"></span>
            </div>
            <div style="font-weight: 700; color: #f8fafc; font-size: 0.95rem; margin-top: 0.2rem;">👤 {user.get('username')}</div>
            <div style="font-size: 0.75rem; color: {role_color}; text-transform: uppercase; font-weight: 600;">Role: {user.get('role', 'analyst')}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        """
        <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 10px; padding: 0.75rem 0.9rem; margin-bottom: 1rem;">
            <div style="font-size: 0.74rem; color: #f59e0b; font-weight: 700; letter-spacing: 0.05em;">GUEST SURVEILLANCE MODE</div>
            <div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 0.2rem;">Sign in via Analyst Portal to edit rules and manage credentials.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Callback for smooth navigation
def on_menu_selection_change():
    st.session_state["active_page"] = st.session_state["main_nav_radio"]

selected_page = st.sidebar.radio(
    "Navigation Menu",
    NAV_PAGES,
    key="main_nav_radio",
    on_change=on_menu_selection_change
)

# Keep active_page in sync
st.session_state["active_page"] = selected_page

# Live System Telemetry in Sidebar
st.sidebar.markdown("---")
model_mgr = get_model_manager()
model_status_label = "🟢 Ready" if model_mgr.is_model_trained() else "🟡 Untrained"
tx_stats = crud.get_transaction_stats()
total_tx_count = tx_stats.get("total_count", 0)

st.sidebar.markdown(
    f"""
    <div style="font-size: 0.76rem; color: #94a3b8; line-height: 1.6; margin-bottom: 0.8rem;">
        <div><b>Database:</b> <span style="color: #34d399;">SQLite (Active)</span></div>
        <div><b>ML Engine:</b> <span style="color: #60a5fa;">{model_status_label}</span></div>
        <div><b>Audit Ledger:</b> <span style="color: #cbd5e1;">{total_tx_count:,} records</span></div>
    </div>
    """,
    unsafe_allow_html=True
)

# Quick Action Buttons in Sidebar
if auth_status:
    if st.sidebar.button("🚪 Sign Out", use_container_width=True):
        logout_user()
        navigate_to("Home")
else:
    if st.sidebar.button("⚡ 1-Click Demo Login", use_container_width=True, type="primary"):
        success, msg, user_data = authenticate_user("demo_analyst", "Demo@12345")
        if success and user_data:
            login_user(user_data)
            navigate_to("Dashboard")

# 6. Page Routing Execution
active = st.session_state.get("active_page", "Home")

if active == "Home":
    home.render()
elif active == "Dashboard":
    dashboard.render()
elif active == "Fraud Detection":
    fraud_detection.render()
elif active == "Transaction History":
    transaction_history.render()
elif active == "Analytics":
    analytics.render()
elif active == "Model Performance":
    model_performance.render()
elif active == "REST API Docs":
    api_docs.render()
elif active == "Settings":
    settings.render()
elif active == "About":
    about.render()
elif active == "Analyst Portal":
    portal.render()
else:
    home.render()
