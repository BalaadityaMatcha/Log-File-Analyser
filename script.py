
import matplotlib,os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
g_1st, g_2nd, g_3rd = {},{},{}
if os.path.isfile("sorted.csv"):
    file="sorted.csv"
else:
    file="Orgsorted.csv"
with open(file, "r") as f:
    for line in f:
        loline=line.strip().split(",")
        g_1st[loline[0]] = g_1st.get(loline[0], 0) + 1
        g_2nd[loline[1]] = g_2nd.get(loline[1], 0) + 1
        g_3rd[loline[3]] = g_3rd.get(loline[3], 0) + 1
    g_3rd = dict(sorted(g_3rd.items(), key=lambda item: item[0]))                  
