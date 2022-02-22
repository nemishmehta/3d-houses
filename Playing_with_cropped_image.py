import imageio
from matplotlib import pyplot as plt
import numpy as np

# Plot cropped image in 3D <-- Method 2. See method 1 in first_test_GeoTIFF.py file
# Link: https://chris35wills.github.io/courses/PythonPackages_matplotlib/matplotlib_3d/
img = imageio.imread('/home/nemish/BeCode/BeCode_Projects/3d-houses/Test.tif')

ny, nx = img.shape

x = np.linspace(0, 1, nx)
y = np.linspace(0, 1, ny)
xv, yv = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
dem3d = ax.plot_surface(xv, yv, img, cmap='winter', linewidth=0)
plt.show()
