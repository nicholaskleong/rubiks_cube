import plotly.graph_objects as go
import math
import numpy as np
from pyquaternion import Quaternion


def get_q(axis, theta):
  '''Get quaternion that represents rotation'''
  q = Quaternion([math.cos(theta/2)] + [math.sin(theta/2) * x for x in axis])
  return q
def rotate_point(point, q):
  '''Rotate a single 3D point by quaternion q'''
  point_q = Quaternion([0]+list(point))
  rotated_q = q*point_q*q.conjugate
  return [rotated_q[i] for i in [1, 2, 3]]
def rotate_face(face, q):
  '''Rotate a face by q'''
  return [rotate_point(point, q) for point in face]
def rotate_shape(faces, q):
  '''rotate a shape (list of faces) by q'''
  return [rotate_face(face, q) for face in faces]



def get_sticker_background(color='black'):
  '''Get a trace that provided black background'''
  qs = [get_q(axis, math.pi/2)
    for axis in [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]]
  eps = 0.01
  sticker_background = [np.array([1.5-eps, 1.5-eps, 1.5-eps]),
                        np.array([1.5-eps, -1.5+eps, 1.5-eps]),
                        np.array([-1.5+eps, 1.5-eps, 1.5-eps]),
                        np.array([-1.5+eps, -1.5+eps, 1.5-eps])]
  sticker_background1 = [
      point-np.array([0, 0, 3-2*eps]) for point in sticker_background]
  sticker_background_full = [rotate_face(
      sticker_background, q) for q in qs]+[sticker_background, sticker_background1]
  q=get_q([1, 1, 1], 0.0001)
  return [face_3d(rotate_face(face, q), color) for face in sticker_background_full]
class Block():
  '''Class for single sticker. 9 stickers to a face'''
  def __init__(self, points, color):
    self.points = points
    self.color = color
    self.centre = np.array(self.points).mean(axis=0)

  def get_state(self):
    state = [[point for point in self.points], self.color]
    return state

  def rotate(self, q):
    self.points = [rotate_point(point, q) for point in self.points]

  def trace(self):
    return face_3d(self.points, self.color)


class Rubik():
  def __init__(self, blocks):
    self.blocks = blocks

  def get_state(self):
    state = [block.get_state() for block in self.blocks]
    return state

  def load_state(self, state):
    self.blocks = [Block(*block) for block in state]

  def rotate(self, q):
    [block.rotate(q) for block in self.blocks]

  def get_centres(self):
    centres = [block.centre for block in self.blocks]
    return np.array(centres)

  def rotate_left(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([-1, 0, 0], theta)
    for block in [self.blocks[i] for i in np.where(self.get_centres()[:, 0] < -0.9)[0]]:
      block.rotate(q)

  def rotate_right(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([1, 0, 0], theta)
    for block in [self.blocks[i] for i in np.where(self.get_centres()[:, 0] > 0.9)[0]]:
      block.rotate(q)

  def rotate_back(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([0, 1, 0], theta)
    for block in [self.blocks[i] for i in np.where(self.get_centres()[:, 1] > 0.9)[0]]:
      block.rotate(q)

  def rotate_front(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([0, -1, 0], theta)
    for block in [self.blocks[i] for i in np.where(self.get_centres()[:, 1] < -0.9)[0]]:
      block.rotate(q)

  def rotate_down(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([0, 0, 1], theta)
    for block in [self.blocks[i] for i in np.where(self.get_centres()[:, 2] > 0.9)[0]]:
      block.rotate(q)

  def rotate_up(self, clockwise=True):
    theta = (1 if clockwise else -1) * math.pi/2
    q = get_q([0, 0, -1], theta)
    for block in [self.blocks[i] for i in np.where(self.get_centres()[:, 2] < -0.9)[0]]:
      block.rotate(q)

  def plot(self):
    fig = go.Figure()
    [fig.add_trace(block.trace()) for block in self.blocks]
    lim = -3
    [fig.add_trace(trace) for trace in get_sticker_background()]
    axis_params = dict(range=[-lim, lim],
                       showbackground=False,
                       showticklabels=False,
                       showspikes=False,)
    fig.update_layout(scene=dict(
        xaxis=axis_params,
        yaxis=axis_params,
        zaxis=axis_params,
        camera=dict(
            eye=dict(x=0.8, y=0.8, z=0.8)
        )))
    return fig


def face_3d(face, color='red'):
  '''Plot face as trace in 3D scatter'''
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

def init_rubiks():
    '''Create list of blocks and rotate to get full rubiks cube'''
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
    faces = [rotate_shape(cube_faces, q)
                              for q in qs]+[cube_faces, cube_faces1]
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
    R = Rubik([Block(block, color) for color, cube_faces in zip(
        colors, faces) for block in cube_faces])
    R.rotate(get_q([1, 1, 1], 0.0001))
    return R

def plot_rubiks(state):
    '''Update plot to the configuration of state.'''
    R = Rubik(None)
    R.load_state(state)
    fig = R.plot()
    fig.update_layout(
      width=800,
      height=600,
      uirevision='fixed',
    )
    return fig
