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
    # Matches markdown links [text](url)
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')
    links = link_pattern.findall(markdown_text)
    
    internal_links = set()
    base_domain = urlparse(base_url).netloc
    
    for link in links:
        link = link.strip()
        # Ignore obvious non-http links and anchors
        if link.startswith(('mailto:', 'tel:', '#')):
            continue
            
        # Resolve relative URLs
        full_url = urljoin(base_url, link)
        parsed_url = urlparse(full_url)
        
        # Only keep HTTP/HTTPS links belonging to the same domain (internal links)
        if parsed_url.scheme in ('http', 'https') and parsed_url.netloc == base_domain:
            # Normalize URL by removing fragment
            clean_url = parsed_url._replace(fragment='').geturl()
            internal_links.add(clean_url)
            
    return list(internal_links)


st.set_page_config(
    page_title="SynqNode | AI Visibility Infrastructure",
    page_icon="⚡",
    layout="centered"
)

# 1. Custom CSS
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Optional: make the main container a bit more sleek */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
        
        /* Tweak the primary button to look more like a SaaS CTA */
        .stButton>button[data-testid="baseButton-primary"] {
            width: 100%;
            border-radius: 6px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# 2. Professional Copywriting (Hero Section)
st.markdown("<h1 style='text-align: center; font-weight: 700; margin-bottom: 0;'>SynqNode.</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight: 400; color: #666; margin-top: 0;'>The Infrastructure for the Agentic Web.</h3>", unsafe_allow_html=True)

st.markdown("""
<p style="text-align: center; max-width: 600px; margin: 1rem auto; font-size: 1.1rem; color: #444;">
Transform your standard website into a machine-readable data layer. Ensure your products, pricing, and services are perfectly understood by ChatGPT, Perplexity, and autonomous AI agents.
</p>
""", unsafe_allow_html=True)

st.write("")

# Use columns to create a centered, sleek search bar feel
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    url_input = st.text_input("Target URL", placeholder="https://example.com", label_visibility="collapsed")
    generate_pressed = st.button("Generate AI Interface", type="primary", use_container_width=True)

st.write("---")

if generate_pressed:
    if not url_input.strip():
        st.warning("Please enter a valid URL.")
    else:
        if not url_input.startswith("http"):
            url_input = "https://" + url_input

        # 3. Pipeline Status Updates (Professional Tone)
        with st.status("Initializing SynqNode Data Pipeline...", expanded=True) as status:
            try:
                # --- Step 1: The Base Crawl & Link Extraction ---
                status.update(label="Step 1: Ingesting base domain architecture...", state="running")
                jina_url = f"https://r.jina.ai/{url_input}"
                response = requests.get(jina_url)
                response.raise_for_status()
                base_text = response.text
                
                status.write("Base domain ingested successfully.")
                
                # Extract links
                status.write("Mapping internal endpoint architecture...")
                internal_links = extract_links(base_text, url_input)
                status.write(f"Isolated {len(internal_links)} internal routes.")

                client = get_openai_client()
                selected_urls = []

                if internal_links:
                    # --- Step 2: The "Scout" LLM Pass ---
                    status.update(label="Step 2: AI Scout idenitifying high-value commercial and structural endpoints...", state="running")
                    
                    scout_system_prompt = """You are a web routing assistant. Look at this list of URLs from a company's website. Select a maximum of 6 URLs that are absolutely strictly necessary to understand the company's core products, services, pricing, and audience segments. Prioritize URLs containing words like pricing, preise, products, leistungen, about, or services. Additionally, specifically hunt for audience-specific endpoints (e.g., '/agencies', '/enterprise', '/solutions') and subpages that might contain pricing toggles or tiered service descriptions. Return ONLY a JSON array of the selected URL strings. Do not include markdown formatting or backticks around the JSON array."""
                    
                    scout_user_prompt = f"Here are the internal URLs found on the site:\n{json.dumps(internal_links, indent=2)}\n\nPlease select up to 6 of the most relevant URLs for understanding products, services, segments, and pricing based on the instructions."
                    
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
                        # Ensure we convert relative paths or partial URLs correctly back to absolute URLs before crawling
                        selected_urls = [urljoin(url_input, url) for url in selected_urls[:6]]
                        status.write(f"Scout prioritized {len(selected_urls)} critical endpoints: {', '.join(selected_urls)}")
                    except json.JSONDecodeError:
                        status.write("Warning: Failed to parse Scout response. Proceeding with base architecture only.")
                        selected_urls = []

                else:
                    status.write("No internal commercial routes found to prioritize.")

                # --- Step 3: Deep Crawl & Final Generation ---
                status.update(label="Step 3: Deep-crawling selected endpoints via secure Jina API...", state="running")
                
                urls_to_crawl = [url_input] + [url for url in selected_urls if url != url_input]
                
                aggregated_text = f"--- Content from {url_input} ---\n\n{base_text}"
                
                for i, url in enumerate(urls_to_crawl[1:], start=1):
                    status.write(f"Synchronizing endpoint {i}/{len(urls_to_crawl)-1}: {url}... (Rate limit throttle active)")
                    time.sleep(2)
                    try:
                        resp = requests.get(f"https://r.jina.ai/{url}")
                        resp.raise_for_status()
                        aggregated_text += f"\n\n--- Content from {url} ---\n\n{resp.text}"
                    except Exception as e:
                        status.write(f"Warning: Endpoint synchronization failed for {url}: {e}")
                        
                # --- Step 4: Generating final AI formats ---
                status.update(label="Step 4: Compiling Agent-Ready data structures (llms.txt & JSON)...", state="running")

                # The original generation prompt
                system_prompt = """You are an expert at analyzing website content and converting it into two specific formats for Search Agent Optimization.
Based on the provided website content, you must generate two items:
1. A markdown-formatted string meant for an `llms.txt` file that explains the structure of the business, its core offerings, and guides an AI agent on how to use this site.
2. A very precise list of products/services mentioned, including rich descriptions, multi-audience segment data, and structured pricing details.

Your response MUST be a valid JSON object with exactly two keys:
- "llms_txt": A string containing the markdown-formatted content for llms.txt.
- "products_json": A JSON array of objects representing the products/services found. 

For EACH product/service inside `products_json`, strictly adhere to this schema:
{
  "name": "Product Name",
  "description": "Rich description of the product or service.",
  "pricing": "Nested object representing segment-specific pricing if it exists (e.g., {'Brands': '$500', 'Agencies': '$900'}) or a standard description of pricing. Try to format hierarchically when multiple tiers or segments are detected.",
  "confidence_score": "Float between 0.0 and 1.0 representing how certain you are about the extracted data based purely on the text provided.",
  "data_gaps": "A string or list describing what missing information was not found on the page (e.g., 'Agency pricing not explicitly found on page')."
}

Do NOT include any markdown code block backticks (like ```json) in your final response. Just return the raw JSON string that can be parsed directly.
"""

                user_prompt = f"Aggregated Website Content:\n\n{aggregated_text}"

                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"}
                )

                result_text = completion.choices[0].message.content
                result_json = json.loads(result_text)

                st.session_state.llms_txt_content = result_json.get("llms_txt", "Error generating llms.txt content.")
                
                # Format products_json as a pretty string
                products_data = result_json.get("products_json", [])
                if isinstance(products_data, str):
                    try:
                        st.session_state.products_json_content = json.dumps(json.loads(products_data), indent=4, ensure_ascii=False)
                    except json.JSONDecodeError:
                        st.session_state.products_json_content = products_data
                else:
                    st.session_state.products_json_content = json.dumps(products_data, indent=4, ensure_ascii=False)

                # Store the length of urls crawled for the metrics dashboard
                st.session_state.pages_scouted_count = len(urls_to_crawl)

                status.update(label="SynqNode Pipeline Complete.", state="complete", expanded=False)

            except requests.exceptions.RequestException as e:
                status.update(label="Ingestion Protocol Error", state="error", expanded=True)
                st.error(f"Failed to synchronize via Jina API. Error: {e}")
            except Exception as e:
                status.update(label="Compilation Error", state="error", expanded=True)
                st.error(f"An error occurred in compilation. Verification required for OPENAI_API_KEY. Details: {e}")

# 4. The Results Dashboard (SaaS Metrics) & Display
if "llms_txt_content" in st.session_state and "products_json_content" in st.session_state:
    
    # Render the Metrics Dashboard
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        pages_count = st.session_state.get('pages_scouted_count', 1)
        st.metric("Endpoints Scouted", f"{pages_count}")
    with metric_col2:
        st.metric("AI Visibility Ready", "Yes", "Optimized")
    with metric_col3:
        st.metric("Data Format", "Markdown & JSON")
        
    st.write("---")

    tab_llms, tab_products = st.tabs(["llms.txt", "products.json"])

    with tab_llms:
        st.text_area("llms.txt content", value=st.session_state.llms_txt_content, height=400, label_visibility="collapsed")
        st.download_button(
            label="Download llms.txt",
            data=st.session_state.llms_txt_content,
            file_name="llms.txt",
            mime="text/markdown",
            key="download_llms",
            type="primary"
        )

    with tab_products:
        st.text_area("products.json content", value=st.session_state.products_json_content, height=400, label_visibility="collapsed")
        st.download_button(
            label="Download products.json",
            data=st.session_state.products_json_content,
            file_name="products.json",
            mime="application/json",
            key="download_products",
            type="primary"
        )
# --- FOOTER & RECHTLICHES ---
st.write("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.85rem; line-height: 1.5; margin-bottom: 1rem;'>
    SynqNode AI Visibility Infrastructure
</div>
""", unsafe_allow_html=True)

# Wir nutzen Expander, damit die Texte das Design nicht stören, aber rechtlich vorhanden sind
col_imp, col_dat = st.columns(2)

with col_imp:
    with st.expander("Impressum"):
        st.markdown("""
        **Angaben gemäß § 5 TMG:** [Dein Vor- und Nachname]  
        [Deine Straße und Hausnummer]  
        [Deine PLZ und Ort, z.B. 76131 Karlsruhe]  
        
        **Kontakt:** E-Mail: [Deine E-Mail-Adresse]  
        """)

with col_dat:
    with st.expander("Datenschutz"):
        st.markdown("""
        **Datenschutzerklärung (Kurzfassung)** Wir nehmen den Schutz Ihrer Daten ernst. Diese App wird über Streamlit Community Cloud gehostet. 
        Bei der Nutzung unseres Scanners verarbeiten wir die von Ihnen eingegebene URL. 
        Die Inhalte der Ziel-URL werden über externe Dienstleister (Jina AI) ausgelesen und über die 
        API von OpenAI in strukturierte Datenformate übersetzt. Wir speichern die generierten Ergebnisse 
        (JSON/TXT) nicht dauerhaft auf unseren Servern, sondern stellen sie Ihnen lediglich zum direkten Download zur Verfügung.
        
        *[Hier den ausführlichen Text aus dem eRecht24-Generator einfügen]*
        """)
