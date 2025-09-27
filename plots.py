import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io,base64,os

g_1st, g_2nd, g_3rd = {},{},{}

def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_data

def g():
    if os.path.isfile("sorted.csv"):
        file="sorted.csv"
    else:
        file="Orgsorted.csv"
    with open(file, "r") as f:
        global g_1st, g_2nd, g_3rd
        for line in f:
            loline=line.strip().split(",")
            g_1st[loline[0]] = g_1st.get(loline[0], 0) + 1
            g_2nd[loline[1]] = g_2nd.get(loline[1], 0) + 1
            g_3rd[loline[3]] = g_3rd.get(loline[3], 0) + 1
    g_3rd = dict(sorted(g_3rd.items(), key=lambda item: item[0]))
    fig, ax1=plt.subplots()
    ax1.plot(g_1st.keys(),g_1st.values(),c='#FFB347',ls='-.',lw=0.25,marker='o',ms=1,mfc='hotpink',mec='hotpink')
    plt.xticks([list(g_1st.keys())[0], list(g_1st.keys())[-1]])
    ax1.set_title("Events logged with time")
    plt.tight_layout()
    img1=plot_to_base64(fig)
    fig, ax2=plt.subplots()
    ax2.pie(g_2nd.values(),labels=g_2nd.keys())
    ax2.set_title("Level State Distribution")
    plt.tight_layout()
    img2=plot_to_base64(fig)
    fig, ax3=plt.subplots()
    ax3.bar(g_3rd.keys(),g_3rd.values())
    ax3.set_title("Event Code Distribution")
    plt.tight_layout()
    img3=plot_to_base64(fig)
    [c.clear() for c in [g_1st,g_2nd,g_3rd]]
    return [img1,img2,img3]