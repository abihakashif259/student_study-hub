import streamlit as st
import time
import random
import json

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="Student Study Hub", page_icon="🎓", layout="wide")

# =========================================================
# SAVE & LOAD FUNCTIONS
# =========================================================
def save_data():
    data = {
        "subjects": st.session_state.subjects,
        "tasks": st.session_state.tasks,
        "goals": st.session_state.goals,
        "badges": st.session_state.badges,
        "quiz_score": st.session_state.quiz_score,
        "quiz_attempts": st.session_state.quiz_attempts,
        "focus_minutes": st.session_state.focus_minutes
    }
    with open("studyspace_data.json", "w") as f:
        json.dump(data, f)

def load_data():
    try:
        with open("studyspace_data.json", "r") as f:
            data = json.load(f)
            st.session_state.subjects = data.get("subjects", {})
            st.session_state.tasks = data.get("tasks", [])
            st.session_state.goals = data.get("goals", [])
            st.session_state.badges = data.get("badges", [])
            st.session_state.quiz_score = data.get("quiz_score", 0)
            st.session_state.quiz_attempts = data.get("quiz_attempts", 0)
            st.session_state.focus_minutes = data.get("focus_minutes", 0)
    except FileNotFoundError:
        pass

# =========================================================
# SESSION STATE INIT
# =========================================================
if "subjects" not in st.session_state: st.session_state.subjects = {}
if "tasks" not in st.session_state: st.session_state.tasks = []
if "goals" not in st.session_state: st.session_state.goals = []
if "badges" not in st.session_state: st.session_state.badges = []
if "quiz_score" not in st.session_state: st.session_state.quiz_score = 0
if "quiz_attempts" not in st.session_state: st.session_state.quiz_attempts = 0
if "focus_minutes" not in st.session_state: st.session_state.focus_minutes = 0

# Load saved data at start
load_data()

# =========================================================
# HEADER
# =========================================================
st.title("🎓 Student Study Hub")
st.subheader("Your colorful space for learning, practice and growth ✨")

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", [
    "🏠 Home","📚 Subjects","📝 To-Do List","🕒 Focus Timer","🎯 Goals",
   "🏆 Progress & Badges","🌍 Language Learning","🔗 Useful Links",
    "⚙️ Tools","🎬 Streaming"
])

# =========================================================
# HOME
# =========================================================
if page == "🏠 Home":
    st.header("🌸 Welcome to StudySpace!")
    st.write("Study smarter, stay focused and enjoy learning. 💜")
    if st.button("💾 Save Progress"):
        save_data()
        st.success("Progress saved successfully!")

# =========================================================
# SUBJECTS
# =========================================================
elif page == "📚 Subjects":
    st.header("📚 My Subjects")
    subject = st.text_input("Enter subject name", placeholder="Example: Mathematics")
    topic = st.text_input("What do you need to study?", placeholder="Example: Algebra")
    if st.button("➕ Add Study Topic"):
        if subject.strip() and topic.strip():
            if subject not in st.session_state.subjects:
                st.session_state.subjects[subject] = []
            st.session_state.subjects[subject].append(topic)
            st.success(f"✨ {topic} added to {subject}!")
            save_data()
        else:
            st.warning("Please enter both subject and topic.")
    st.markdown("---")
    if st.session_state.subjects:
        for subj, topics in st.session_state.subjects.items():
            with st.expander(f"📖 {subj}"):
                for number, topic_name in enumerate(topics, 1):
                    st.write(f"{number}. {topic_name}")
    else:
        st.info("📚 No subjects added yet.")

# =========================================================
# TO-DO LIST
# =========================================================
elif page == "📝 To-Do List":
    st.header("📝 My Study To-Do List")
    new_task = st.text_input("Add a new task", placeholder="Example: Complete Math homework")
    if st.button("➕ Add Task"):
        if new_task.strip():
            st.session_state.tasks.append({"task": new_task, "done": False})
            st.success("✅ Task added!")
            save_data()
        else:
            st.warning("Please enter a task.")
    st.markdown("---")
    if st.session_state.tasks:
        for i, item in enumerate(st.session_state.tasks):
            checked = st.checkbox(item["task"], value=item["done"], key=f"task_{i}")
            st.session_state.tasks[i]["done"] = checked
        completed = sum(1 for task in st.session_state.tasks if task["done"])
        st.info(f"📊 Completed: {completed}/{len(st.session_state.tasks)} tasks")
        if completed == len(st.session_state.tasks):
            st.success("🎉 Amazing! All tasks completed!")
        save_data()
    else:
        st.info("📝 Your to-do list is empty.")

# =========================================================
# FOCUS TIMER
# =========================================================
elif page == "🕒 Focus Timer":
    st.header("🕒 Focus Timer")
    mode = st.radio("Choose mode:", ["Custom Minutes", "Pomodoro (25+5)"])

    if mode == "Custom Minutes":
        minutes = st.number_input("Focus minutes:", min_value=1, max_value=120, value=5, step=5)
        break_time = 0
    else:
        minutes = 25
        break_time = 5
        st.info("Pomodoro Mode: 25 min focus + 5 min break")

    if st.button("🚀 Start Focus"):
        st.success(f"🌟 Focus started for {minutes} minutes!")
        st.session_state.focus_minutes += minutes

        progress = st.progress(0)
        countdown_text = st.empty()

        total_seconds = minutes * 60
        for sec in range(total_seconds, 0, -1):
            mins, secs = divmod(sec, 60)
            countdown_text.markdown(f"⏱ **Time left: {mins:02d}:{secs:02d}**")
            progress.progress((total_seconds - sec + 1) / total_seconds)
            time.sleep(1)

        st.success("⏰ Focus session complete!")
        if break_time > 0:
            st.info(f"☕ Take a {break_time} min break!")

        if minutes >= 30 and "🔥 Focus Hero" not in st.session_state.badges:
            st.session_state.badges.append("🔥 Focus Hero")
        if st.session_state.focus_minutes >= 100 and "🌟 Focus Legend" not in st.session_state.badges:
            st.session_state.badges.append("🌟 Focus Legend")

        save_data()

# =========================================================
# GOALS
# =========================================================
elif page == "🎯 Goals":
    st.header("🎯 My Study Goals")
    goal = st.text_input("Enter your study goal", placeholder="Example: Finish Chapter 5")
    if st.button("➕ Add Goal"):
        if goal.strip():
            st.session_state.goals.append(goal)
            st.success("🎯 Goal added!")
            save_data()
        else:
            st.warning("Please enter a goal.")
    st.markdown("---")
    if st.session_state.goals:
        for i, goal_name in enumerate(st.session_state.goals, 1):
            st.write(f"🎯 **Goal {i}:** {goal_name}")
    else:
        st.info("🎯 No goals added yet.")

elif page == "🏆 Progress & Badges":
    st.header("🏆 My Progress")
    col1,col2 = st.columns(2)
    with col1: st.metric("⏱ Focus Minutes", st.session_state.focus_minutes)
    with col2: st.metric("🎯 Goals", len(st.session_state.goals))
    st.markdown("---")
    st.subheader("🏅 My Badges")
    if st.session_state.badges:
        for badge in st.session_state.badges:
            st.success(badge)
    else:
        st.info("🌱 No badges yet. Complete activities to earn badges!")

# =========================================================
# LANGUAGE LEARNING
# =========================================================
elif page == "🌍 Language Learning":
    st.header("🌍 Language Learning")
    st.write("Practice languages using these useful learning websites.")
    st.markdown("🦉 [Duolingo](https://www.duolingo.com)")
    st.markdown("🇬🇧 [BBC Learning English](https://www.bbc.co.uk/learningenglish)")
    st.markdown("🇸🇦 [Madinah Arabic](https://www.madinaharabic.com)")

# =========================================================
# USEFUL LINKS
# =========================================================
elif page == "🔗 Useful Links":
    st.header("🔗 Useful Study Links")
    st.markdown("📖 [Khan Academy](https://www.khanacademy.org)")
    st.markdown("📚 [Wikipedia](https://www.wikipedia.org)")
    st.markdown("🎓 [Google Scholar](https://scholar.google.com)")
elif page == "⚙️ Tools":
    st.header("⚙️ Quick Tools")
    choice = st.selectbox("Choose a tool:", ["Calculator","Today's Quote"])  # <-- yahan choice define ho raha hai

    if choice == "Calculator":
        st.subheader("🧮 Calculator")
        num1 = st.number_input("Enter first number")
        num2 = st.number_input("Enter second number")
        operation = st.selectbox("Choose operation", ["Add","Subtract","Multiply","Divide"])
        if st.button("Calculate"):
            if operation == "Add": result = num1 + num2
            elif operation == "Subtract": result = num1 - num2
            elif operation == "Multiply": result = num1 * num2
            else:
                if num2 == 0:
                    st.error("Cannot divide by zero.")
                    result = None
                else:
                    result = num1 / num2
            if result is not None:
                st.success(f"🎯 Result: {round(result, 4)}")  # short result

    elif choice == "Today's Quote":
        st.subheader("💜 Study Motivation")
        quotes = [
            "Education is the passport to the future. – Malcolm X",
            "The expert in anything was once a beginner.",
            "Success is the sum of small efforts repeated daily.",
            "Dream big, work hard, stay focused.",
            "Learning never exhausts the mind. – Leonardo da Vinci",
            "Believe in yourself and keep going! 🌟"
        ]
        st.info(random.choice(quotes))



    elif choice == "Today's Quote":
        st.subheader("💜 Study Motivation")
        quotes = [
            "Education is the passport to the future. – Malcolm X",
            "The expert in anything was once a beginner.",
            "Success is the sum of small efforts repeated daily.",
            "Dream big, work hard, stay focused.",
            "Learning never exhausts the mind. – Leonardo da Vinci",
            "Believe in yourself and keep going! 🌟"
        ]
        st.info(random.choice(quotes))

# =========================================================
# STREAMING
# =========================================================
elif page == "🎬 Streaming":
    st.header("🎬 Free Movie & Cartoon Streaming")
    st.write("You can explore free movies and cartoons on Plex.")
    st.markdown("🎥 [Plex Free Movies](https://www.plex.tv/watch-free)")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#888;'>Made with 💜 for students by Abiha Kashif| StudySpace 🎓</p>",
    unsafe_allow_html=True
)

