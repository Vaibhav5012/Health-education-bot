# Health Education Bot - Streamlit Cloud Edition
import streamlit as st
import uuid
from datetime import datetime

# ============================================
# AGENT TOOLS
# ============================================

def get_health_information(topic: str) -> dict:
    """Search Agent - Health Information"""
    health_db = {
        "diabetes": {
            "title": "Diabetes",
            "info": "Chronic condition affecting blood glucose regulation.",
            "types": ["Type 1: Autoimmune", "Type 2: Lifestyle-related", "Gestational: During pregnancy"],
            "mgmt": ["Regular exercise", "Healthy diet", "Weight management", "Regular monitoring"]
        },
        "vaccines": {
            "title": "Vaccines",
            "info": "Train immune system to fight diseases.",
            "benefits": ["Prevent serious disease", "Reduce transmission", "Save 2-3M lives/year"],
            "safety": "Rigorous testing; side effects mild and temporary"
        },
        "nutrition": {
            "title": "Nutrition",
            "info": "Good nutrition prevents chronic diseases.",
            "tips": ["5+ fruits/veggies daily", "Whole grains", "Lean proteins", "Healthy fats"],
            "tips2": ["Limit sugars", "Control portions", "Stay hydrated"]
        },
        "sleep": {
            "title": "Sleep",
            "info": "Essential for health, immunity, and cognition.",
            "recommended": "Adults: 7-9 hours daily",
            "tips": ["Consistent schedule", "Dark room", "Cool temperature", "Avoid screens before bed"],
            "benefits": ["Immune strength", "Memory consolidation", "Hormone regulation"]
        },
        "mental_health": {
            "title": "Mental Health",
            "info": "Psychological well-being is crucial.",
            "conditions": ["Depression", "Anxiety", "Stress", "Burnout"],
            "help": ["Therapy", "Exercise", "Meditation", "Social connections"]
        }
    }
    
    topic_lower = topic.lower().strip()
    if topic_lower in health_db:
        return {"status": "success", **health_db[topic_lower]}
    
    return {"status": "error", "msg": "Try: diabetes, vaccines, nutrition, sleep, mental_health"}

def generate_quiz(topic: str) -> dict:
    """Quiz Agent - Generate Questions"""
    quizzes = {
        "diabetes": {"q": "Normal fasting glucose?", "opts": ["<100", "100-125", ">125"], "ans": 0, "exp": "<100 is normal"},
        "vaccines": {"q": "When do side effects occur?", "opts": ["15 min", "2 weeks", "6 months"], "ans": 1, "exp": "Most within 2 weeks"},
        "nutrition": {"q": "Daily veggie servings?", "opts": ["1-2", "3-4", "5+"], "ans": 2, "exp": "5+ recommended"},
        "sleep": {"q": "Hours needed?", "opts": ["5-6", "7-9", "10-12"], "ans": 1, "exp": "7-9 hours optimal"}
    }
    
    if topic.lower() in quizzes:
        return {"status": "success", "quiz": quizzes[topic.lower()]}
    return {"status": "error", "msg": "No quiz"}

def bust_myth(myth: str) -> dict:
    """Myth Buster Agent - Counter Misinformation"""
    myths = {
        "cold": {"myth": "Cold weather causes colds", "truth": "Viruses cause colds", "evidence": "Virus transmission in close quarters"},
        "sugar": {"myth": "Sugar makes kids hyperactive", "truth": "No scientific link", "evidence": "Placebo effect and excitement"},
        "vitamin": {"myth": "Vitamin C prevents colds", "truth": "Doesn't prevent", "evidence": "Large trials show no benefit"},
        "water": {"myth": "Drink 8 glasses daily", "truth": "Needs vary by person", "evidence": "Listen to thirst"}
    }
    
    for key, value in myths.items():
        if key in myth.lower():
            return {"status": "success", "bust": value}
    
    return {"status": "error", "msg": "Myth not found"}

# ============================================
# STREAMLIT UI
# ============================================

st.set_page_config(page_title="🩺 Health Bot", layout="wide")

st.title("🩺 Health Education Bot")
st.markdown("**Evidence-based health info, quizzes, and myth-busting**")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []
if "scores" not in st.session_state:
    st.session_state.scores = {}

# Sidebar
mode = st.sidebar.radio("Select:", ["📚 Learn", "🎯 Quiz", "🔍 Myths", "📊 Dashboard"])

# ============================================
# MODE 1: LEARN
# ============================================

if mode == "📚 Learn":
    st.subheader("📚 Learn About Health")
    topic = st.text_input("Topic:", placeholder="diabetes, vaccines, nutrition, sleep, mental_health")
    
    if st.button("Get Info"):
        result = get_health_information(topic)
        if result["status"] == "success":
            st.success(f"✅ {result['title']}")
            st.write(f"**{result['info']}**")
            for key, val in result.items():
                if key not in ["status", "title", "info"] and isinstance(val, list):
                    st.write(f"• {key.replace('_', ' ').upper()}:")
                    for item in val:
                        st.write(f"  - {item}")
            st.session_state.history.append({"type": "learn", "topic": topic})
        else:
            st.error(result["msg"])

# ============================================
# MODE 2: QUIZ
# ============================================

elif mode == "🎯 Quiz":
    st.subheader("🎯 Test Your Knowledge")
    topic = st.selectbox("Topic:", ["diabetes", "vaccines", "nutrition", "sleep"])
    
    if st.button("Start Quiz"):
        result = generate_quiz(topic)
        if result["status"] == "success":
            q = result["quiz"]
            st.write(f"**Q: {q['q']}**")
            ans = st.radio("Your answer:", q["opts"])
            
            if st.button("Submit"):
                if q["opts"].index(ans) == q["ans"]:
                    st.success(f"✅ Correct! {q['exp']}")
                    if topic not in st.session_state.scores:
                        st.session_state.scores[topic] = {"correct": 0, "total": 0}
                    st.session_state.scores[topic]["correct"] += 1
                else:
                    st.error(f"❌ Wrong. Correct: {q['opts'][q['ans']]}")
                
                st.session_state.scores[topic]["total"] = st.session_state.scores[topic].get("total", 0) + 1
                st.session_state.history.append({"type": "quiz", "topic": topic})

# ============================================
# MODE 3: MYTHS
# ============================================

elif mode == "🔍 Myths":
    st.subheader("🔍 Bust Health Myths")
    myth = st.text_input("Enter myth:", placeholder="Does sugar make kids hyperactive?")
    
    if st.button("Investigate"):
        result = bust_myth(myth)
        if result["status"] == "success":
            b = result["bust"]
            col1, col2 = st.columns(2)
            with col1:
                st.error(f"❌ **MYTH:** {b['myth']}")
            with col2:
                st.success(f"✅ **TRUTH:** {b['truth']}")
            st.info(f"**Evidence:** {b['evidence']}")
            st.session_state.history.append({"type": "myth", "myth": myth})
        else:
            st.warning(result["msg"])

# ============================================
# MODE 4: DASHBOARD
# ============================================

elif mode == "📊 Dashboard":
    st.subheader("📊 Your Progress")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Activities", len(st.session_state.history))
    col2.metric("Quiz Taken", len([h for h in st.session_state.history if h["type"] == "quiz"]))
    col3.metric("Topics Learned", len([h for h in st.session_state.history if h["type"] == "learn"]))
    
    if st.session_state.scores:
        st.subheader("Quiz Scores")
        for topic, scores in st.session_state.scores.items():
            pct = (scores["correct"] / scores["total"] * 100) if scores["total"] > 0 else 0
            st.write(f"**{topic.title()}:** {scores['correct']}/{scores['total']} ({pct:.0f}%)")

st.markdown("---")
st.markdown("**Disclaimer:** For medical advice, consult a healthcare provider. This is educational only.")
