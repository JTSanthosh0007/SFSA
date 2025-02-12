import streamlit as st
from statement_parser import StatementParser
from auth import show_login_page, logout_user
from platform_selector import PlatformSelector, check_platform_selected
from platforms.router import route_to_platform
import time

# Must be the first Streamlit command
st.set_page_config(
    page_title="Statement Analyzer",
    page_icon="💰",
    layout="wide"
)

# Add this after set_page_config
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Responsive container */
            .main-container {
                max-width: 100% !important;
                padding: 0 1rem;
            }
            
            /* Make sure content doesn't get hidden under footer */
            .main .block-container {
                padding-bottom: 5rem;
                margin-bottom: 0;
            }
            
            /* Adjust for mobile screens */
            @media (max-width: 768px) {
                .main .block-container {
                    padding: 2rem 0.5rem 7rem 0.5rem;
                }
                
                /* Make text more readable on mobile */
                .stMarkdown {
                    font-size: 16px !important;
                }
                
                /* Adjust button sizes for mobile */
                .stButton button {
                    padding: 0.5rem !important;
                    font-size: 14px !important;
                }
            }
            
            /* Keep content from touching edges */
            .stApp {
                margin: 0 auto;
                max-width: 1200px;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Add global dark theme CSS
st.markdown("""
    <style>
    /* Global dark theme */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* Style for all containers */
    .stMarkdown, .stText, div[data-testid="stVerticalBlock"] {
        color: #ffffff;
    }
    
    /* Style for text inputs */
    .stTextInput input {
        background-color: #2d2d2d;
        color: #ffffff;
        border-color: #404040;
    }
    
    /* Style for buttons */
    .stButton button {
        background-color: #2d2d2d;
        color: #ffffff;
        border-color: #404040;
    }
    
    /* Style for success messages */
    .stSuccess {
        background-color: rgba(40, 167, 69, 0.2);
        color: #ffffff;
    }
    
    /* Style for error messages */
    .stError {
        background-color: rgba(220, 53, 69, 0.2);
        color: #ffffff;
    }
    
    /* Style for info messages */
    .stInfo {
        background-color: rgba(0, 123, 255, 0.2);
        color: #ffffff;
    }
    
    /* Style for warnings */
    .stWarning {
        background-color: rgba(255, 193, 7, 0.2);
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Add custom CSS for footer and buttons
st.markdown("""
    <style>
    /* Footer container */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #1a1a1a;
        padding: 10px 15px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        z-index: 999;
    }
    
    /* Button container within footer */
    .footer-buttons {
        display: flex;
        gap: 20px;
        align-items: center;
        justify-content: center;
    }
    
    /* Style for footer buttons */
    .footer .stButton button {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        border-radius: 8px;
        min-width: auto !important;
        height: auto !important;
        line-height: 1.2 !important;
        border: 1px solid #404040 !important;
    }
    
    /* Platform selector adjustments */
    .platform-selector {
        position: sticky;
        top: 0;
        background-color: #1a1a1a;
        padding: 10px;
        z-index: 1000;
        border-bottom: 1px solid #404040;
    }
    
    .platform-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 8px;
        max-width: 100%;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .footer {
            padding: 8px;
        }
        
        .footer-buttons {
            gap: 10px;
        }
        
        .footer .stButton button {
            padding: 8px 12px !important;
            font-size: 14px !important;
        }
        
        .platform-grid {
            grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
        }
    }
    
    /* Make sure content is visible above footer */
    .stApp > div:nth-child(1) {
        padding-bottom: 80px;
    }
    </style>
""", unsafe_allow_html=True)

# Update the platform selector CSS for better mobile display
st.markdown("""
    <style>
    /* Platform selector container */
    .platform-selector {
        position: fixed;
        top: 0;
        right: 0;
        padding: 10px;
        background-color: #1a1a1a;
        z-index: 1000;
        border-bottom-left-radius: 10px;
        box-shadow: -2px 2px 5px rgba(0,0,0,0.2);
        width: 100%;  /* Full width on mobile */
        max-width: 400px;  /* Max width on desktop */
    }
    
    /* Platform buttons grid */
    .platform-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
        gap: 8px;
        width: 100%;
    }
    
    /* Platform button style */
    .stButton button {
        width: 100%;
        background-color: #2d2d2d !important;
        border: 1px solid #404040 !important;
        color: #ffffff !important;
        padding: 8px 5px !important;
        font-size: 12px !important;
        transition: all 0.3s ease !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .platform-selector {
            position: sticky;  /* Change to sticky on mobile */
            right: auto;
            border-radius: 0;
            max-width: 100%;
        }
        
        .platform-grid {
            grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
        }
        
        .stButton button {
            font-size: 11px !important;
            padding: 6px 3px !important;
        }
        
        /* Adjust main content padding */
        .main .block-container {
            padding-top: 80px !important;  /* Space for platform selector */
        }
        
        /* Make title and text more mobile-friendly */
        h1 {
            font-size: 24px !important;
            margin-top: 0 !important;
        }
        
        h3 {
            font-size: 18px !important;
        }
        
        p {
            font-size: 14px !important;
        }
    }
    
    /* Improve footer on mobile */
    @media (max-width: 768px) {
        .footer {
            padding: 5px !important;
        }
        
        .footer .stButton button {
            padding: 6px 10px !important;
            font-size: 12px !important;
            min-width: 70px !important;
        }
        
        .footer-buttons {
            gap: 5px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Add this after your existing CSS, before the show_footer function

st.markdown("""
    <style>
    /* Plot container styles */
    .plot-container {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 auto;
    }
    
    /* Make plots responsive */
    iframe {
        width: 100% !important;
        min-height: 400px;
    }
    
    /* Adjust plot sizes for mobile */
    @media (max-width: 768px) {
        .plot-container {
            padding: 0 !important;
        }
        
        iframe {
            min-height: 300px !important;
            height: auto !important;
        }
        
        /* Make pie charts more compact on mobile */
        [class*="pie"] iframe {
            min-height: 250px !important;
        }
        
        /* Make bar charts more readable on mobile */
        [class*="bar"] iframe {
            min-height: 350px !important;
        }
        
        /* Adjust plot margins and padding */
        .js-plotly-plot .plotly {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Make plot text more readable on mobile */
        .js-plotly-plot .plotly text {
            font-size: 10px !important;
        }
        
        /* Adjust legend size and position */
        .js-plotly-plot .legend {
            font-size: 10px !important;
            transform: scale(0.9);
        }
    }
    
    /* Dark theme for plots */
    .js-plotly-plot {
        background-color: #1a1a1a !important;
    }
    
    .js-plotly-plot .plotly text {
        fill: #ffffff !important;
        color: #ffffff !important;
    }
    
    .js-plotly-plot .plotly .gridlayer path {
        stroke: #404040 !important;
    }
    
    .js-plotly-plot .plotly .bglayer rect {
        fill: #1a1a1a !important;
    }
    </style>
""", unsafe_allow_html=True)

def show_footer():
    """Show footer with all buttons"""
    # Add footer CSS
    st.markdown("""
        <style>
        .footer-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #1a1a1a;
            padding: 8px;
            z-index: 999;
            border-top: 1px solid #333;
        }
        
        /* Style all footer buttons */
        .footer-container .stButton > button {
            background-color: #2d2d2d !important;
            color: white !important;
            border: 1px solid #404040 !important;
            padding: 5px 10px !important;
            font-size: 12px !important;
            height: 30px !important;
            min-height: 30px !important;
            width: auto !important;
            transition: all 0.2s ease;
        }
        
        .footer-container .stButton > button:hover {
            background-color: #404040 !important;
            border-color: #505050 !important;
            transform: translateY(-2px);
        }
        
        /* Warning message style */
        .warning-message {
            position: fixed;
            bottom: 60px;
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba(255, 75, 75, 0.1);
            color: #ff4b4b;
            padding: 8px 16px;
            border-radius: 5px;
            font-size: 12px;
            z-index: 1000;
        }
        
        @media (max-width: 768px) {
            .footer-container .stButton > button {
                padding: 3px 8px !important;
                font-size: 11px !important;
                height: 25px !important;
                min-height: 25px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create footer container
    st.markdown('<div class="footer-container">', unsafe_allow_html=True)
    
    # Create columns for buttons
    cols = st.columns([1, 1, 1, 9])
    
    # Back button
    with cols[0]:
        if st.button("⬅️", key="back_btn", help="Go back to platform selection"):
            if 'selected_platform' in st.session_state:
                del st.session_state.selected_platform
            st.rerun()
    
    # Help button
    with cols[1]:
        if st.button("📞", key="help_btn", help="Get support"):
            st.session_state.show_support = True
            st.rerun()
    
    # Logout button
    with cols[2]:
        warning_placeholder = st.empty()
        if st.button("🚪", key="logout_btn", help="Logout from application"):
            warning_placeholder.markdown("""
                <div class="warning-message">
                    ⚠️ Logging out in 5s...
                </div>
            """, unsafe_allow_html=True)
            
            for i in range(5, 0, -1):
                time.sleep(1)
                warning_placeholder.markdown(f"""
                    <div class="warning-message">
                        ⚠️ Logging out in {i}s...
                    </div>
                """, unsafe_allow_html=True)
            
            warning_placeholder.empty()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Add this CSS to your existing styles
st.markdown("""
    <style>
    /* Back button specific style */
    [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child button {
        background-color: #2d2d2d !important;
        border-color: #404040 !important;
        padding: 10px !important;
        min-width: 80px !important;
        font-size: 12px !important;
    }
    
    [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child button:hover {
        background-color: #404040 !important;
        border-color: #505050 !important;
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

def show_platform_selector_header():
    """Show platform selector in top right"""
    platforms = {
        'PhonePe': '📱',
        'Google Pay': '💳',
        'Paytm': '💰',
        'SuperMoney': '💸',
        'NAVI': '🏦',
        'Amazon Pay': '🛒',
        'WhatsApp Pay': '💬',
        'BHIM UPI': '🇮🇳',
        'CRED': '💎',
        'MobiKwik': '📲',
        'FreeCharge': '⚡',
        'PayPal': '��',
        'Other': '🔄'
    }

    # Add CSS for platform selector
    st.markdown("""
        <style>
        /* Platform selector container */
        .platform-selector {
            position: fixed;
            top: 0;
            right: 0;
            padding: 15px;
            background-color: #1a1a1a;
            z-index: 1000;
            border-bottom-left-radius: 10px;
            box-shadow: -2px 2px 5px rgba(0,0,0,0.2);
        }
        
        /* Platform buttons grid */
        .platform-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            max-width: 400px;
        }
        
        /* Platform button style */
        .stButton button {
            width: 100%;
            background-color: #2d2d2d !important;
            border: 1px solid #404040 !important;
            color: #ffffff !important;
            padding: 10px !important;
            font-size: 14px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton button:hover {
            background-color: #404040 !important;
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(255,255,255,0.1);
            border-color: #505050 !important;
        }
        
        .platform-active {
            background-color: #000000 !important;
            border-color: #505050 !important;
            color: #ffffff !important;
        }

        /* Make emojis more visible on dark background */
        .stButton button {
            text-shadow: 0 0 10px rgba(255,255,255,0.5);
        }
        </style>
    """, unsafe_allow_html=True)

    # Create platform selector container
    with st.container():
        st.markdown('<div class="platform-selector"><div class="platform-grid">', unsafe_allow_html=True)
        
        # Create columns for the grid
        cols = st.columns(3)
        current_platform = st.session_state.get('selected_platform', '')
        
        # Add platform buttons
        for idx, (platform, icon) in enumerate(platforms.items()):
            with cols[idx % 3]:
                if st.button(
                    f"{icon}\n{platform}",
                    key=f"platform_{platform}",
                    use_container_width=True,
                    type="secondary"
                ):
                    st.session_state.selected_platform = platform
                    st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)

def main():
    # Check if user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        show_login_page()
        return

    if 'selected_platform' in st.session_state:
        # If platform is selected, show the platform page
        route_to_platform(st.session_state.selected_platform, st.session_state.username)
    else:
        # Show welcome message with instructions
        st.title("Welcome to Statement Analyzer!")
        st.markdown("""
        ### Please select your payment platform
        
        Choose the platform you use for digital payments to analyze your statements.
        Your data is processed securely and never stored.
        """)
        
        # Show platform grid
        route_to_platform(None, st.session_state.username)

if __name__ == "__main__":
    main() 