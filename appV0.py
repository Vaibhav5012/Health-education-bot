import streamlit as st
import uuid
from datetime import datetime

# ============================================
# AGENT TOOLS (FIXED)
# ============================================

def get_health_information(topic: str) -> dict:
    """Search Agent - Health Information"""
    health_db = {
        "diabetes": {
            "title": "Diabetes",
            "info": "Chronic condition affecting blood glucose regulation.",
            "types": ["Type 1: Autoimmune", "Type 2: Lifestyle-related", "Gestational: During pregnancy"],
            "mgmt": ["Regular exercise", "Healthy diet", "Weight management", "Regular monitoring"],
            "stats": "Affects 1 in 10 adults"
        },
        "vaccines": {
            "title": "Vaccines",
            "info": "Train immune system to fight diseases.",
            "benefits": ["Prevent serious disease", "Reduce transmission", "Save 2-3M lives/year"],
            "safety": "Rigorous testing; side effects mild and temporary",
            "stats": "Save 2-3 million lives annually"
        },
        "nutrition": {
            "title": "Nutrition",
            "info": "Good nutrition prevents chronic diseases.",
            "tips": ["5+ fruits/veggies daily", "Whole grains", "Lean proteins", "Healthy fats"],
            "tips2": ["Limit sugars", "Control portions", "Stay hydrated"],
            "stats": "Poor diet linked to 40% of chronic diseases"
        },
        "sleep": {
            "title": "Sleep",
            "info": "Essential for health, immunity, and cognition.",
            "recommended": "Adults: 7-9 hours daily",
            "tips": ["Consistent schedule", "Dark room", "Cool temperature", "Avoid screens before bed"],
            "benefits": ["Immune strength", "Memory consolidation", "Hormone regulation"],
            "stats": "Sleep deprivation increases disease risk by 30%"
        },
        "mental_health": {
            "title": "Mental Health",
            "info": "Psychological well-being is crucial.",
            "conditions": ["Depression", "Anxiety", "Stress", "Burnout"],
            "help": ["Therapy", "Exercise", "Meditation", "Social connections"],
            "stats": "1 in 5 adults experience mental illness yearly"
        }
    }
    
    topic_lower = topic.lower().strip()
    if topic_lower in health_db:
        return {"status": "success", **health_db[topic_lower]}
    
    available = ", ".join(health_db.keys())
    return {"status": "error", "msg": f"Try: {available}"}

def generate_quiz(topic: str) -> dict:
    """Quiz Agent - Generate Questions (FIXED)"""
    quizzes = {
        "diabetes": {
            "q": "What is the normal fasting blood glucose level?",
            "opts": ["Less than 100 mg/dL", "100-125 mg/dL", "More than 125 mg/dL"],
            "ans": 0,
            "exp": "Normal fasting glucose is less than 100 mg/dL. 100-125 indicates prediabetes."
        },
        "vaccines": {
            "q": "When do most vaccine side effects occur?",
            "opts": ["Within 15 minutes", "Within 2 weeks", "After 3 months"],
            "ans": 1,
            "exp": "Most vaccine side effects occur within 2 weeks. Serious delayed effects are extremely rare."
        },
        "nutrition": {
            "q": "How many servings of fruits and vegetables should you eat daily?",
            "opts": ["1-2 servings", "3-4 servings", "5 or more servings"],
            "ans": 2,
            "exp": "Health experts recommend 5 or more servings of fruits and vegetables daily."
        },
        "sleep": {
            "q": "How many hours of sleep do adults need per night?",
            "opts": ["5-6 hours", "7-9 hours", "10-12 hours"],
            "ans": 1,
            "exp": "Adults need 7-9 hours of sleep daily for optimal health and function."
        },
        "mental_health": {
            "q": "What percentage of adults experience mental illness yearly?",
            "opts": ["About 1 in 20", "About 1 in 10", "About 1 in 5"],
            "ans": 2,
            "exp": "About 1 in 5 (20%) of adults experience mental illness yearly. Help is available."
        }
    }
    
    topic_lower = topic.lower().strip()
    if topic_lower in quizzes:
        return {"status": "success", "quiz": quizzes[topic_lower]}
    
    available = ", ".join(quizzes.keys())
    return {"status": "error", "msg": f"Quiz for: {available}"}

def bust_myth(myth: str) -> dict:
    """Myth Buster Agent - Counter Misinformation"""
    myths = {
        "cold": {
            "myth": "Exposure to cold weather causes colds",
            "truth": "Viruses cause colds, not cold weather",
            "evidence": "People spend more time indoors in winter, increasing virus transmission"
        },
        "sugar": {
            "myth": "Sugar makes children hyperactive",
            "truth": "Scientific studies show no direct link",
            "evidence": "Blind studies found no behavioral changes from sugar vs placebo"
        },
        "vitamin": {
            "myth": "Taking vitamin C prevents colds",
            "truth": "Extra vitamin C doesn't prevent colds",
            "evidence": "Large clinical trials show no significant prevention benefit"
        },
        "water": {
            "myth": "You must drink exactly 8 glasses of water daily",
            "truth": "Water needs vary by person, activity, and climate",
            "evidence": "Listen to your body's thirst; guideline is ~3.7L for men, 2.7L for women"
        },
        "knuckles": {
            "myth": "Cracking knuckles causes arthritis",
            "truth": "Cracking knuckles does NOT cause arthritis",
            "evidence": "33-year study found no link between knuckle-cracking and arthritis"
        }
    }
    
    myth_lower = myth.lower()
    for key, value in myths.items():
        if key in myth_lower:
            return {"status": "success", "bust": value}
    
    return {"status": "error", "msg": "Myth not found. Try: cold, sugar, vitamin, water, knuckles"}

# ============================================
# STREAMLIT UI - FIXED
# ============================================

st.set_page_config(page_title="🩺 Health Bot", layout="wide")

st.title("🩺 Health Education Bot")
st.markdown("**Evidence-based health info, quizzes, and myth-busting**")

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if "history" not in st.session_state:
    st.session_state.history = []

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False

if "quiz_correct" not in st.session_state:
    st.session_state.quiz_correct = False

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

# ============================================
# SIDEBAR NAVIGATION
# ============================================

with st.sidebar:
    st.title("📋 Menu")
    mode = st.radio("Select Mode:", ["📚 Learn", "🎯 Quiz", "🔍 Myths", "📊 Dashboard"])

# ============================================
# MODE 1: LEARN
# ============================================

if mode == "📚 Learn":
    st.subheader("📚 Learn About Health Topics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input(
            "Enter a health topic:",
            placeholder="diabetes, vaccines, nutrition, sleep, mental_health",
            key="learn_topic"
        )
    
    with col2:
        st.markdown("")
        st.markdown("")
        search_btn = st.button("🔍 Get Information", key="learn_btn")
    
    if search_btn and topic:
        result = get_health_information(topic)
        
        if result["status"] == "success":
            st.success(f"✅ {result['title']}")
            st.write(f"**Overview:** {result['info']}")
            
            # Display all content nicely
            for key, val in result.items():
                if key not in ["status", "title", "info"]:
                    if isinstance(val, list):
                        st.write(f"**{key.replace('_', ' ').upper()}:**")
                        for item in val:
                            st.write(f"  • {item}")
                    else:
                        st.write(f"**{key.upper().replace('_', ' ')}:** {val}")
            
            st.session_state.history.append({
                "type": "learn",
                "topic": topic,
                "time": datetime.now().strftime("%H:%M")
            })
        else:
            st.error(f"❌ {result['msg']}")
    
    elif search_btn:
        st.warning("Please enter a health topic!")

# ============================================
# MODE 2: QUIZ (COMPLETELY FIXED)
# ============================================

elif mode == "🎯 Quiz":
    st.subheader("🎯 Test Your Knowledge")
    
    # Topic selection
    topic = st.selectbox(
        "Select a topic:",
        ["diabetes", "vaccines", "nutrition", "sleep", "mental_health"],
        key="quiz_topic"
    )
    
    # Load quiz button
    if st.button("📝 Load Quiz Question", key="load_quiz_btn"):
        result = generate_quiz(topic)
        
        if result["status"] == "success":
            st.session_state.current_quiz = result["quiz"]
            st.session_state.quiz_answered = False
            st.session_state.quiz_correct = False
            st.rerun()
    
    # Display quiz if loaded
    if st.session_state.current_quiz:
        quiz = st.session_state.current_quiz
        
        st.write(f"**Question:** {quiz['q']}")
        st.write("---")
        
        # Radio button for answer selection
        selected_idx = st.radio(
            "Select your answer:",
            range(len(quiz['opts'])),
            format_func=lambda i: quiz['opts'][i],
            key=f"quiz_answer_{topic}_{id(quiz)}"
        )
        
        # Submit button
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Submit Answer", key="submit_quiz_btn"):
                st.session_state.quiz_answered = True
                st.session_state.quiz_correct = (selected_idx == quiz['ans'])
                
                # Update score
                if topic not in st.session_state.scores:
                    st.session_state.scores[topic] = {"correct": 0, "total": 0}
                
                st.session_state.scores[topic]["total"] += 1
                if st.session_state.quiz_correct:
                    st.session_state.scores[topic]["correct"] += 1
                
                # Log to history
                st.session_state.history.append({
                    "type": "quiz",
                    "topic": topic,
                    "correct": st.session_state.quiz_correct,
                    "time": datetime.now().strftime("%H:%M")
                })
                
                st.rerun()
        
        with col2:
            if st.button("🔄 Next Question", key="next_quiz_btn"):
                st.session_state.current_quiz = None
                st.session_state.quiz_answered = False
                st.rerun()
        
        # Show result if answered
        if st.session_state.quiz_answered:
            st.write("---")
            if st.session_state.quiz_correct:
                st.success(f"🎉 **Correct!**")
            else:
                st.error(f"❌ **Incorrect!** The correct answer is: **{quiz['opts'][quiz['ans']]}**")
            
            st.info(f"**Explanation:** {quiz['exp']}")

# ============================================
# MODE 3: MYTHS
# ============================================

elif mode == "🔍 Myths":
    st.subheader("🔍 Bust Health Myths")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        myth = st.text_input(
            "Enter a health myth:",
            placeholder="Does sugar make kids hyperactive?",
            key="myth_input"
        )
    
    with col2:
        st.markdown("")
        st.markdown("")
        myth_btn = st.button("🔍 Investigate", key="myth_btn")
    
    if myth_btn and myth:
        result = bust_myth(myth)
        
        if result["status"] == "success":
            b = result["bust"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.error(f"**❌ THE MYTH:**\n{b['myth']}")
            
            with col2:
                st.success(f"**✅ THE TRUTH:**\n{b['truth']}")
            
            st.info(f"**Evidence:** {b['evidence']}")
            
            st.session_state.history.append({
                "type": "myth",
                "myth": myth,
                "time": datetime.now().strftime("%H:%M")
            })
        else:
            st.error(f"❌ {result['msg']}")
    
    elif myth_btn:
        st.warning("Please enter a health myth!")

# ============================================
# MODE 4: DASHBOARD
# ============================================

elif mode == "📊 Dashboard":
    st.subheader("📊 Your Learning Progress")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_activities = len(st.session_state.history)
    learn_count = len([h for h in st.session_state.history if h["type"] == "learn"])
    quiz_count = len([h for h in st.session_state.history if h["type"] == "quiz"])
    myth_count = len([h for h in st.session_state.history if h["type"] == "myth"])
    
    col1.metric("Total Activities", total_activities)
    col2.metric("Topics Learned", learn_count)
    col3.metric("Quizzes Taken", quiz_count)
    col4.metric("Myths Busted", myth_count)
    
    st.write("---")
    
    # Quiz Scores
    if st.session_state.scores:
        st.subheader("🎯 Quiz Performance")
        
        score_data = []
        for topic, scores in st.session_state.scores.items():
            if scores["total"] > 0:
                pct = (scores["correct"] / scores["total"] * 100)
                score_data.append({
                    "Topic": topic.title(),
                    "Correct": scores["correct"],
                    "Total": scores["total"],
                    "Score": f"{pct:.0f}%"
                })
        
        if score_data:
            st.dataframe(score_data, use_container_width=True, hide_index=True)
    
    st.write("---")
    
    # Recent Activities
    if st.session_state.history:
        st.subheader("📝 Recent Activities")
        
        for i, entry in enumerate(reversed(st.session_state.history[-10:]), 1):
            if entry["type"] == "learn":
                st.write(f"{i}. 📚 Learned about **{entry['topic'].title()}** ({entry['time']})")
            elif entry["type"] == "quiz":
                icon = "✅" if entry["correct"] else "❌"
                st.write(f"{i}. {icon} Quizzed on **{entry['topic'].title()}** ({entry['time']})")
            elif entry["type"] == "myth":
                st.write(f"{i}. 🔍 Investigated myth about **{entry['myth'][:40]}...** ({entry['time']})")

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.85em;'>
🩺 Health Education Bot | Evidence-Based Health Information<br>
⚠️ This is educational content only. Consult a healthcare provider for medical advice.<br>
📊 Session data is stored locally.
</div>
""", unsafe_allow_html=True)
