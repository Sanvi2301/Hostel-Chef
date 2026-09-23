import streamlit as st
from groq import Groq
from datetime import datetime
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="HostelChef AI",
    page_icon="🍳",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.stButton>button {
    width:100%;
    background:#FF6B35;
    color:white;
    border:none;
    border-radius:12px;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover {
    background:#ff8a5c;
}

.block-container {
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# GROQ API
# =====================================================

GROQ_API_KEY = st.secrets["GROQ_API_KEYS"]

client = Groq(
    api_key=GROQ_API_KEY
)

# =====================================================
# SYSTEM PROMPT
# =====================================================

SYSTEM_PROMPT = """
You are HostelChef Pro AI.

Your purpose is to help hostel students and working professionals make healthy, affordable and delicious food using ingredients already available.

Rules:

1. Suggest exactly 3 recipes.

2. Recipes must:
- Use user ingredients first
- Be hostel friendly
- Be beginner friendly
- Require minimal utensils
- Be healthy and nutritious

For EACH recipe provide:

Recipe Name

Preparation Time

Cooking Time

Difficulty Level

Ingredients Used

Step By Step Instructions

Health Benefits

Nutrition Estimate:
- Calories
- Protein
- Carbs
- Fat

---------------------

After recipes provide:

SECTION 1: Weekly Meal Plan

Monday
Tuesday
Wednesday
Thursday
Friday
Saturday
Sunday

SECTION 2: Shopping Suggestions

Provide 10 inexpensive ingredients that can unlock more meals.

Include approximate cost.

SECTION 3: Leftover Ingredient Ideas

Suggest meals from leftovers.

SECTION 4: High Protein Options

SECTION 5: Weight Loss Options

SECTION 6: Budget Meals Under ₹50

Keep output clean markdown.
"""

# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# FUNCTION
# =====================================================

def generate_recipe(user_prompt):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
  