import plotly.graph_objects as go
import math
from pyquaternion import Quaternion
cube = [[[-1, -1, -1], [-1, -1, 1], [-1, 1, 1], [-1, 1, -1]],
        [[1, -1, -1], [1, -1, 1], [1, 1, 1], [1, 1, -1]],
        [[-1, -1, -1], [-1, -1, 1], [1, -1, 1], [1, -1, -1]],
        [[-1, 1, -1], [-1, 1, 1], [1, 1, 1], [1, 1, -1]],
        [[-1, -1, -1], [-1, 1, -1], [1, 1, -1], [1, -1, -1]],
        [[-1, -1, 1], [-1, 1, 1], [1, 1, 1], [1, -1, 1]]]

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
def get_q(axis,theta):
    q = Quaternion([math.cos(theta/2)] + [math.sin(theta/2) * x for x in axis])
    return q

def rotate_point(point,q):
    point_q = Quaternion([0]+point)
    rotated_q = q*point_q*q.conjugate
    return [rotated_q[i] for i in [1,2,3]]

def rotate_face(face,q):
    return [rotate_point(point,q) for point in face]
def rotate_shape(faces,q):
    return [rotate_face(face,q) for face in faces]



def cube_graph(theta):
    axis = [1,1,1/2]
    # theta = math.pi/3
    q = get_q(axis,theta)
    q = q.normalised
    cube_rotated=rotate_shape(cube,q)
    fig = plot_faces(cube_rotated)
    return fig

