import plotly.graph_objects as go
import math
import numpy as np
from pyquaternion import Quaternion


def get_q(axis, theta):
    q = Quaternion([math.cos(theta/2)] + [math.sin(theta/2) * x for x in axis])
    return q
def rotate_point(point, q):
  point_q = Quaternion([0]+list(point))
  rotated_q = q*point_q*q.conjugate
  return [rotated_q[i] for i in [1, 2, 3]]
def rotate_face(face, q):
    return [rotate_point(point, q) for point in face]
def rotate_shape(faces, q):
    return [rotate_face(face, q) for face in faces]

cube = [[[-1, -1, -1], [-1, -1, 1], [-1, 1, 1], [-1, 1, -1]],
        [[1, -1, -1], [1, -1, 1], [1, 1, 1], [1, 1, -1]],
        [[-1, -1, -1], [-1, -1, 1], [1, -1, 1], [1, -1, -1]],
        [[-1, 1, -1], [-1, 1, 1], [1, 1, 1], [1, 1, -1]],
        [[-1, -1, -1], [-1, 1, -1], [1, 1, -1], [1, -1, -1]],
        [[-1, -1, 1], [-1, 1, 1], [1, 1, 1], [1, -1, 1]]]

delta = 0.05
centre_block = [np.array([-0.5, -0.5, 1.5+delta]), np.array([-0.5, 0.5, 1.5+delta]),
                np.array([0.5, 0.5, 1.5+delta]), np.array([0.5, -0.5, 1.5+delta])]
x = 1 + delta
translations = [np.array([0, 0, 0]), np.array([x, 0, 0]), np.array([-x, 0, 0]),
                np.array([0, x, 0]), np.array([x, x, 0]), np.array([-x, x, 0]),
                np.array([0, -x, 0]), np.array([x, -x, 0]
                                               ), np.array([-x, -x, 0])
                ]
cube_faces = [[point + x for point in centre_block] for x in translations]
cube_faces1 = [[point-np.array([0, 0, 3+2*delta])
                for point in block] for block in cube_faces]
qs = [get_q(axis, math.pi/2)
      for axis in [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]]
rubik = [rotate_shape(cube_faces, q) for q in qs]+[cube_faces, cube_faces1]


class Block():
  def __init__(self, points, color):
    self.points = points
    self.color = color
    self.centre = np.array(self.points).mean(axis=0)

  def rotate(self, q):
    self.points = [rotate_point(point, q) for point in self.points]

  def trace(self):
    return face_3d(self.points, self.color)


class Rubik():
  def __init__(self, blocks):
    self.blocks = blocks

  def rotate(self, q):
    [block.rotate(q) for block in self.blocks]

  def get_centres(self):
    centres = [block.centre for block in self.blocks]
    return np.array(centres)

  def rotate_left(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([1, 0, 0], theta)
    for block in [R.blocks[i] for i in np.where(R.get_centres()[:, 0] < -0.9)[0]]:
      block.rotate(q)

  def rotate_right(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([-1, 0, 0], theta)
    for block in [R.blocks[i] for i in np.where(R.get_centres()[:, 0] > 0.9)[0]]:
      block.rotate(q)

  def rotate_back(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([0, 1, 0], theta)
    for block in [R.blocks[i] for i in np.where(R.get_centres()[:, 1] > 0.9)[0]]:
      block.rotate(q)

  def rotate_front(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([0, -1, 0], theta)
    for block in [R.blocks[i] for i in np.where(R.get_centres()[:, 1] < -0.9)[0]]:
      block.rotate(q)

  def rotate_bottom(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([0, 0, 1], theta)
    for block in [R.blocks[i] for i in np.where(R.get_centres()[:, 2] > 0.9)[0]]:
      block.rotate(q)

  def rotate_top(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([0, 0, -1], theta)
    for block in [R.blocks[i] for i in np.where(R.get_centres()[:, 2] < -0.9)[0]]:
      block.rotate(q)

  def plot(self):
    fig = go.Figure()
    [fig.add_trace(block.trace()) for block in self.blocks]
    lim = -3
    axis_params = dict(range=[-lim, lim],
                       showbackground=False,
                       showticklabels=False,
                       showspikes=False,)
    fig.update_layout(scene=dict(
        xaxis=axis_params,
        yaxis=axis_params,
        zaxis=axis_params,))
    return fig
def shape_trace(shape):
    x = [tup[0] for tup in shape]
    y = [tup[1] for tup in shape]
    return go.Scatter(x=x+[x[0]],
                            y=y+[y[0]],
                            fill="toself",
                            visible=True,
                            showlegend=False,)

def plot_faces(faces):
    lim = 2.5
    fig = go.Figure()
    for face in faces:
        fig.add_trace(shape_trace(face))
    fig.update_layout(xaxis_range = (-lim,lim),
                    yaxis_range = (-lim,lim),
                    height=500,
                    width=500)
    return fig






def face_3d(face, color='red'):
  x = [point[0] for point in face]
  y = [point[1] for point in face]
  z = [point[2] for point in face]
  trace = go.Scatter3d(
      x=x,
      y=y,
      z=z,
      line_color=color,
      showlegend=False,
      surfaceaxis=0,
      hoverinfo='skip',
      mode='lines')
  return trace


def cube_graph(theta):
    axis = [1,1,1/2]
    # theta = math.pi/3
    q = get_q(axis,theta)
    q = q.normalised
    cube_rotated=rotate_shape(cube,q)
    fig = plot_faces(cube_rotated)
    return fig

def plot_rubiks():
    faces = [rotate_shape(cube_faces, q) for q in qs]+[cube_faces, cube_faces1]
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
    R = Rubik([Block(block, color) for color, cube_faces in zip(
        colors, faces) for block in cube_faces])
    R.rotate(get_q([1, 1, 1], 0.01))
    fig = R.plot()
    return fig
