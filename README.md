# TaskPrism

TaskPrism is a resource/task allocation app using graph coloring. It helps optimize task scheduling and resource usage. 
You can view the live app [here](https://taskprism.streamlit.app).
# Task/Resource Allocation Using Graph Coloring

## Overview
This project demonstrates the use of graph coloring algorithms to optimize resource allocation in project management. By implementing a task allocation system, it ensures efficient task scheduling, minimizes resource conflicts, and helps project managers optimize resource usage. The system visualizes task dependencies and generates efficient execution schedules while considering task priorities, durations, and deadlines.

![Screenshot 2024-11-24 003301](https://github.com/user-attachments/assets/f0b9678a-e986-4540-b76d-f22abfdd333f)

![Screenshot 2024-11-23 235645](https://github.com/user-attachments/assets/b39aace1-c9d0-49f4-a6f9-50fa143f350d)
##  🛠️ Features
- **Dynamic Graph Generation**: Creates task dependency graphs with adjustable
 density
- **Resource Allocation**: Uses graph coloring algorithm to optimally assign resources to tasks
- **Interactive Visualizations**:
  - Task dependency graph visualization
  - Adjacency matrix representation
  - Interactive Gantt chart for task execution timeline
- **Task Management**:
  - Customizable task durations
  - Deadline setting
  - Priority assignment
  - Task descriptions
- **Analysis Tools**:
  - Automatic detection of overdue tasks
  - Resource allocation overview
  - Exportable task execution data

## ⚙️ Prerequisites
Required Python packages:
- streamlit
- numpy
- pandas
- networkx
- matplotlib
- plotly

## Installation
1. Clone the repository
2. Install required packages:
   ```
   pip install streamlit numpy pandas networkx matplotlib plotly
   ```

## 🖥️ Usage
1. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Use the sidebar to configure:
   - Number of tasks
   - Graph density (probability of dependencies between tasks)
   - Number of available resources
   - Individual task details (duration, deadline, description, priority)

3. Click "Generate Graph and Allocate Tasks" to:
   - View the task dependency graph
   - See resource allocation
   - Analyze the execution timeline
   - Check for potential scheduling conflicts

4. Export the task execution data as CSV for further analysis

## 📊 Key Visualizations

1. **Task Dependency Graph**
   - Nodes represent tasks
   - Edges represent dependencies
   - Colors represent assigned resources
   - Interactive visualization using NetworkX

2. **Gantt Chart**
   - Interactive timeline of task execution
   - Color-coded by resource
   - Shows task durations and dependencies
   - Built using Plotly

## 🚀 Future Enhancements
- Support for resource-specific constraints
- Multiple resource requirements per task
- Cost optimization
- Custom dependency definition
- Historical data analysis
- Resource load balancing
- Integration with project management tools

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
