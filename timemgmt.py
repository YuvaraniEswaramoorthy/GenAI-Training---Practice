import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(
    page_title="Personalized Daily Scheduler",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for enhanced aesthetics ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green */
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextArea, .stTextInput, .stNumberInput, .stSelectbox {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 5px;
    }
    .task-card {
        background-color: #ffffff;
        border-left: 5px solid #4CAF50; /* Green border for tasks */
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .schedule-entry {
        background-color: #e0f2f7; /* Light blue for schedule */
        border-left: 5px solid #2196F3; /* Blue border for schedule */
        padding: 10px;
        margin-bottom: 5px;
        border-radius: 6px;
    }
    .header-style {
        font-family: 'Inter', sans-serif;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
    }
    .subheader-style {
        font-family: 'Inter', sans-serif;
        color: #34495e;
        margin-top: 20px;
        border-bottom: 2px solid #ccc;
        padding-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State Initialization ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# --- Helper Functions ---
def add_task(task_name, priority, estimated_time):
    """Adds a new task to the session state."""
    if task_name and estimated_time > 0:
        st.session_state.tasks.append({
            'name': task_name,
            'priority': priority,
            'estimated_time_minutes': estimated_time,
            'completed': False
        })
        st.success(f"Task '{task_name}' added successfully!")
    else:
        st.error("Please enter a task name and a valid estimated time.")

def clear_tasks():
    """Clears all tasks from the session state."""
    st.session_state.tasks = []
    st.info("All tasks cleared.")

def generate_schedule(tasks, start_time_str="09:00"):
    """
    Generates a time-blocked schedule based on task priorities and estimated times.
    Tasks are sorted by priority (High, Medium, Low) and then by estimated time (shortest first).
    """
    if not tasks:
        return []

    # Map priority to a numerical value for sorting
    priority_map = {"High": 1, "Medium": 2, "Low": 3}
    sorted_tasks = sorted(
        tasks,
        key=lambda x: (priority_map.get(x['priority'], 4), x['estimated_time_minutes'])
    )

    schedule = []
    try:
        current_time = datetime.strptime(start_time_str, "%H:%M")
    except ValueError:
        st.error("Invalid start time format. Please use HH:MM (e.g., 09:00).")
        return []

    for task in sorted_tasks:
        end_time = current_time + timedelta(minutes=task['estimated_time_minutes'])
        schedule.append({
            'start_time': current_time.strftime("%H:%M"),
            'end_time': end_time.strftime("%H:%M"),
            'task': task['name'],
            'priority': task['priority'],
            'duration': task['estimated_time_minutes']
        })
        current_time = end_time # Set the start of the next task to the end of the current one

    return schedule

def get_productivity_insights(tasks, schedule):
    """Provides productivity insights based on input tasks and generated schedule."""
    total_estimated_time = sum(task['estimated_time_minutes'] for task in tasks)
    num_tasks = len(tasks)

    insights = []

    if num_tasks == 0:
        insights.append("Start by adding your daily tasks to get personalized insights!")
        return insights

    insights.append(f"**Total tasks planned:** {num_tasks}")
    insights.append(f"**Total estimated work time:** {total_estimated_time} minutes ({total_estimated_time // 60} hours and {total_estimated_time % 60} minutes)")

    high_priority_tasks = sum(1 for task in tasks if task['priority'] == 'High')
    if high_priority_tasks > 0:
        insights.append(f"You have **{high_priority_tasks} High priority tasks** today. Focus on these first!")
    else:
        insights.append("No High priority tasks identified. Great for tackling those important-but-not-urgent items!")

    if total_estimated_time > 8 * 60: # More than 8 hours of estimated work
        insights.append("🔔 **Heads up!** Your estimated workload for today is quite high. Consider breaking down larger tasks or delegating if possible to avoid burnout.")
    elif total_estimated_time < 4 * 60 and num_tasks > 0:
        insights.append("Looks like a manageable day! Consider adding a buffer for unexpected interruptions or deep work sessions.")

    if any(task['estimated_time_minutes'] > 120 for task in tasks): # Any task over 2 hours
        insights.append("💡 **Large tasks detected!** For tasks longer than 2 hours, try breaking them into smaller, more manageable sub-tasks. This can reduce procrastination and make progress feel more achievable.")

    return insights

# --- Main Application Layout ---
st.markdown('<h1 class="header-style">🗓️ Personalized Daily Task Scheduler</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #555;">Input your daily tasks, and let Gemini help you create an organized schedule!</p>', unsafe_allow_html=True)

# --- Sidebar for Task Input ---
with st.sidebar:
    st.markdown('<h2 class="subheader-style">➕ Add New Task</h2>', unsafe_allow_html=True)
    with st.form("task_form", clear_on_submit=True):
        task_name = st.text_input("Task Name", placeholder="e.g., Prepare presentation slides")
        priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=0)
        estimated_time = st.number_input("Estimated Time (minutes)", min_value=5, max_value=480, value=60, step=5)
        submitted = st.form_submit_button("Add Task")
        if submitted:
            add_task(task_name, priority, estimated_time)

    st.markdown("---")
    st.markdown('<h2 class="subheader-style">⚙️ Settings</h2>', unsafe_allow_html=True)
    schedule_start_time = st.text_input("Schedule Start Time (HH:MM)", value="09:00", max_chars=5)
    st.markdown("---")
    if st.button("Clear All Tasks", help="Removes all tasks from the list and schedule."):
        clear_tasks()

# --- Main Content Area ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h2 class="subheader-style">📝 Your Current Tasks</h2>', unsafe_allow_html=True)
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            st.markdown(f"""
                <div class="task-card">
                    <strong>{task['name']}</strong><br>
                    Priority: {task['priority']} | Est. Time: {task['estimated_time_minutes']} mins
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No tasks added yet. Use the sidebar to add your first task!")

with col2:
    st.markdown('<h2 class="subheader-style">⏰ Personalized Schedule</h2>', unsafe_allow_html=True)
    schedule = generate_schedule(st.session_state.tasks, schedule_start_time)
    if schedule:
        for entry in schedule:
            st.markdown(f"""
                <div class="schedule-entry">
                    <strong>{entry['start_time']} - {entry['end_time']}</strong>: {entry['task']} 
                    <span style="float: right; font-size: 0.9em; color: #666;">({entry['duration']} min)</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Add tasks and click 'Generate Schedule' to see your personalized plan!")
        st.warning("Please ensure the schedule start time is in HH:MM format (e.g., 09:00).")

st.markdown("---")

st.markdown('<h2 class="subheader-style">🧠 Productivity Insights & Tips</h2>', unsafe_allow_html=True)
productivity_insights = get_productivity_insights(st.session_state.tasks, schedule)
for insight in productivity_insights:
    st.markdown(f"- {insight}")

st.markdown("""
    <br>
    <h3 style="color: #34495e;">Time-Blocking Tips:</h3>
    <ul>
        <li><strong>Batch Similar Tasks:</strong> Group emails, calls, or administrative tasks together to minimize context switching.</li>
        <li><strong>Schedule Breaks:</strong> Incorporate short breaks (5-10 minutes) every 60-90 minutes to maintain focus and energy.</li>
        <li><strong>Deep Work Blocks:</strong> Dedicate uninterrupted blocks of time (1-2 hours) for your most important, high-priority tasks. Turn off notifications during these times.</li>
        <li><strong>Flexibility is Key:</strong> While time-blocking provides structure, be prepared to adjust your schedule if unexpected urgent tasks arise.</li>
        <li><strong>Review and Reflect:</strong> At the end of the day, review your schedule and actual progress. This helps you refine your time estimates and planning for future days.</li>
    </ul>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Powered by Gemini for personalized scheduling and insights.")

