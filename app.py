import streamlit as st
import plotly.graph_objects as go

# Create a title for the app
st.title("Visualize your Lead Flow")

# Create a function to create the Sankey diagram
def create_graph(MQL_touch_rate, response_rate, positive_response_rate, negative_response_rate, st=st):
    # output
    MQL = 100
    touched = round(MQL * MQL_touch_rate / 100)
    untouched = MQL - touched
    responded = round(touched * response_rate / 100)
    no_response = touched - responded
    yes = round(responded * positive_response_rate / 100)
    no = round(responded * negative_response_rate / 100)
    yes_ish = responded - yes - no

    # configure visualization
    config = dict({
        'scrollZoom': True,
        'responsive': True
    })

    # Plot
    fig = go.Figure(data=[go.Sankey(
        arrangement = "snap",
        node = dict(
        pad = 10,
        thickness = 30,
        line = dict(color = "black", width = 0.5),
        label = ["MQL", "Touched", "Untouched", "Responded", "No Response", "Yes", "Yes-ish", "No"],
        color = ["#182B52","#1E77CC","#4DCCBD","#1E77CC","#FFB67B","#1E77CC","#63A8EA","#D81E5B"],
        hovertemplate='%{value} %{label}<extra></extra>',
        customdata = [MQL, touched, untouched, responded, no_response, yes, yes_ish, no],
        x = [0.1, 0.25, 0.25, 0.5, 0.9, 0.9, 0.9, 0.9],
        y = [0.1, 0.1, 0.25, 0.1, 0.5, 0.1, 0.2, 0.3],
        ),
        link = dict(
        source = [0, 0, 1, 1, 3, 3, 3, 2], # indices correspond to labels, eg A1, A2, A1, B1, ...
        target = [1, 2, 3, 4, 5, 6, 7, 4],
        value = [touched, untouched, responded, no_response, yes, yes_ish, no]
    ))])

    fig.update_layout(title_text="MQL Flow", font_size=10)
    # Show the plot in the st object
    st.plotly_chart(fig, use_container_width=True, config=config)

# Create a side bar with a title "Inputs"
st.sidebar.title("Inputs")

# Create inputs for the following metrics:
# MQL_touch_rate = 69 # What percentage of MQLs are contacted by sales
# response_rate = 16 # What percentage of contacted MQLs contacted by sales respond
# positive_response_rate = 50 # What percentage of responses are positive
# negative_response_rate = 30 # What percentage of responses are negative (note that the remaining percentage will be considered as "yes-ish")

st.sidebar.markdown("MQL Touch Rate: What percentage of MQLs are contacted by sales")
MQL_touch_rate = st.sidebar.slider("MQL Touch Rate", 0, 100, 69)
st.sidebar.markdown("Response Rate: What percentage of contacted MQLs contacted by sales respond")
response_rate = st.sidebar.slider("Response Rate", 0, 100, 16)
st.sidebar.markdown("Positive Response Rate: What percentage of responses are positive")
positive_response_rate = st.sidebar.slider("Positive Response Rate", 0, 100, 50)
st.sidebar.markdown("Negative Response Rate: What percentage of responses are negative (note that the remaining percentage will be considered as 'yes-ish')")
negative_response_rate = st.sidebar.slider("Negative Response Rate", 0, 100, 30)


# Create a button to run the model. When the button is clicked, the variables will be passed to the state
if st.sidebar.button("Run Model"):
    st.experimental_set_query_params(MQL_touch_rate=MQL_touch_rate, response_rate=response_rate, positive_response_rate=positive_response_rate, negative_response_rate=negative_response_rate)
    # display the Sankey diagram in the main panel
    create_graph(MQL_touch_rate, response_rate, positive_response_rate, negative_response_rate, st=st)

# Add information about the author in an info box
st.sidebar.info(
    "This app is created by [MadKudu](https://www.madkudu.com/)."
    "The source code is available on [GitHub](https://github.com/francisbrero/mql_flow_visualization)"
)