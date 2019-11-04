# -- View Topology of Network
# Lighter color connections are connected to earlier layers (NOT weight strength)
import vis as nv
import matplotlib.pyplot as plt
nv.viewInd('log/test_best.out','swingup')
plt.show()
