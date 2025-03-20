#
# SPDX-FileCopyrightText: 2025 Tian Xiang Du
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
# Contact Tian Xiang Du (tdu@ualberta.ca)
# Commercial Licensing Contact: Lisa Stein (stein1@ualberta.ca)

# import dependencies
import streamlit as st
import streamlit.components.v1 as components
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_utils import GRN_Network, provide_progress_bar

# toggle to allow for manual debugging
DEBUG = False
static = True
st.set_page_config(
    page_title="GRN Visualization App",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Gene Regulation Network")

#style overrides
with open('style.css') as s:
    st.markdown(f'<style>{s.read()}</style>', unsafe_allow_html=True)

### app lifecycle management
# initialization behavior. run each time a change is made
# variable names

if "net" not in st.session_state:
    st.session_state["net"] = GRN_Network()
if "history" not in st.session_state:
    st.session_state["history"] = {}
if "disabled" not in st.session_state:
    st.session_state["disabled"] = False
if "group" not in st.session_state:
    st.session_state["group"] = 'small' # can be 'small' or 'large'
# history is organized by the above network attributes as follows:
# {"CD_Cluster_7_0": [html_str, **summary], {"IBD_ICD_4_200": [html_str, **summary]}

if DEBUG:
    net = GRN_Network()
else: net = st.session_state["net"]

# column layout control
col_network, col_summary = st.columns([0.65,0.35], gap="small")

def generate_col_network():
    with col_network:
    # generate name based on network attributes to check if object already exists
        net.set_network_attributes({**st.session_state}, DEBUG)
        net.init_df()
        net.create_html(static=static)
        html_network_fname = "index.html"
        print("html creation complete. opening now...")
        with open(html_network_fname, "r", encoding='utf-8') as f:
                html_network_str = f.read()
                f.close()
        print("html as string read. loading component...")
        components.html(html_network_str, height=950, width=902, scrolling=True) #850 802

generate_col_network()

with st.sidebar:
    with st.form("Visualization Options"):
        # search function: takes in ICD code or description, reloads network with new filter
        ###NOTE: ask cerrise what options are helpful

        st.markdown("**Visualization Options**")
        radio_group = st.radio(key="group", label="Network type", options=["small", "large"], help="Choose the network type. Small is top 1000 AMS/NMS genes by diffexp, Large is all found connections")
        
        # radio select node coloring: color nodes by first char of ICD code (eg: K codes have same color), or by Louvain clustering
        #radio_color = st.radio(key="color", label="Network organization:", options=["ICD", "Cluster"], help="Choose network coloring based on ICD code domain (eg: all codes that start with K) or Louvain clustering")
        
        # slider to filter by ICD code specificity
        #slider_specificity = st.slider(key="specICD", label="Level of hierarchical organization", min_value=1, max_value=7, step=1, help="Filter ICD codes based on ICD10 2020 hierarchies (ex: A00-B99 > A00-A99 > A00 > A00.1 ...)")

        # slider to filter by min ICD pairs
        #slider_minICD = st.slider(key="minICD", label="Minimum number of ICD pairs", min_value=0, max_value=1000, step=10, help="Filter ICD codes based on the number of associations between two codes")

        submitted = st.form_submit_button("Submit")
