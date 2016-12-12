import numpy as np
import matplotlib.pyplot as plt

im_size = 512

# the big triangle
t0 = [[0, 0], [1, 0], [0, 1]]
# three small triangles
t1 = [[0, 0], [.5, 0], [0, .5]]
t2 = [[.5, 0], [1, 0], [.5, .5]]
t3 = [[0, .5], [.5, .5], [0, 1]]
T = [t1, t2, t3]


# affine transformation matrices
def get_affine(x, y, scale):
    homo_x = np.concatenate([np.asarray(x)*scale, np.ones((3,1))], axis=1).T
    homo_y = np.concatenate([np.asarray(y)*scale, np.ones((3,1))], axis=1).T
    return np.dot(homo_y, np.linalg.inv(homo_x))

A = []
for t in T:
    A.append(get_affine(t0, t, im_size-1))

# initialize canvas
white = 255
canvas = np.ones((im_size, im_size))*white

# draw
iter_num = 30
for i in range(iter_num):
    new_canvas = np.zeros((im_size, im_size))
    for x1 in range(im_size):
        for x2 in range(im_size):
            if canvas[x1, x2] == white:
                for a in A:
                    y1, y2 = np.dot(a, [x1, x2, 1])[0:2]
                    if 0 <= y1 < im_size and 0 <= y2 < im_size:
                        new_canvas[y1, y2] = white
                    # else:
                        # print x1, x2, y1, y2
    canvas = new_canvas

plt.imshow(np.rot90(canvas), cmap='Greys_r')
plt.axis('off')
plt.show()
