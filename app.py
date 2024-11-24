import streamlit as st
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.graph_objects as go
import time

st.set_page_config(page_title="TaskPrism", layout="wide", page_icon="📊")


# Helper functions
def generate_color_map(n_colors):
    """Generate a color map with distinct colors for resources."""
    cmap = plt.cm.get_cmap('tab20', n_colors)  # Use 'tab20' for distinct colors
    return {i: mcolors.rgb2hex(cmap(i)[:3]) for i in range(n_colors)}


def generate_graph(n_nodes, prob):
    """Generate a random graph and its adjacency matrix."""
    if n_nodes < 1:
        st.error("Number of nodes must be at least 1!")
        return None, None
    if prob < 0 or prob > 1:
        st.error("Graph density must be between 0 and 1!")
        return None, None

    G = nx.fast_gnp_random_graph(n_nodes, prob)
    adj_matrix = nx.to_numpy_array(G, dtype=int)
    return G, adj_matrix


def greedy_coloring(adj_matrix):
    """Assign colors to nodes using a greedy graph coloring algorithm."""
    n_nodes = len(adj_matrix)
    colors = [-1] * n_nodes  # -1 means uncolored
    for node in range(n_nodes):
        # Finding colors of adjacent nodes
        neighbor_colors = {colors[neighbor] for neighbor in np.where(adj_matrix[node] == 1)[0] if colors[neighbor] != -1}
        # Assigning the lowest available color
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[node] = color
    return colors


# Main application code
def main():
    # Centered Title
    st.markdown("<h1 style='text-align: center;'>📊 TaskPrism</h1>", unsafe_allow_html=True)

    # Subtitle
    st.markdown("<h3 style='text-align: center;'>Allocate Tasks with Graph Colouring</h3>", unsafe_allow_html=True)

    # How-To Section (Shortened)
    st.write("### 📋 How to Use TaskPrism")
    st.write("""
    1. **Set Details:**  
       Use the sidebar to define tasks, resources, durations, deadlines, and priorities.
    
    2. **Generate Results:**  
       Click **"Generate"** to view the graph and Gantt chart.

    3. **Explore Outputs:**  
       - **Graph:** Task dependencies and resources.  
       - **Timeline:** Task schedule.
       - **Download Data:**Export as CSV.

    """)

    # Sidebar Section
    st.sidebar.header("Task Allocation Parameters")
    n_nodes = st.sidebar.number_input(
        "Number of tasks (nodes):", min_value=1, max_value=20, value=5, step=1
    )
    prob = st.sidebar.slider(
        "Graph density (probability of dependency):", 0.0, 1.0, 0.5, 0.01
    )
    n_colors = st.sidebar.number_input(
        "Number of resources (colors):", min_value=1, max_value=20, value=10, step=1
    )

    # Task details
    task_duration = {}
    task_deadlines = {}
    task_descriptions = {}
    task_priorities = {}
    for node in range(n_nodes):
        with st.sidebar.expander(f"Task {node + 1} Details"):
            task_duration[node] = st.slider(f"Duration of task", 1, 10, 3, key=f"duration_{node}")
            task_deadlines[node] = st.slider(f"Deadline", 1, 20, 10, key=f"deadline_{node}")
            task_descriptions[node] = st.text_input(f"Description", f"Task {node + 1}", key=f"desc_{node}")
            task_priorities[node] = st.slider(f"Priority (1 = highest)", 1, 10, 1, key=f"priority_{node}")

    # Instruction to click the button on the main page
    st.sidebar.write("🔘 **After setting the parameters, click the 'Generate' button on the main page.**")

    # Generate results
    if st.button("Generate Graph and Allocate Tasks", key="generate", help="Click to generate the graph and allocate tasks"):
        with st.spinner("Generating the graph and allocating resources..."):
            time.sleep(1)

            # Generate graph and adjacency matrix
            G, adj_matrix = generate_graph(n_nodes, prob)
            if G is None or adj_matrix is None:
                st.error("Failed to generate the graph. Please check the parameters.")
            else:
                st.header("Generated Task Dependency Graph")
                st.subheader("Adjacency Matrix")
                st.dataframe(pd.DataFrame(adj_matrix, dtype=int))

                # Perform graph coloring
                try:
                    assigned_colors = greedy_coloring(adj_matrix)
                    color_map = generate_color_map(n_colors)
                    node_colors = [color_map[assigned_colors[node] % n_colors] for node in range(n_nodes)]

                    # Sort tasks by priority
                    sorted_tasks = sorted(range(n_nodes), key=lambda x: task_priorities[x])

                    # Plot the graph
                    st.subheader("Task Dependency Visualization")
                    fig, ax = plt.subplots(figsize=(12, 8))
                    nx.draw(
                        G,
                        with_labels=True,
                        node_color=node_colors,
                        node_size=500,
                        font_size=12,
                        font_color="white",
                        edge_color="gray",
                        ax=ax,
                        arrows=True,
                        pos=nx.spring_layout(G)
                    )
                    st.pyplot(fig)

                    # Resource Allocation
                    st.subheader("Resource Allocation")
                    allocation_df = pd.DataFrame(
                        [assigned_colors],
                        columns=[f"Task {i + 1}" for i in range(n_nodes)],
                        index=["Resource Allocation"]
                    )
                    st.dataframe(allocation_df)

                    # Calculate task start times
                    start_times = {task: 0 for task in range(n_nodes)}
                    for task in sorted_tasks:
                        dependent_tasks = np.where(adj_matrix[task] == 1)[0]
                        if dependent_tasks.size > 0:
                            start_times[task] = max(start_times[dep] + task_duration[dep] for dep in dependent_tasks)

                    # Gantt Chart
                    st.subheader("Task Execution Timeline")
                    gantt_data = []
                    for task in sorted_tasks:
                        gantt_data.append({
                            "Task": task_descriptions[task],
                            "Start": start_times[task],
                            "Finish": start_times[task] + task_duration[task],
                            "Resource": f"Resource {assigned_colors[task] + 1}",
                        })

                    fig = go.Figure()
                    for task in sorted_tasks:
                        fig.add_trace(go.Bar(
                            x=[gantt_data[task]["Finish"] - gantt_data[task]["Start"]],
                            y=[gantt_data[task]["Task"]],
                            base=gantt_data[task]["Start"],
                            orientation="h",
                            name=gantt_data[task]["Resource"],
                            marker=dict(color=color_map[assigned_colors[task]]),
                            hoverinfo="x+y+name"
                        ))

                    fig.update_layout(
                        title="Task Execution Schedule",
                        xaxis_title="Time (units)",
                        yaxis_title="Tasks",
                        barmode="stack",
                        showlegend=True,
                        xaxis=dict(showgrid=True),
                        height=600,
                    )

                    st.plotly_chart(fig)

                    # Check for overdue tasks
                    overdue_tasks = [f"Task {task + 1}" for task in sorted_tasks if start_times[task] + task_duration[task] > task_deadlines[task]]
                    if overdue_tasks:
                        st.error(f"The following tasks are overdue: {', '.join(overdue_tasks)}")

                    # Export to CSV
                    export_data = pd.DataFrame(gantt_data)
                    csv = export_data.to_csv(index=False)
                    st.download_button(
                        label="Download Task Execution Data",
                        data=csv,
                        file_name="task_execution_data.csv",
                        mime="text/csv"
                    )

                except Exception as e:
                    st.error(f"Error in task allocation: {e}")


if __name__ == "__main__":
    main()


