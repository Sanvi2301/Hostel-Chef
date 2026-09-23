import streamlit as st
from google import genai
from datetime import datetime
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="🍳 HostelChef AI",
    page_icon="🍳",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.stButton>button{
    width:100%;
    background:#FF6B35;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#ff814f;
}

.recipe-card{
    background:#1E293B;
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
}

.metric-box{
    background:#16213E;
    padding:15px;
    border-radius:12px;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# API SETUP
# ==================================================

API_KEY = "YOUR_GEMINI_API_KEY"

client = genai.Client(api_key=API_KEY)

# ==================================================
# SYSTEM PROMPT
# ==================================================

SYSTEM_PROMPT = """
You are HostelChef AI.

Your job is to help hostel students and busy professionals cook healthy and affordable meals using ingredients already available.

Rules:

1. Suggest exactly 3 recipes.

2. Prioritize user's ingredients.

3. Recipes must be:
   - Healthy
   - Hostel friendly
   - Budget friendly
   - Easy to cook

4. Mention:

Recipe Name

Preparation Time

Cooking Time

Difficulty Level

Ingredients Used

Step By Step Instructions

Health Benefits

Approx Nutrition:
- Calories
- Protein
- Carbs
- Fat

5. Suggest optional improvements.

6. If ingredients are limited,
   creatively combine them.

7. Never suggest unsafe cooking techniques.

8. Focus on:
   High protein
   Low effort
   Good taste

9. Return output in markdown.

10. Add a final section:

"Shopping Suggestions"
Give 5 inexpensive ingredients that can unlock more recipes.

11. Add section:
"Leftover Ingredient Ideas"

12. Add section:
"Weekly Meal Plan"

Monday
Tuesday
Wednesday
Thursday
Friday
Saturday
Sunday

"""

# ==================================================
# SESSION STATE
# ==================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==================================================
# HEADER
# ==================================================

st.title("🍳 HostelChef AI")

st.caption(
    "Generate healthy hostel-friendly meals from ingredients you already have"
)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("⚙️ Settings")

    diet = st.selectbox(
        "Diet Preference",
        [
            "No Preference",
            "Vegetarian",
            "Eggetarian",
            "Vegan",
            "High Protein"
        ]
    )

    appliance = st.selectbox(
        "Cooking Appliance",
        [
            "Any",
            "Microwave",
            "Kettle",
            "Induction",
            "Rice Cooker"
        ]
    )

    cooking_time = st.slider(
        "Maximum Cooking Time (Minutes)",
        5,
        60,
        20
    )

    st.divider()

    st.header("📌 Quick Examples")

    example1 = "Rice, Onion, Egg"
    example2 = "Bread, Peanut Butter, Banana"
    example3 = "Maggi, Capsicum, Tomato"

    if st.button(example1):
        st.session_state.ingredients = example1

    if st.button(example2):
        st.session_state.ingredients = example2

    if st.button(example3):
        st.session_state.ingredients = example3

    st.divider()

    st.header("💡 Hostel Tips")

    st.info("""
✅ Keep eggs for quick protein

✅ Use oats for breakfast

✅ Buy seasonal vegetables

✅ Store roasted peanuts

✅ Cook once, eat twice
""")

# ==================================================
# INGREDIENT INPUT
# ==================================================

ingredients = st.text_area(
    "Enter Available Ingredients",
    value=st.session_state.get("ingredients", ""),
    height=120,
    placeholder="Rice, Onion, Tomato, Egg"
)

# ==================================================
# METRICS
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Healthy", "✅")

with col2:
    st.metric("Budget Friendly", "✅")

with col3:
    st.metric("Hostel Friendly", "✅")

# ==================================================
# BUTTON
# ==================================================

generate = st.button("🚀 Generate Recipes")

# ==================================================
# GENERATE RECIPES
# ==================================================

if generate:

    if not ingredients.strip():

        st.warning("Please enter some ingredients.")

    else:

        with st.spinner("Cooking some AI magic... 🍲"):

            user_prompt = f"""
            Ingredients:
            {ingredients}

            Diet:
            {diet}

            Appliance:
            {appliance}

            Maximum Cooking Time:
            {cooking_time} minutes

            Generate:
            - 3 recipes
            - Weekly meal plan
            - Shopping suggestions
            - Nutrition estimates
            - Leftover ideas
            """

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=SYSTEM_PROMPT + "\n\n" + user_prompt
                )

                result = response.text

                st.success("Recipes Generated Successfully!")

                st.markdown(result)

                st.download_button(
                    "📥 Download Recipes",
                    result,
                    file_name="hostel_recipes.txt",
                    mime="text/plain"
                )

                st.session_state.history.append({
                    "date": datetime.now(),
                    "ingredients": ingredients
                })

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ==================================================
# HISTORY
# ==================================================

if st.session_state.history:

    st.divider()

    st.subheader("🕘 Recipe History")

    history_df = pd.DataFrame(st.session_state.history)

    st.dataframe(
        history_df,
        use_container_width=True
    )

# ==================================================
# FAQ SECTION
# ==================================================

st.divider()

st.subheader("❓ Frequently Asked Questions")

with st.expander("How does HostelChef AI work?"):
    st.write("""
You enter ingredients available with you and
the AI suggests healthy recipes based on them.
""")

with st.expander("Are recipes healthy?"):
    st.write("""
Yes. Recipes prioritize balanced nutrition,
protein, fiber and reduced oil usage.
""")

with st.expander("Can I use only a kettle?"):
    st.write("""
Yes. Select Kettle from the appliance list
and recipes will be tailored accordingly.
""")

with st.expander("Can I lose weight using these recipes?"):
    st.write("""
The app focuses on healthier food choices,
but medical or dietary advice should be
obtained from qualified professionals.
""")

with st.expander("How are nutrition values generated?"):
    st.write("""
Nutrition values are AI-generated estimates
and may vary from actual values.
""")

# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown(
"""
<center>
<h4>🍳 HostelChef AI</h4>
Healthy • Budget Friendly • Student Friendly
</center>
""",
unsafe_allow_html=True
)