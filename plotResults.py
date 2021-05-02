import networkx as nx
import numpy as np
import os
import ast
import matplotlib.pyplot as plt

def plot_res(list_of_res,mu_values,std):
    fig, ax = plt.subplots(1)
    for res,mu,s in zip(list_of_res,mu_values,std):
        ax.plot(beta_values,res,label = 'mu = '+mu)
        ax.legend()
        ax.set_title(graph_path.split('/')[-1][:-4])
        ax.legend(loc='lower right')
        ax.set_xlabel(r'$\beta$')
        ax.set_ylabel(r'$\rho$')
        ax.fill_between(beta_values, np.array(res) - np.array(s) , np.array(res) + np.array(s), alpha=0.7)
    fig.show()
    fig.savefig('results_'+graph_path.split('/')[-1][:-4]+'.png',dpi=100)


beta_values = np.arange(0.00,1.02,0.02)
graphs = ['./model/ER1000k8.net', './model/SF_500_g2.7.net', './real/airports_UW.net']
results_path = './results/'
results_dir = os.listdir(results_path)

for graph_path in graphs:
    net = nx.Graph(nx.read_pajek(graph_path))
    graph_name = graph_path.split('/')[-1][:-4]
    list_of_res = list()
    std = list()
    mu_values = list()
    for result_file in results_dir:
        if graph_name in result_file:
            if 'p_values' in result_file:
                with open(results_path+result_file,'r') as file:
                    res = file.read()
                    res = ast.literal_eval(res)
                    list_of_res.append(res)
                    mu_values.append(result_file.split('_')[-1][-3:])
            elif 'std' in result_file:
                with open(results_path+result_file,'r') as file:
                    res = file.read()
                    res = ast.literal_eval(res)
                    std.append(res)

    plot_res(list_of_res,mu_values,std)
