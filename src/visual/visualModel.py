import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from cycler import cycler


data = pd.read_csv(sys.argv[1])

# fig = go.Figure(data=go.Scatter(x=np.array(data['x']), y=np.array(data['y'])))
# fig.show()
monochrome = (cycler('color', ['k']) * cycler('marker', ['', '.']) *
              cycler('linestyle', ['-', '--', ':', '=.']))
plt.rc('axes', prop_cycle=monochrome)

plt.plot(np.array(data['x']), np.array(data['y']))
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.show()
