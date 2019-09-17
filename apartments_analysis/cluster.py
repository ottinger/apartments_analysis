# NOTE: old, moved to Jupyter notebook
#
# Playing with cluster analysis of multifamily buildings in NW central OKC.
#
# See https://github.com/gboeing/urban-data-science/blob/master/15-Spatial-Cluster-Analysis/cluster-analysis.ipynb

import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
from sklearn.cluster import DBSCAN
from sklearn import metrics

df = pd.read_csv('multifamily_coords.csv')
df = df.sort_values(by=['lat','lon'])

coords = df.as_matrix(columns=['lat','lon'])

kms_per_radian = 6371.0088
epsilon = 0.1 / kms_per_radian

db = DBSCAN(eps=epsilon, min_samples=10, algorithm='ball_tree',metric='haversine').fit(np.radians(coords))
cluster_labels = db.labels_
unique_labels = set(cluster_labels)

print(unique_labels)

fig,ax = plt.subplots()
for cluster_label in unique_labels:
    size = 150
    if cluster_label == -1:
        size = 30
    x_coords = coords[cluster_labels==cluster_label][:,1]
    y_coords = coords[cluster_labels==cluster_label][:,0]
    ax.scatter(x=x_coords, y=y_coords, edgecolor='k', s=size, alpha=0.5)

plt.show()

