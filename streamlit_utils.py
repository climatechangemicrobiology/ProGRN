#
# SPDX-FileCopyrightText: 2025 Tian Xiang Du
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
# Contact Tian Xiang Du (tdu@ualberta.ca)
# Commercial Licensing Contact: Lisa Stein (stein1@ualberta.ca)
# Modified with permission by Cerrise Weiblen 2025

from __future__ import annotations
from math import isclose
import pandas as pd
import networkx as nx
from pyvis.network import Network
import threading
from stqdm import stqdm

def provide_progress_bar(function, estimated_time, tstep=1, tqdm_kwargs={}, args=[], kwargs={}):
    """Tqdm wrapper for a long-running function

    args:
        function - function to run
        estimated_time - how long you expect the function to take
        tstep - time delta (seconds) for progress bar updates
        tqdm_kwargs - kwargs to construct the progress bar
        args - args to pass to the function
        kwargs - keyword args to pass to the function
    ret:
        function(*args, **kwargs)
    """
    ret = [None]  # Mutable var so the function can store its return value
    def myrunner(function, ret, *args, **kwargs):
        ret[0] = function(*args, **kwargs)

    thread = threading.Thread(target=myrunner, args=(function, ret) + tuple(args), kwargs=kwargs)
    pbar = stqdm(total=estimated_time, **tqdm_kwargs)

    thread.start()
    elapsed = 0
    while thread.is_alive():
        thread.join(timeout=tstep)
        elapsed += tstep
        if elapsed < estimated_time:
            pbar.update(tstep)
        elif isclose(elapsed, estimated_time, rel_tol=0.2):
            elapsed += estimated_time #to ensure thread does not enter this condition again
            pbar.set_postfix_str(s="Taking longer than usual...", refresh=True)
        
    pbar.close()
    return ret[0]

class GRN_Network:
    def __init__(self) -> None:
        self.group = 'small'
        self.data_fn = "consensus_network.csv"
        self.df = None
        
        # base dataframes (might want multiple views at some point)

        # network attrs
        #self.treatment = "note treatment data tag" # can also be other treatment data tags (might be unused...)
        self.edge_attr = None
        self.regulator_color = "#D81B60" # red
        self.target_color = "#00BDFF" # blue


        # internal df management
        self.color_map = None
        # self.product_map = None

        # graph statistics
        # tbd (num regs, tars, etc)
        # small (subnetwork.csv) indicates GRN data file containing subset of network connection output from ML inference
        # large (fullnetwork.csv) indicates GRN data file enhanced with full ML network plus additional columns containing gene expression information and gene product information

    def set_network_attributes(self, attrs: dict, debug: bool = False) -> None: 
            self.group = "consensus_network"
            self.data_fn = "consensus_network.csv"


    def reset(self):
        self.group = 'small'
        self.data_fn = "consensus_network.csv"
        self.df = load_df(self.data_fn)

        self.color_map = None
        # self.product_map = None

        self.edge_attr = None
        self.regulator_color = "#D81B60" # red
        self.target_color = "#00BDFF" # blue
        # graph statistics

    def init_df(self) -> None:
        # goal is to load df and prepare it for graphing
        self.df = load_df(self.data_fn)

        # get color mappings for each gene (regulator, target)
        color_map = {}
        reg_cm = {reg:self.regulator_color for reg in self.df['0Regulator']}
        color_map.update(reg_cm)
        tar_cm = {tar:self.target_color for tar in self.df['0Target']}
        color_map.update(tar_cm)
        self.color_map = color_map

        # get product map
        # product_map = {}
        # reg_pm = {reg:prod for reg, prod in zip(self.df['0Regulator'], self.df['reg_name'])}
        # product_map.update(reg_pm)
        # tar_pm = {tar:prod for tar, prod in zip(self.df['0Target'], self.df['tar_name'])}
        # product_map.update(tar_pm)
        # self.product_map = product_map

        # if other maps required, get them here...

    def create_html(self, static=True) -> None:
        # returns html fname for streamlit rendering
        # sets graph properties using default specifications, or pulls from GRN_network properties
        #self.init_df() # sets graph properties based on df and specs
        self.df['0Regulator'] = self.df['0Regulator'].astype(str)
        self.df['0Target'] = self.df['0Target'].astype(str)
        graph = nx.from_pandas_edgelist(self.df, source='0Regulator', target='0Target', edge_attr=self.edge_attr, create_using=nx.Graph())
        
        #node_list = list(graph.nodes)

        # node attributes:
        nx.set_node_attributes(graph, self.color_map, "color")
        nx.set_node_attributes(graph, 0.7, 'opacity')
        nx.set_node_attributes(graph, 2, 'borderWidth')
        '''
        nx.set_node_attributes(graph, degree_dict, 'degree_centrality')
        nx.set_node_attributes(graph, betweenness_dict, 'betweenness_centrality')
        nx.set_node_attributes(graph, closeness_dict, 'closeness_centrality')
        nx.set_node_attributes(graph, groups, 'group')
        nx.set_node_attributes(graph, node_degree_dict, 'degree')
        nx.set_node_attributes(graph, node_weight_dict, 'size')
        '''
        if not static: net = Network(width='900px', height='900px', bgcolor='#ffffff', font_color='black', filter_menu=True, select_menu=True)
        else: net = Network(width='900px', height='900px', bgcolor='#ffffff', font_color='black', filter_menu=True, select_menu=False)
        net.from_nx(graph)
        net.set_edge_smooth(True)
        net.show_buttons(filter_=['physics'])
        
        for node in net.nodes:
            node_id = node['id']
            node_description = f'Locus tag: {node_id}'
            # node_description = f'Locus tag: {node_id}, Product name: {self.product_map[node_id]}'
                         #tbi
            node['title'] = node_description
            #if static: node['physics']=False

        if static: net.toggle_physics(True)

        #labels = nx.draw_networkx_labels(graph, pos=nx.
        # spring_layout(graph)) #can change label font size and such here
        net.write_html(name='index.html', local=True, notebook=False, open_browser=False)


    def update_specs(self, **attrs) -> None:
        # attrs is a dictionary containing graph properties like color, size, etc
        # create_html needs to be rerun to reflect these changes. This is handled by the app interface
        
        pass


#@st.cache_data
def load_df(fname):
    df = pd.read_csv(f'{fname}')
    return df

if __name__ == "__main__":
    # Create a network instance
    network = GRN_Network()
    
    # Set attributes to use the preferred dataset
    network.group = "consensus_network"
    network.data_fn = "consensus_network.csv"
    
    # Initialize the dataframe (this sets up color maps, product maps, etc.)
    network.init_df()
    
    # Generate the HTML with search bar and interactive features
    network.create_html(static=False)  
    
    print(f"HTML visualization created successfully: index.html")
