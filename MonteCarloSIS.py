import networkx as nx
import numpy as np

N_rep = 100
T_max = 1000
p_0 = 0.2
T_trans = 900

graphs = ['./model/ER1000k8.net', './model/SF_500_g2.7.net', './real/airports_UW.net']

mu_values = [0.1, 0.5, 0.9]

for g in graphs:
    net = nx.Graph(nx.read_pajek(g))

    for mu in mu_values:
        p = []

        for beta in np.arange(0, 1.02, 0.02):

            p_sum = 0
            infected = {}
            for n in nx.nodes(net):
                if np.random.random() < p_0:
                    infected[n] = True
                else:
                    infected[n] = False

            infected_copy = infected.copy()

            for t in range(T_max):

                for n in nx.nodes(net):
                    if infected[n]:
                        if np.random.random() < mu:
                            infected_copy[n] = False
                    else:
                        neighbors = nx.neighbors(net, n)
                        for neigh in neighbors:
                            if infected[neigh]:
                                if np.random.random() < beta:
                                    infected_copy[n] = True
                                    break
                infected = infected_copy.copy()

                if t >= T_trans:
                    p_t = len([y for y in infected.keys() if infected[y]])
                    p_sum += p_t

            avg_p = p_sum/(T_max-T_trans)
            p.append(avg_p)

        with open('p_values_mu='+str(mu), mode='w') as o:
            print(p, file=o)

