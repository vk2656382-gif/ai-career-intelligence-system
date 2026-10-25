import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Career Intelligence",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #10152c, #192b4d);
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #111a30;
}
h1, h2, h3 {
    color: #7dd3fc;
}
div[data-testid="stMetric"] {
    background: #202e4c;
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎯 AI Career Intelligence System")
st.caption("Understand Your Skills • Discover Your Future")

st.info(
    "Explore career options using your interests, skills and assessment scores. "
    "Recommendations are guidance, not guaranteed predictions."
)

st.sidebar.header("👩‍🎓 Student Profile")

name = st.sidebar.text_input("Student Name", "Student")
education = st.sidebar.selectbox(
    "Education",
    ["BCA", "B.Tech", "B.Sc", "B.Com", "BA", "Other"]
)

interest = st.sidebar.selectbox(
    "Main Interest",
    [
        "Artificial Intelligence",
        "Data Science",
        "Software Development",
        "Cybersecurity",
        "Web Development",
        "UI/UX Design"
    ]
)

st.sidebar.subheader("📊 Assess Your Skills")

python_score = st.sidebar.slider("Python", 0, 100, 65)
math_score = st.sidebar.slider("Mathematics", 0, 100, 60)
logic_score = st.sidebar.slider("Logical Reasoning", 0, 100, 70)
communication = st.sidebar.slider("Communication", 0, 100, 75)
creativity = st.sidebar.slider("Creativity", 0, 100, 80)
data_score = st.sidebar.slider("Data Analysis", 0, 100, 55)

skills = {
    "Python": python_score,
    "Mathematics": math_score,
    "Logical Reasoning": logic_score,
    "Communication": communication,
    "Creativity": creativity,
    "Data Analysis": data_score
}

career_requirements = {
    "AI/ML Engineer": {
        "Python": 85,
        "Mathematics": 85,
        "Logical Reasoning": 80,
        "Communication": 60,
        "Creativity": 65,
        "Data Analysis": 80
    },
    "Data Analyst": {
        "Python": 65,
        "Mathematics": 70,
        "Logical Reasoning": 75,
        "Communication": 75,
        "Creativity": 60,
        "Data Analysis": 90
    },
    "Software Developer": {
        "Python": 85,
        "Mathematics": 65,
        "Logical Reasoning": 85,
        "Communication": 65,
        "Creativity": 75,
        "Data Analysis": 55
    },
    "Cybersecurity Analyst": {
        "Python": 70,
        "Mathematics": 70,
        "Logical Reasoning": 90,
        "Communication": 65,
        "Creativity": 65,
        "Data Analysis": 65
    },
    "Web Developer": {
        "Python": 60,
        "Mathematics": 50,
        "Logical Reasoning": 70,
        "Communication": 65,
        "Creativity": 85,
        "Data Analysis": 45
    },
    "UI/UX Designer": {
        "Python": 25,
        "Mathematics": 40,
        "Logical Reasoning": 65,
        "Communication": 80,
        "Creativity": 95,
        "Data Analysis": 40
    }
}

def calculate_match(student_skills, requirements):
    differences = [
        abs(student_skills[key] - requirements[key])
        for key in student_skills
    ]
    return round(max(0, 100 - sum(differences) / len(differences)), 1)

career_matches = {
    career: calculate_match(skills, requirements)
    for career, requirements in career_requirements.items()
}

career_df = pd.DataFrame({
    "Career": list(career_matches.keys()),
    "Profile Alignment (%)": list(career_matches.values())
}).sort_values("Profile Alignment (%)", ascending=False)

st.subheader(f"👋 Welcome, {name or 'Student'}!")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Student Dashboard",
    "🎯 Career Explorer",
    "🔍 Skill Gap Analysis",
    "🗺️ Learning Roadmap"
])

with tab1:
    st.subheader("Your Skill Overview")

    average_score = round(sum(skills.values()) / len(skills), 1)
    strongest_skill = max(skills, key=skills.get)
    developing_skill = min(skills, key=skills.get)

    c1, c2, c3 = st.columns(3)
    c1.metric("Average Assessment Score", f"{average_score}%")
    c2.metric("Highest Scoring Skill", strongest_skill)
    c3.metric("Skill to Develop", developing_skill)

    skill_df = pd.DataFrame({
        "Skill": list(skills.keys()),
        "Score": list(skills.values())
    })

    fig = px.bar(
        skill_df,
        x="Skill",
        y="Score",
        color="Score",
        range_y=[0, 100],
        title="Your Assessed Skills",
        text="Score",
        color_continuous_scale="Blues"
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(
        r=list(skills.values()),
        theta=list(skills.keys()),
        fill="toself",
        name="Your Skills"
    ))
    radar.update_layout(
        title="Student Skill Radar",
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        template="plotly_dark"
    )
    st.plotly_chart(radar, use_container_width=True)

    st.caption(
        "Scores are self-reported or entered assessment scores, "
        "not independently verified measures of ability."
    )

with tab2:
    st.subheader("🎯 Career Recommendations")

    st.write(
        "Career options are ranked by how closely your entered skill profile "
        "matches the illustrative skill requirements."
    )

    st.dataframe(
        career_df,
        use_container_width=True,
        hide_index=True
    )

    selected_career = st.selectbox(
        "Explore a Career",
        list(career_requirements.keys())
    )

    st.markdown(f"### {selected_career}")

    required = career_requirements[selected_career]

    gaps = {
        skill: max(0, required[skill] - skills[skill])
        for skill in skills
    }

    if career_matches[selected_career] >= 75:
        st.success("Your profile shows relatively strong alignment with this career.")
    else:
        st.info(
            "This career may still be worth exploring. "
            "Review its requirements and your learning interests."
        )

    st.write("**Why explore this career?**")

    if selected_career == "AI/ML Engineer":
        st.write("Explore Python, mathematics, data preparation and machine learning.")
    elif selected_career == "Data Analyst":
        st.write("Explore data interpretation, SQL, spreadsheets and visualization.")
    elif selected_career == "Software Developer":
        st.write("Explore programming, algorithms, software design and testing.")
    elif selected_career == "Cybersecurity Analyst":
        st.write("Explore networking, operating systems, security fundamentals and scripting.")
    elif selected_career == "Web Developer":
        st.write("Explore HTML, CSS, JavaScript and backend development.")
    else:
        st.write("Explore user research, wireframing, accessibility and interface design.")

    st.write("**Selected interest:**", interest)
    st.write("**Education:**", education)

with tab3:
    st.subheader("🔍 Skill Gap Analysis")

    selected = st.selectbox(
        "Choose a career to analyze skill gaps",
        list(career_requirements.keys()),
        key="gap_career"
    )

    target = career_requirements[selected]

    gap_df = pd.DataFrame({
        "Skill": list(skills.keys()),
        "Current Score": [skills[k] for k in skills],
        "Illustrative Target": [target[k] for k in skills]
    })

    gap_df["Gap"] = (
        gap_df["Illustrative Target"] - gap_df["Current Score"]
    ).clip(lower=0)

    fig_gap = px.bar(
        gap_df,
        x="Skill",
        y=["Current Score", "Illustrative Target"],
        barmode="group",
        range_y=[0, 100],
        title=f"Your Skills vs {selected} Reference Profile",
        template="plotly_dark"
    )
    st.plotly_chart(fig_gap, use_container_width=True)

    st.write("### Priority Areas to Develop")

    priorities = gap_df[gap_df["Gap"] > 0].sort_values(
        "Gap", ascending=False
    )

    if priorities.empty:
        st.success("Your entered scores meet or exceed all illustrative targets.")
    else:
        st.dataframe(
            priorities[["Skill", "Current Score", "Illustrative Target", "Gap"]],
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "Targets are illustrative project settings, not official industry "
        "standards or hiring cutoffs."
    )

with tab4:
    st.subheader("🗺️ Your Learning Roadmap")

    roadmap = {
        "AI/ML Engineer": [
            "Python fundamentals",
            "Mathematics and statistics",
            "NumPy and Pandas",
            "Machine learning algorithms",
            "Build an AI project",
            "Document projects in a portfolio"
        ],
        "Data Analyst": [
            "Excel or Google Sheets",
            "SQL fundamentals",
            "Python and Pandas",
            "Data visualization",
            "Build an analytics project",
            "Create a project portfolio"
        ],
        "Software Developer": [
            "Learn one programming language",
            "Practice problem-solving",
            "Learn data structures",
            "Understand databases",
            "Build and test an application",
            "Document projects in a portfolio"
        ],
        "Cybersecurity Analyst": [
            "Networking fundamentals",
            "Linux and operating systems",
            "Security fundamentals",
            "Python scripting",
            "Practice in legal learning labs",
            "Document security projects"
        ],
        "Web Developer": [
            "HTML fundamentals",
            "CSS and responsive design",
            "JavaScript",
            "Backend fundamentals",
            "Databases and APIs",
            "Deploy a portfolio website"
        ],
        "UI/UX Designer": [
            "Understand user-centered design",
            "Learn visual design principles",
            "Practice wireframing",
            "Study accessibility",
            "Create prototype projects",
            "Build a design portfolio"
        ]
    }

    st.write(f"### Roadmap: {selected_career if 'selected_career' in globals() else interest}")

    roadmap_career = st.selectbox(
        "Select your learning goal",
        list(roadmap.keys()),
        key="roadmap_choice"
    )

    for i, step in enumerate(roadmap[roadmap_career], 1):
        st.checkbox(f"Step {i}: {step}", key=f"roadmap_{roadmap_career}_{i}")

    st.info(
        "Start with the fundamentals, build small projects, and review "
        "your progress regularly. The roadmap is a starting point, "
        "not a guaranteed timeline for employment."
    )

st.divider()
st.caption("AI Career Intelligence System | Student Career Exploration Project")
