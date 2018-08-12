import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def coefs2df(coefs):
    methods = ['ANTs','BSpline','FLIRT','SPM']
    d = {}
    
    d['Methods']=[]
    for method in methods:
        for i in range(len(coefs[:,1])):
            d['Methods'].append(method)
    d['Overlap']=np.concatenate((coefs[:,0],coefs[:,1],coefs[:,2],coefs[:,3]), axis = 0)
    
    d['Mask'] = np.concatenate((coefs[:,4],coefs[:,4],coefs[:,4],coefs[:,4]), axis = 0)
    return pd.DataFrame(data=d)


def figure_boxplot(coefs):
    df = coefs2df(coefs)
    sns.set(style="ticks")
    f, ax = plt.subplots(figsize=(7, 6))
    sns.boxplot(x="Overlap", y="Methods", data=df, whis="range", palette="vlag",
                hue="Mask")
    ax2 = sns.swarmplot(x="Overlap", y="Methods", data=df,size=5, linewidth=0,palette=['grey','grey'], hue="Mask", dodge=True, color=".3")
    ax2.color = "black"
    handles, _ = ax2.get_legend_handles_labels()
    ax2.legend(handles, ["Man", "Woman"])
    ax.xaxis.grid(True)
    ax.set(ylabel="")
    ax.set(xlabel="Similiarity Coefficient")
    ax.set(title="Sorensen-Dice Overlap")
    sns.despine(trim=True, left=True)
    plt.show()
