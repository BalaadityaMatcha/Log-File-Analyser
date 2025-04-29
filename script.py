
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
##### Please make only one image at a time to get results. #####

# g_1st -> A dictionary instance with 'Timestamps' as keys
# g_2nd -> A dictionary instance with 'Levels' as keys
# g_3rd -> A dictionary instance with 'EventIDs' as keys
# All the values of the respective keys of the dictionaries are the no.of occurences of them.

# Use them wisely to get your plot ☺️ and do not change anything apart from "dpi".

# Write your code here(pyplot and numpy are already imported as plt and np respectively 🫠)
plt.pie(g_2nd.values(),labels=g_2nd.keys())
# End of input.
plt.tight_layout()
plt.savefig('userplot.png',dpi=300)
os.rename('userplot.png','static/userplot.png')