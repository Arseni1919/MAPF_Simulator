import plotly.graph_objects as go
import plotly.express as px

import numpy as np

fig = go.Figure(
    data=[go.Scatter(x=[0, 1], y=[0, 1])],
    layout=go.Layout(
        xaxis=dict(range=[0, 5], autorange=False),
        yaxis=dict(range=[0, 5], autorange=False),
        title="Start Title",
        updatemenus=[dict(
                        type="buttons",
                        buttons=[dict(label="Play",
                                      method="animate",
                                      args=[None])
                                ]
                    )
        ]
    ),
    frames=[go.Frame(data=[go.Scatter(x=[1, 2], y=[1, 2])]),
            go.Frame(data=[go.Scatter(x=[1, 4], y=[1, 4])]),
            go.Frame(data=[go.Scatter(x=[3, 4], y=[3, 4])],
                     layout=go.Layout(title_text="End Title"))]
)

fig.show()

# fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16],
#                  animation_frame=[[10, 11, 12, 13, 14]])
# fig.show()

# Generate curve data
t = np.linspace(-1, 1, 100)
x = t + t ** 2
y = t - t ** 2
xm = np.min(x) - 1.5
xM = np.max(x) + 1.5
ym = np.min(y) - 1.5
yM = np.max(y) + 1.5
N = 50
s = np.linspace(-1, 1, N)
xx = s + s ** 2
yy = s - s ** 2


# Create figure
# fig = go.Figure(
#     data=[go.Scatter(x=x, y=y,
#                      mode="lines",
#                      line=dict(width=2, color="blue")),
#           go.Scatter(x=x, y=y,
#                      mode="lines",
#                      line=dict(width=2, color="blue"))],
#     layout=go.Layout(
#         xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
#         yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
#         title_text="Kinematic Generation of a Planar Curve", hovermode="closest",
#         updatemenus=[dict(type="buttons",
#                           buttons=[dict(label="Play",
#                                         method="animate",
#                                         args=[None])])]),
#     frames=[go.Frame(
#         data=[go.Scatter(
#             x=[xx[k]],
#             y=[yy[k]],
#             mode="markers",
#             marker=dict(color="red", size=10))])
#
#         for k in range(N)]
# )
#
# fig.show()