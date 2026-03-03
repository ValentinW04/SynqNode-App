import streamlit as st
import requests
import json
import os
import re
import time
from openai import OpenAI
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI Client (assumes OPENAI_API_KEY is available in the environment)
def get_openai_client():
    return OpenAI()

def extract_links(markdown_text, base_url):
    """Extracts internal HTTP/HTTPS links from markdown text."""
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')
    links = link_pattern.findall(markdown_text)
    
    internal_links = set()
    base_domain = urlparse(base_url).netloc
    
    for link in links:
        link = link.strip()
        if link.startswith(('mailto:', 'tel:', '#')):
            continue
            
        full_url = urljoin(base_url, link)
        parsed_url = urlparse(full_url)
        
        if parsed_url.scheme in ('http', 'https') and parsed_url.netloc == base_domain:
            clean_url = parsed_url._replace(fragment='').geturl()
            internal_links.add(clean_url)
            
    return list(internal_links)


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
metric_lbl = "#94A3B8"
input_bg = "#FFFFFF"
input_border = "rgba(0, 0, 0, 0.2)"

# 1. Custom CSS
st.markdown(f"""
    <style>
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        .stApp {{
            background-color: {{bg_color}};
            color: {{text_color}};
            font-family: 'Inter', sans-serif;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        
        .block-container {{
            padding-top: 4rem !important;
            padding-bottom: 6rem !important;
            max-width: 1000px;
        }}

        /* Top Nav / Logo */
        .nav-logo {{
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: {{text_color}};
            margin-bottom: 4rem;
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
        
        /* Inputs */
        div[data-baseweb="input"] {{
            background-color: {{input_bg}} !important;
            border: 1px solid {{input_border}} !important;
            border-radius: 8px !important;
            height: 48px;
        }}
        div[data-baseweb="input"] input {{
            color: {{text_color}} !important;
            font-weight: 500;
        }}

        /* Typography */
        .app-title {{
            font-weight: 800;
            font-size: 3rem;
            line-height: 1.1;
            letter-spacing: -0.04em;
            color: {{text_color}};
            margin-bottom: 1rem;
            text-align: center;
        }}
        .app-subtitle {{
            font-weight: 400;
            font-size: 1.15rem;
            color: {{sub_text}};
            max-width: 650px;
            margin: 0 auto 3rem auto;
            line-height: 1.6;
            letter-spacing: -0.01em;
            text-align: center;
        }}

        /* Footer/Legal */
        .footer-text {{
            color: {{sub_text}};
            font-size: 0.85rem;
        }}
        .streamlit-expanderHeader {{
            color: {{sub_text}} !important;
            font-weight: 500 !important;
            border-bottom: 1px solid {{border_color}} !important;
        }}
        .streamlit-expanderContent {{
            color: {{sub_text}};
            background-color: {{bg_color}};
        }}
        
        /* Tabs and Metric overrides */
        [data-testid="stMetricLabel"] {{
            color: {{metric_lbl}} !important;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}
        [data-testid="stMetricValue"] {{
            color: {{text_color}} !important;
            font-weight: 700;
        }}
        /* Keep markdown text area readable in light mode */
        textarea {{
            background-color: {{input_bg}} !important;
            color: {{text_color}} !important;
            border: 1px solid {{input_border}} !important;
        }}
    </style>
""".replace("{{", "{").replace("}}", "}"), unsafe_allow_html=True)

# Navigation
col_logo, col_nav_btn = st.columns([5, 1])
with col_logo:
    st.markdown("<div class='nav-logo'>SynqNode</div>", unsafe_allow_html=True)

# 2. Professional Copywriting
st.markdown("<div class='app-title'>Infrastructure for the Agentic Web.</div>", unsafe_allow_html=True)
st.markdown("""
<div class='app-subtitle'>
    Transform your standard website into a machine-readable data layer. Ensure your products, pricing, and services are perfectly understood by autonomous AI agents.
</div>
""", unsafe_allow_html=True)

# Search Bar Input Area
st.markdown("<br>", unsafe_allow_html=True)
col_input1, col_input2 = st.columns([3, 1], gap="medium")
with col_input1:
    url_input = st.text_input("Target URL", placeholder="https://example.com", label_visibility="collapsed")
with col_input2:
    generate_pressed = st.button("Generate SDK", type="primary", use_container_width=True)
st.markdown("<br><br>", unsafe_allow_html=True)


if generate_pressed:
    if not url_input.strip():
        st.warning("Please enter a valid URL.")
    else:
        if not url_input.startswith("http"):
            url_input = "https://" + url_input

        # 3. Pipeline Status Updates
        with st.status("Initializing SynqNode Pipeline...", expanded=True) as status:
            try:
                # --- Step 1 ---
                status.update(label="01 / INGEST: Analyzing base domain architecture...", state="running")
                jina_url = f"https://r.jina.ai/{url_input}"
                response = requests.get(jina_url, headers={"X-No-Cache": "true"})
                response.raise_for_status()
                base_text = response.text
                
                status.write("Base domain ingested successfully.")
                status.write("Mapping internal endpoint architecture...")
                internal_links = extract_links(base_text, url_input)
                status.write(f"Isolated {len(internal_links)} internal routes.")

                client = get_openai_client()
                selected_urls = []

                if internal_links:
                    # --- Step 2 ---
                    status.update(label="02 / SCOUT: Identifying commercial endpoints...", state="running")
                    
                    scout_system_prompt = """You are a web routing assistant. Select a maximum of 10 URLs strictly necessary to understand products, services, pricing, and segments. 
CRITICAL RULES:
1. Prioritize commercial endpoints like '/preise', '/tarife', '/pakete', '/pricing', '/agencies', '/enterprise', '/funktionen'.
2. LANGUAGE & DEDUPLICATION AVOIDANCE: If the website is multilingual, STRICTLY stick to ONE language path (prefer the primary language, usually German if '.de' or if German paths exist). DO NOT select both '/preise' and '/en/pricing'. Avoid any redundant URLs that serve the exact same purpose in a different language or region.
Return ONLY a JSON array of selected URL strings. No markdown."""
                    scout_user_prompt = f"Internal URLs:\n{json.dumps(internal_links, indent=2)}\n\nSelect up to 10 critical URLs."
                    
                    scout_completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": scout_system_prompt},
                            {"role": "user", "content": scout_user_prompt}
                        ]
                    )
                    
                    scout_response = scout_completion.choices[0].message.content.strip()
                    
                    try:
                        if scout_response.startswith('```json'):
                            scout_response = scout_response[7:-3]
                        elif scout_response.startswith('```'):
                            scout_response = scout_response[3:-3]
                            
                        selected_urls = json.loads(scout_response)
                        if not isinstance(selected_urls, list):
                            selected_urls = []
                        selected_urls = [urljoin(url_input, url) for url in selected_urls[:10]]
                        status.write(f"Prioritized endpoints: {', '.join(selected_urls)}")
                    except json.JSONDecodeError:
                        status.write("Warning: Failed to parse Scout response. Proceeding with base architecture.")
                        selected_urls = []
                else:
                    status.write("No internal commercial routes found to prioritize.")

                # --- Step 3 ---
                status.update(label="03 / CRAWL: Deep-crawling selected endpoints...", state="running")
                urls_to_crawl = [url_input] + [url for url in selected_urls if url != url_input]
                aggregated_text = f"--- Content from {url_input} ---\n\n{base_text}"
                
                for i, url in enumerate(urls_to_crawl[1:], start=1):
                    status.write(f"Synchronizing endpoint {i}/{len(urls_to_crawl)-1}: {url}...")
                    time.sleep(2)
                    try:
                        resp = requests.get(f"https://r.jina.ai/{url}", headers={"X-No-Cache": "true"})
                        resp.raise_for_status()
                        aggregated_text += f"\n\n--- Content from {url} ---\n\n{resp.text}"
                    except Exception as e:
                        status.write(f"Warning: Endpoint synchronization failed for {url}")
                        
                # --- Step 4 ---
                status.update(label="04 / COMPILE: Generating Agent-Ready JSON...", state="running")

                system_prompt = """You are an expert at parsing web content into structured SAO formats.
Generate two items from the content:
1. `llms_txt`: A markdown string explaining company structure, offerings, and agent navigation.
2. `products_json`: A precise JSON array of products/services with rich data.

ANTI-HALLUCINATION PROTOCOL: You are analyzing real B2B websites. DO NOT guess, estimate, or invent prices. DO NOT assume USD ($) if the context is European (e.g., Germany). If exact numerical prices are NOT explicitly written in the provided text (e.g., because they are hidden behind Javascript or dynamic sliders), you MUST set the 'pricing' field to 'Data not rendered in raw HTML (Requires JS)'.
If explicit pricing is missing, you MUST lower the 'confidence_score' to 0.4 or lower. In the 'data_gaps' field, explicitly state: 'Pricing tables blocked by Javascript/Bot-Protection. Manual verification required.'.

Adhere to this schema for `products_json` items:
{
  "name": "Product Name",
  "description": "Rich description",
  "pricing": "Nested object (e.g. {'Brands': '500€', 'Agencies': '900€'}) or standard string",
  "confidence_score": 0.95,
  "data_gaps": "E.g., 'Agency pricing missing'"
}
Return raw JSON object with keys "llms_txt" and "products_json". NO MARKDOWN BACKTICKS."""

                MAX_CHARS = 350000
                if len(aggregated_text) > MAX_CHARS:
                    aggregated_text = aggregated_text[:MAX_CHARS] + "\n\n[SYSTEM WARNING: CONTENT TRUNCATED DUE TO LENGTH LIMITS]"

                user_prompt = f"Website Content:\n\n{aggregated_text}"

                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"}
                )

                result_json = json.loads(completion.choices[0].message.content)
                st.session_state.llms_txt_content = result_json.get("llms_txt", "Error")
                
                products_data = result_json.get("products_json", [])
                if isinstance(products_data, str):
                    try:
                        st.session_state.products_json_content = json.dumps(json.loads(products_data), indent=4, ensure_ascii=False)
                    except:
                        st.session_state.products_json_content = products_data
                else:
                    st.session_state.products_json_content = json.dumps(products_data, indent=4, ensure_ascii=False)

                st.session_state.pages_scouted_count = len(urls_to_crawl)
                status.update(label="05 / DEPLOY: Pipeline Complete.", state="complete", expanded=False)

            except Exception as e:
                status.update(label="Protocol Error", state="error", expanded=True)
                st.error(f"Execution failed. Details: {e}")

# 4. Results Dashboard
if "llms_txt_content" in st.session_state and "products_json_content" in st.session_state:
    
    st.markdown(f"<div style='border: 1px solid {{border_color}}; border-radius: 12px; padding: 2rem; background-color: {{card_bg}}; margin-bottom: 2rem;'>".replace("{{", "{").replace("}}", "}"), unsafe_allow_html=True)
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Endpoints Scouted", f"{st.session_state.get('pages_scouted_count', 1)}")
    with metric_col2:
        st.metric("AI Visibility Ready", "Yes", "Optimized")
    with metric_col3:
        st.metric("Data Format", "Markdown & JSON")
    st.markdown("</div>", unsafe_allow_html=True)

    tab_llms, tab_products = st.tabs(["llms.txt", "products.json"])

    with tab_llms:
        st.text_area("llms.txt content", value=st.session_state.llms_txt_content, height=400, label_visibility="collapsed")
        st.download_button("Download llms.txt", data=st.session_state.llms_txt_content, file_name="llms.txt", mime="text/markdown", type="primary")

    with tab_products:
        st.text_area("products.json content", value=st.session_state.products_json_content, height=400, label_visibility="collapsed")
        st.download_button("Download products.json", data=st.session_state.products_json_content, file_name="products.json", mime="application/json", type="primary")

st.markdown("<br><br><br>", unsafe_allow_html=True)

# 5. Footer (Legal)
st.markdown(f"<hr style='border-top: 1px solid {{border_color}};'>".replace("{{", "{").replace("}}", "}"), unsafe_allow_html=True)

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
