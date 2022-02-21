import imageio
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Plot cropped image in 3D
# Link: https://chris35wills.github.io/courses/PythonPackages_matplotlib/matplotlib_3d/
img = imageio.imread('/home/nemish/BeCode/BeCode_Projects/3d-houses/Test.tif')

ny, nx = img.shape

x = np.linspace(0, 1, nx)
y = np.linspace(0, 1, ny)

xv, yv = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
dem3d = ax.plot_surface(xv, yv, img, cmap='winter', linewidth=0, alpha=0.2)
plt.show()
