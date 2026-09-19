import streamlit as st
import sqlite3

# Database setup
conn = sqlite3.connect("studyspace.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS students_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    student_name TEXT,
    note_text TEXT
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS teachers_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id TEXT,
    teacher_name TEXT,
    note_text TEXT
)
""")
conn.commit()

# =========================================================
# LOGIN PROCESS
# =========================================================
st.sidebar.header("🔑 Login")
role = st.sidebar.selectbox("Login as:", ["Student", "Teacher"])
user_id = st.sidebar.text_input("Enter your ID")
user_name = st.sidebar.text_input("Enter your Name")
if not user_id or not user_name:
    st.warning("⚠️ Please enter your ID and Name to continue.")
else:
    st.success(f"Welcome {user_name} ({role})!")
    if role == "Student":
        pages = st.sidebar.radio("📚 Student Menu", [
        "🏠 Home","📖 My Notes","📝 To-Do List","🕒 Focus Timer",
        "📐 Maths","📘 English","🌍 Languages","🕌 Islamic Studies",
        "🌎 General Knowledge","🎮 Games","🎉 Fun Activities"
    ])

        if pages == "🏠 Home":
            st.header(f"👩‍🎓 Welcome Student {user_name}")
            st.write("This is your study dashboard.")

        elif pages == "📖 My Notes":
            st.header("📖 My Notes")
            note = st.text_area("Write your note")
            if st.button("Save Note"):
                c.execute("INSERT INTO students_notes (student_id, student_name, note_text) VALUES (?,?,?)",
                        (user_id, user_name, note))
                conn.commit()
                st.success("✅ Note saved!")
            st.subheader("Your Notes")
            rows = c.execute("SELECT note_text FROM students_notes WHERE student_id=?",(user_id,)).fetchall()
            for r in rows:
                st.write(f"- {r[0]}")

        elif pages == "📝 To-Do List":
            st.header("📝 To-Do List")
            if "tasks" not in st.session_state: st.session_state.tasks = []
            new_task = st.text_input("Add task")
            if st.button("Add Task"):
                st.session_state.tasks.append({"task": new_task, "done": False})
            for i, t in enumerate(st.session_state.tasks):
                st.checkbox(t["task"], key=f"task_{i}")

        elif pages == "🕒 Focus Timer":
            st.header("🕒 Focus Timer")
            minutes = st.number_input("Minutes", 1, 60, 25)
            if st.button("Start Focus"):
                st.success(f"Focus started for {minutes} minutes!")

        # ---------------- Extra Subjects ----------------
        elif pages == "📐 Maths":
            st.header("📐 Maths Resources")
            st.markdown("- [Khan Academy Maths](https://www.khanacademy.org/math)")
            st.markdown("- [Mr Barton Maths](https://www.mrbartonmaths.com)")
            st.markdown("- [Math Playground](https://www.mathplayground.com)")

        elif pages == "📘 English":
            st.header("📘 English Resources")
            st.markdown("- [BBC Learning English](https://www.bbc.co.uk/learningenglish)")
            st.markdown("- [Grammarly Blog](https://www.grammarly.com/blog)")
            st.markdown("- [Duolingo English](https://www.duolingo.com/course/en)")

        elif pages == "🌍 Languages":
            st.header("🌍 Language Learning")
            st.markdown("- [Duolingo](https://www.duolingo.com)")
            st.markdown("- [Busuu](https://www.busuu.com)")
            st.markdown("- [Memrise](https://www.memrise.com)")

        elif pages == "🕌 Islamic Studies":
            st.header("🕌 Islamic Studies")
            st.markdown("- [Islamic Quiz](https://islamicquiz.com)")
            st.markdown("- [Ilm Arena](https://ilmarena.com)")
            st.markdown("- [Muslim Trivia](https://muslimtrivia.com)")

        elif pages == "🌎 General Knowledge":
            st.header("🌎 General Knowledge")
            st.markdown("- [National Geographic Kids](https://kids.nationalgeographic.com)")
            st.markdown("- [Britannica Kids](https://kids.britannica.com)")
            st.markdown("- [GK Quiz](https://www.gkquiz.com)")

        elif pages == "🎮 Games":
            st.header("🎮 Educational Games")
            st.markdown("- [Cool Math Games](https://www.coolmathgames.com)")
            st.markdown("- [ABCya](https://www.abcya.com)")
            st.markdown("- [Fun Brain](https://www.funbrain.com)")

        elif pages == "🎉 Fun Activities":
            st.header("🎉 Fun Activities")
            st.markdown("- [Pinterest Crafts](https://www.pinterest.com)")
            st.markdown("- [Origami Club](https://www.origami-club.com)")
            st.markdown("- [DIY Science Experiments](https://www.sciencefun.org/kidszone/experiments)")


    # =========================================================
    # TEACHER PAGES
    # =========================================================
    elif role == "Teacher":
        pages = st.sidebar.radio("👨‍🏫 Teacher Menu", [
            "🏠 Home","📖 Teacher Notes","👩‍🎓 View Students' Notes"
        ])

        if pages == "🏠 Home":
            st.header(f"👨‍🏫 Welcome Teacher {user_name}")
            st.write("This is your teaching dashboard.")

        elif pages == "📖 Teacher Notes":
            st.header("📖 Teacher Notes")
            note = st.text_area("Write your teacher note")
            if st.button("Save Teacher Note"):
                c.execute("INSERT INTO teachers_notes (teacher_id, teacher_name, note_text) VALUES (?,?,?)",
                          (user_id, user_name, note))
                conn.commit()
                st.success("✅ Teacher note saved!")
            st.subheader("Your Notes")
            rows = c.execute("SELECT note_text FROM teachers_notes WHERE teacher_id=?",(user_id,)).fetchall()
            for r in rows:
                st.write(f"- {r[0]}")

        elif pages == "👩‍🎓 View Students' Notes":
            st.header("👩‍🎓 All Students' Notes")
            rows = c.execute("SELECT student_id, student_name, note_text FROM students_notes").fetchall()
            if rows:
                for r in rows:
                    st.write(f"ID: {r[0]} | Name: {r[1]} → {r[2]}")
            else:
                st.info("No student notes yet.")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown("<p style='text-align:center; color:#888;'>Made with 💜 | StudySpace Hub</p>", unsafe_allow_html=True)

