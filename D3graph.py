import plotly.graph_objs as go

def create_d3graph():
    trace1= go.Scatter3d(
        x = [9,1,None,8,5,1], y = [1,8,None, 2, 4, 8],
        z = [11,3,None, 8,15, 3],
        mode = 'lines'
    )
    labels = ['mark1','mark2', 'mark3', 'mark4']
    trace2= go.Scatter3d(
        x = [9,8,5,1], y = [1, 2, 4, 8],
        z = [11, 8,15, 3],
        mode='markers',marker=dict(symbol='circle',
                                size=15,
                                color='blue',
                                
                                line=dict(color='rgb(50,50,50)', width=0.5)
                                ),
                text=labels,
                hoverinfo='text'
    )
    axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )

    layout = go.Layout(
            title="Disease",
            width=1400,
            height=800,
            showlegend=False,
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
            ),
        margin=dict(
            t=100
        ),
        hovermode='closest',
        )

    data = [trace1,trace2]
    fig = go.Figure(data = data, layout=layout)

    fig.show()

create_d3graph()