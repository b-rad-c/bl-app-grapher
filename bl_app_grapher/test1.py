#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import PIL


x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

# output = window
# plt.show()

# output = file
# fig.savefig('myfig.png')

# output = bytesIO
# buf = BytesIO()
# fig.savefig(buf, format='png')

# output = canvas
fig.canvas.draw()
canvas = fig.canvas
plt.close()

dimensions = canvas.get_width_height()
print(dimensions)
img = PIL.Image.frombytes('RGB', dimensions,  canvas.tostring_rgb())
for x in range(dimensions[0]):
    for y in range(dimensions[1]):
        print(img.getpixel((x, y)))

#breakpoint()