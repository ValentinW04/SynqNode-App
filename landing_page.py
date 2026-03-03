import streamlit as st

st.set_page_config(
    page_title="SynqNode | AI Visibility Infrastructure",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define Theme Colors (Permanent Light Mode)
bg_color = "#F8FAFC"
text_color = "#0F172A"
card_bg = "#FFFFFF"
sub_text = "#64748B"
border_color = "rgba(0, 0, 0, 0.1)"
btn_prim_bg = "#0F172A"
btn_prim_text = "#FFFFFF"
btn_sec_bg = "#FFFFFF"
btn_sec_text = "#0F172A"
btn_sec_border = "rgba(0, 0, 0, 0.2)"
btn_sec_hover_bg = "rgba(0, 0, 0, 0.05)"
step_num_color = "#94A3B8"
error_border = "rgba(220,38,38,0.2)"
verify_color = "#000000"
scale_bg = "#F1F5F9"
scale_color = "#0F172A"

# 1. Page Config & CSS
st.markdown(f"""
    <style>
        /* Base Streamlit Overrides */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Global Typography & Colors */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        .stApp {{
            background-color: {{bg_color}};
            color: {{text_color}};
            font-family: 'Inter', sans-serif;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        /* Container padding for massive whitespace */
        .block-container {{
            padding-top: 4rem !important;
            padding-bottom: 6rem !important;
            max-width: 1200px;
        }}

        /* Top Nav / Logo */
        .nav-logo {{
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: {{text_color}};
            margin-bottom: 6rem;
        }}

        /* Buttons styles targeting data-testid or kind */
        button[data-testid="baseButton-primary"], 
        button[data-testid="stBaseButton-primary"], 
        button[kind="primary"] {{
            background-color: {{btn_prim_bg}} !important;
            color: {{btn_prim_text}} !important;
            border: none;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.75rem 2rem !important;
            font-size: 1rem !important;
            height: 48px !important;
            letter-spacing: -0.01em !important;
            transition: all 0.2s ease !important;
        }}
        button[data-testid="baseButton-primary"]:hover, 
        button[data-testid="stBaseButton-primary"]:hover, 
        button[kind="primary"]:hover {{
            transform: translateY(-2px) !important;
            opacity: 0.9 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        }}
        
        button[data-testid="baseButton-secondary"], 
        button[data-testid="stBaseButton-secondary"], 
        button[kind="secondary"] {{
            background-color: {{btn_sec_bg}} !important;
            color: {{btn_sec_text}} !important;
            border: 1px solid {{btn_sec_border}} !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            padding: 0.75rem 2rem !important;
            font-size: 1rem !important;
            height: 48px !important;
            letter-spacing: -0.01em !important;
            transition: all 0.2s ease !important;
        }}
        button[data-testid="baseButton-secondary"]:hover, 
        button[data-testid="stBaseButton-secondary"]:hover, 
        button[kind="secondary"]:hover {{
            border-color: {{text_color}} !important;
            background-color: {{btn_sec_hover_bg}} !important;
        }}

        /* Hero Typography */
        .hero-title {{
            text-align: center;
            font-weight: 800;
            font-size: 4.5rem;
            line-height: 1.05;
            letter-spacing: -0.04em;
            color: {{text_color}};
            margin-bottom: 1.5rem;
        }}
        .hero-subtitle {{
            text-align: center;
            font-weight: 400;
            font-size: 1.25rem;
            color: {{sub_text}};
            max-width: 800px;
            margin: 0 auto 3rem auto;
            line-height: 1.6;
            letter-spacing: -0.01em;
        }}

        /* Trust Banner */
        .trust-banner {{
            border-top: 1px solid {{border_color}};
            border-bottom: 1px solid {{border_color}};
            padding: 2rem 0;
            margin: 6rem 0;
            display: flex;
            justify-content: center;
            gap: 4rem;
        }}
        .trust-item {{
            color: {{sub_text}};
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }}

        /* Section Borders and Cards */
        .glass-card {{
            background-color: {{card_bg}};
            border: 1px solid {{border_color}};
            border-radius: 16px;
            padding: 3rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        }}
        
        /* Headers inside sections */
        .section-header {{
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            margin-bottom: 3rem;
            color: {{text_color}};
        }}
        
        .card-title {{
            font-weight: 600;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
            color: {{text_color}};
        }}
        
        .card-text {{
            color: {{sub_text}};
            font-size: 1.1rem;
            line-height: 1.6;
        }}

        /* Workflow steps */
        .workflow-step-num {{
            font-family: monospace;
            font-size: 0.9rem;
            color: {{step_num_color}};
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        
        /* Footer/Legal */
        .footer-text {{
            color: {{sub_text}};
            font-size: 0.85rem;
        }}
        
        /* Fix Expander styles */
        .streamlit-expanderHeader {{
            color: {{sub_text}} !important;
            font-weight: 500 !important;
            border-bottom: 1px solid {{border_color}} !important;
        }}
        .streamlit-expanderContent {{
            color: {{sub_text}};
            background-color: {{bg_color}};
        }}
    </style>
""".replace("{{", "{").replace("}}", "}"), unsafe_allow_html=True)

# Navigation
col_logo, col_nav_btn = st.columns([5, 1])
with col_logo:
    st.markdown("<div class='nav-logo'>SynqNode</div>", unsafe_allow_html=True)
with col_nav_btn:
    st.link_button("Launch Scanner", url="https://synqnode-app.streamlit.app/#the-infrastructure-for-the-agentic-web", type="primary", use_container_width=True)

# 1. Hero Section
st.markdown("<div class='hero-title'>The Authoritative<br>Data Layer for the Agentic Web.</div>", unsafe_allow_html=True)

st.markdown("""
<div class='hero-subtitle'>
    Don't let AI guess your business facts. SynqNode provides the machine-readable infrastructure (<b>llms.txt</b> & <b>products.json</b>) that ensures ChatGPT, Perplexity, and autonomous agents access your pricing and services with 100% accuracy.
</div>
""", unsafe_allow_html=True)

# Centered Dual CTAs
col_spacer1, col_cta1, col_cta2, col_spacer2 = st.columns([2, 2, 2, 2])
with col_cta1:
    st.link_button("Launch Free Scanner", url="https://synqnode-app.streamlit.app/#the-infrastructure-for-the-agentic-web", type="primary", use_container_width=True)
with col_cta2:
    st.link_button("Talk to Enterprise Sales", url="mailto:valentin_weiss@gmx.de", type="secondary", use_container_width=True)


# 2. Trust Banner
st.markdown("""
<div class='trust-banner'>
    <span class='trust-item'>✓ DSGVO Compliant</span>
    <span class='trust-item'>✓ Enterprise-Grade Security</span>
    <span class='trust-item'>✓ 100% Data Sovereignty</span>
    <span class='trust-item'>✓ Zero-Retention Processing</span>
</div>
""", unsafe_allow_html=True)


# 3. The Contrast (Infrastructure vs. Scraping)
st.markdown("<div class='section-header' style='text-align: center;'>Infrastructure outpaces AI-SEO.</div>", unsafe_allow_html=True)

col_contrast1, col_contrast2 = st.columns(2, gap="large")

with col_contrast1:
    st.markdown(f"""
    <div class='glass-card' style='border-color: {error_border};'>
        <div class='workflow-step-num'>THE OLD WAY</div>
        <div class='card-title'>Traditional AI-SEO</div>
        <div class='card-text'>
            Relying on search agents to scrape complex React frameworks leads to interpretative errors, massive data gaps, hallucinations, and high latency for pricing updates.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_contrast2:
    st.markdown("""
    <div class='glass-card'>
        <div class='workflow-step-num'>THE SYNQNODE WAY</div>
        <div class='card-title'>Authoritative Layer</div>
        <div class='card-text'>
            Providing a precise, JSON-structured database directly to agents guarantees zero hallucinations, perfect API-like latency, and an absolute source of truth.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br><br><br>", unsafe_allow_html=True)


# 4. How It Works (The Trust Workflow)
st.markdown("<div class='section-header'>The Trust Workflow. Generate, Verify, Deploy.</div>", unsafe_allow_html=True)

col_step1, col_step2, col_step3 = st.columns(3, gap="medium")

with col_step1:
    st.markdown("""
    <div style='padding-right: 1rem;'>
        <div class='workflow-step-num'>01 / SCOUT</div>
        <div class='card-title'>Map Architecture</div>
        <div class='card-text'>We programmatically analyze your domain to isolate highest-value commercial routing (pricing, service tiers, enterprise segments).</div>
    </div>
    """, unsafe_allow_html=True)

with col_step2:
    st.markdown(f"""
    <div style='padding-right: 1rem; border-left: 1px solid {border_color}; padding-left: 2rem;'>
        <div class='workflow-step-num' style='color: {verify_color}; font-weight: 600;'>02 / VERIFY</div>
        <div class='card-title'>Human-in-the-Loop</div>
        <div class='card-text'>Our extraction engine flags <b>Data Gaps</b> and provides <b>Confidence Scores</b>. You review and guarantee the facts before any data reaches the AI.</div>
    </div>
    """, unsafe_allow_html=True)

with col_step3:
    st.markdown(f"""
    <div style='padding-right: 1rem; border-left: 1px solid {border_color}; padding-left: 2rem;'>
        <div class='workflow-step-num'>03 / DEPLOY</div>
        <div class='card-title'>Unquestioned Truth</div>
        <div class='card-text'>Upload the lightweight files to your root directory. Your business is instantly converted into the authoritative data source for the agentic web.</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br><br><br><br>", unsafe_allow_html=True)


# 5. Scalability Note
st.markdown(f"""
<div style='text-align: center; max-width: 600px; margin: 0 auto; padding: 2rem; border: 1px solid {border_color}; border-radius: 12px; background-color: {scale_bg};'>
    <div class='workflow-step-num'>B2B ENTERPRISE SCALABILITY</div>
    <div class='card-text' style='color: {scale_color}; font-weight: 500;'>Perfect for stable B2B environments. Built to dynamically scale via API for high-frequency pricing updates.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)


# 6. Footer (German Legal Compliance)
st.markdown(f"<hr style='border-top: 1px solid {border_color};'>", unsafe_allow_html=True)

col_footer1, col_footer2 = st.columns([1, 1])

with col_footer1:
    st.markdown("""
    <div class='footer-text'>
        <p><strong>© 2026 SynqNode Technologies.</strong></p>
        <p>Built for the European Data Economy.</p>
    </div>
    """, unsafe_allow_html=True)

with col_footer2:
    with st.expander("Impressum"):
        st.markdown("""
        <div class='footer-text'>
            <b>Impressum</b><br>
            Angaben gemäß § 5 TMG:<br><br>
            <b>Name:</b> Valentin Weiss<br>
            <b>Adresse:</b> Klosestraße 13, 76137 Karlsruhe<br><br>
            <b>Kontakt:</b><br>
            E-Mail: valentin_weiss@gmx.de
        </div>
        """, unsafe_allow_html=True)
        
    with st.expander("Datenschutz"):
        st.markdown("""
        <div class='footer-text'>
            <b>Datenschutzerklärung</b><br><br>
            Processed via secure APIs (e.g. OpenAI/Jina API) to generate structured files. No permanent storage or retention of scraped URLs or their content on SynqNode servers.<br><br>
            <i>[Hier fügen Sie den vollständigen Text Ihres Datenschutz-Generators, z.B. von eRecht24, ein.]</i>
        </div>
        """, unsafe_allow_html=True)
