import streamlit as st
import sys
import os

st.set_page_config(
    page_title="FYND AI Internship Assessment",
    page_icon="🚀",
    layout="wide"
)

st.sidebar.title("FYND AI Assessment")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Task 1: Rating Prediction", "Task 2: User Dashboard", "Task 2: Admin Dashboard"]
)

st.sidebar.markdown("---")
st.sidebar.info("Navneet Shukla | FYND AI Internship")

if page == "Task 1: Rating Prediction":
    st.title("Task 1: Yelp Rating Prediction via Prompting")
    
    st.markdown("""
    ### Objective
    Design and evaluate multiple prompting approaches to classify Yelp reviews into 1-5 star ratings, 
    returning structured JSON responses with explanations.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Dataset Information")
        st.markdown("""
        - **Source:** Yelp Reviews (Kaggle)
        - **Sample Size:** 200 reviews
        - **Evaluation Metrics:** Accuracy, MAE, JSON Validity Rate
        """)
    
    with col2:
        st.markdown("### Model Details")
        st.markdown("""
        - **Model:** TinyLlama 1.1B
        - **Deployment:** Local inference
        - **Device:** MPS (Apple Silicon)
        """)
    
    st.markdown("---")
    
    st.markdown("## Prompting Approaches")
    
    with st.expander("Approach 1: Basic Direct Prompt", expanded=True):
        st.markdown("""
        #### Simple, minimal prompt asking directly for star rating. Tests baseline model capability without additional guidance or context.
        """)
        
        st.code("""
Analyze this Yelp review and predict the star rating (1-5).
Return your response in JSON format:
{
  "predicted_stars": <number>,
  "explanation": "<brief reasoning>"
}

Review: [REVIEW_TEXT]
        """, language="text")
        
        st.markdown("### Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Accuracy", "31.0%")
        col2.metric("MAE", "1.09")
        col3.metric("JSON Validity", "91.0%")
        
        st.markdown("### Prediction Distribution")
        st.markdown("""
        - 3★: 20 (10.0%)
        - 4★: 114 (57.0%)
        - 5★: 66 (33.0%)
        - Never predicted: 1★, 2★
        """)
        
        st.markdown("### Key Observations")
        st.markdown("""
        - Highest accuracy among all approaches
        - Strong positive bias (71% predicted 4-5 stars)
        - Excellent JSON formatting compliance
        - Fails to capture negative sentiment (never predicted 1-2 stars)
        """)
    
    with st.expander("Approach 2: Keyword-Guided Prompt"):
        st.markdown("""
        #### Enhanced prompt with explicit sentiment keywords mapped to rating levels. Provides clearer signals for classification by associating specific words with star ratings.
        """)
        
        st.code("""
Analyze this Yelp review and predict the star rating (1-5).

Rating Guide:
- 1 star: terrible, awful, horrible, worst
- 2 stars: bad, poor, disappointing, mediocre
- 3 stars: okay, decent, average, fine
- 4 stars: good, nice, pleasant, solid
- 5 stars: excellent, amazing, outstanding, perfect

Return JSON:
{
  "predicted_stars": <number>,
  "explanation": "<brief reasoning>"
}

Review: [REVIEW_TEXT]
        """, language="text")
        
        st.markdown("### Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Accuracy", "28.0%")
        col2.metric("MAE", "1.10")
        col3.metric("JSON Validity", "44.5%")
        
        st.markdown("### Prediction Distribution")
        st.markdown("""
        - 1★: 1 (0.5%)
        - 3★: 111 (55.5%)
        - 4★: 54 (27.0%)
        - 5★: 34 (17.0%)
        - Never predicted: 2★
        """)
        
        st.markdown("### Key Observations")
        st.markdown("""
        - Slight decrease in accuracy compared to basic approach
        - Strong neutral bias (55.5% predicted 3 stars)
        - Significant drop in JSON validity (44.5%)
        - Additional context may have confused the small model
        """)
    
    with st.expander("Approach 3: Examples + Chain-of-Thought"):
        st.markdown("""
        #### Few-shot learning with example reviews and explicit reasoning steps. Guides model through analysis process to improve complex sentiment understanding.
        """)
        
        st.code("""
Analyze Yelp reviews and predict star ratings (1-5).

Examples:
Review: "Food was cold and service terrible"
Reasoning: Negative words indicate poor experience
Rating: 1 star

Review: "Great food, friendly staff, will return"
Reasoning: Positive sentiment throughout
Rating: 5 stars

Now analyze this review step by step:
1. Identify key sentiment words
2. Assess overall tone
3. Assign rating

Return JSON:
{
  "predicted_stars": <number>,
  "explanation": "<brief reasoning>"
}

Review: [REVIEW_TEXT]
        """, language="text")
        
        st.markdown("### Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Accuracy", "25.5%")
        col2.metric("MAE", "1.35")
        col3.metric("JSON Validity", "97.0%")
        
        st.markdown("### Prediction Distribution")
        st.markdown("""
        - 3★: 7 (3.5%)
        - 4★: 2 (1.0%)
        - 5★: 191 (95.5%)
        - Never predicted: 1★, 2★
        """)
        
        st.markdown("### Key Observations")
        st.markdown("""
        - Lowest accuracy but highest JSON validity
        - Extreme positive bias (95.5% predicted 5 stars)
        - Few-shot examples may have anchored model to positive sentiment
        - Best format compliance but worst predictive performance
        """)
    
    st.markdown("---")
    
    st.markdown("## Comparative Analysis")
    
    comparison_data = {
        "Approach": ["Basic Direct", "Keyword-Guided", "Examples + CoT"],
        "Accuracy": ["31.0%", "28.0%", "25.5%"],
        "MAE": ["1.09", "1.10", "1.35"],
        "JSON Validity": ["91.0%", "44.5%", "97.0%"],
        "Primary Bias": ["Positive (4★)", "Neutral (3★)", "Extreme Positive (5★)"]
    }
    
    st.table(comparison_data)
    
    st.markdown("---")
    
    st.markdown("## Key Findings & Discussion")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Best Performing Approach")
        st.success("**Approach 1: Basic Direct Prompt**")
        st.markdown("""
        **Reasons for Success:**
        - Simplicity works best for small models (1.1B parameters)
        - Clear, direct instructions without confusion
        - Optimal balance between accuracy and JSON compliance
        - Less prompt complexity = more consistent outputs
        """)
    
    with col2:
        st.markdown("### Common Challenges")
        st.markdown("""
        **All approaches struggled with:**
        - Negative sentiment detection (rarely predicted 1-2 stars)
        - Model size limitations affecting reasoning depth
        - Inherent positive bias in predictions
        - Difficulty maintaining JSON structure with complex prompts
        """)
    
    st.markdown("### Why More Complex Prompts Underperformed")
    st.markdown("""
    1. **Keyword-Guided Approach:** Additional keywords introduced noise for the small model, 
       causing it to default to middle ratings (3 stars) when uncertain.
    
    2. **Chain-of-Thought Approach:** Few-shot examples anchored the model toward extreme 
       predictions, particularly 5-star ratings, reducing prediction diversity.
    
    3. **Model Capacity:** TinyLlama 1.1B has limited reasoning capacity. More complex 
       instructions exceeded its ability to follow multi-step logic consistently.
    """)
    
    st.markdown("---")
    
    st.markdown("## Recommendations")
    
    st.markdown("""
    ### For Improved Performance:
    
    1. **Model Selection:**
       - Use larger models (7B+ parameters) for better reasoning
       - Consider fine-tuned sentiment analysis models
       - Test instruction-tuned variants for better prompt following
    
    2. **Prompt Engineering:**
       - Keep prompts simple for small models
       - Use balanced examples (both positive and negative)
       - Include explicit instructions for edge cases
       - Add format validation in prompt
    
    3. **Post-Processing:**
       - Implement ensemble voting across approaches
       - Add calibration layer for bias correction
       - Use confidence thresholds for uncertain predictions
    
    4. **Data Strategy:**
       - Ensure balanced representation of all rating levels
       - Include challenging edge cases in evaluation
       - Use stratified sampling for fair assessment
    """)
    
    st.markdown("---")
    
    with st.expander("View Complete Test Results"):
        st.code("""
YELP RATING PREDICTION - LOCAL MODEL (TinyLlama 1.1B)
Sample Size: 200 reviews
Device: MPS (Apple Silicon)

============================================================
APPROACH 1: BASIC DIRECT PROMPT
============================================================
Accuracy: 31.0%
MAE: 1.09
Valid JSON: 91.0%
Failed: 18

Predictions:
  3★: 20 (10.0%)
  4★: 114 (57.0%)
  5★: 66 (33.0%)

Actual Distribution:
  1★: 18 (9.0%)
  2★: 17 (8.5%)
  3★: 33 (16.5%)
  4★: 79 (39.5%)
  5★: 53 (26.5%)

============================================================
APPROACH 2: KEYWORD-GUIDED PROMPT
============================================================
Accuracy: 28.0%
MAE: 1.10
Valid JSON: 44.5%
Failed: 111

Predictions:
  1★: 1 (0.5%)
  3★: 111 (55.5%)
  4★: 54 (27.0%)
  5★: 34 (17.0%)

Actual Distribution:
  1★: 18 (9.0%)
  2★: 17 (8.5%)
  3★: 33 (16.5%)
  4★: 79 (39.5%)
  5★: 53 (26.5%)

============================================================
APPROACH 3: EXAMPLES + CHAIN-OF-THOUGHT
============================================================
Accuracy: 25.5%
MAE: 1.35
Valid JSON: 97.0%
Failed: 6

Predictions:
  3★: 7 (3.5%)
  4★: 2 (1.0%)
  5★: 191 (95.5%)

Actual Distribution:
  1★: 18 (9.0%)
  2★: 17 (8.5%)
  3★: 33 (16.5%)
  4★: 79 (39.5%)
  5★: 53 (26.5%)

============================================================
SUMMARY
============================================================
Best Overall: Approach 1 (Basic Direct Prompt)
  - Highest Accuracy: 31.0%
  - Lowest MAE: 1.09
  - Strong JSON Validity: 91.0%

Average Performance:
  - Accuracy: 28.2%
  - MAE: 1.18
  - JSON Validity: 77.5%
        """, language="text")

elif page == "Task 2: User Dashboard":
    import importlib.util
    
    user_path = os.path.join(os.path.dirname(__file__), 'task2', 'user_dashboard.py')
    
    if os.path.exists(user_path):
        spec = importlib.util.spec_from_file_location("user_dashboard", user_path)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
        user_module.main()
    else:
        st.error("user_dashboard.py not found in task2 folder")

elif page == "Task 2: Admin Dashboard":
    import importlib.util
    
    admin_path = os.path.join(os.path.dirname(__file__), 'task2', 'admin_dashboard.py')
    
    if os.path.exists(admin_path):
        spec = importlib.util.spec_from_file_location("admin_dashboard", admin_path)
        admin_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(admin_module)
        admin_module.main()
    else:
        st.error("admin_dashboard.py not found in task2 folder")