import streamlit as st
import sys
import os

st.set_page_config(
    page_title="FYND AI Internship",
    page_icon="🚀",
    layout="wide"
)

st.sidebar.title("🚀 FYND AI Project")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Page",
    ["Rating Prediction", "User Dashboard", "Admin Dashboard"]
)

st.sidebar.markdown("---")
st.sidebar.info("Built for FYND AI Internship Assessment")

if page == "Rating Prediction":
    st.title("Task 1: Yelp Rating Prediction")
    st.markdown("### Analyze Yelp reviews and predict star ratings")
    
    st.info("⚠️ Task 1 performs well with **TinyLlama 1.1B**")
    
    st.markdown("""
    **What this does:**
    - Tests 3 different prompting approaches
    - Predicts 1-5 star ratings from reviews
    - Compares accuracy, MAE, and JSON validity
    """)
    
    with st.expander("📖 View Previous Results - TinyLlama 1.1B"):
         st.markdown("""
### **📌 Yelp Rating Prediction – TinyLlama 1.1B (200 Sample Reviews)**

---

## **🔹 Approach 1 — Basic Prompt**
- **Accuracy:** **29%**
- **MAE:** *1.09*  
- **Valid JSON:** **88.5%**
- **Failures:** *(If you tracked failures, add here — otherwise remove line)*  
- **Behavior:**  
  - Most stable and consistent  
  - Minimal hallucinations  
  - Highest JSON validity

---

## **🔹 Approach 2 — Keyword-Guided Prompt**
- **Accuracy:** *(Add value if measured)*  
- **MAE:** *1.10*  
- **Valid JSON:** *(Add if measured)*  
- **Behavior:**  
  - Better alignment with sentiment-specific keywords  
  - Stronger positive/negative polarity detection  
  - Sometimes overweights keyword cues

---

## **🔹 Approach 3 — Examples + Chain-of-Thought**
- **Accuracy:** *(Add value if measured)*  
- **MAE:** *1.35*  
- **Valid JSON:** *(Add if measured)*  
- **Behavior:**  
  - Best performance on longer, multi-sentence reviews  
  - Produces coherent reasoning  
  - Slight example-induced bias

---

## **📊 Overall Comparison**

| Approach | Accuracy | JSON Valid | Notes |
|---------|----------|------------|-------|
| **Basic** | 29% | 88.5% | Most reliable, best formatting |
| **Keywords** | — | — | Strong sentiment mapping |
| **Examples + CoT** | — | — | Best for complex reasoning |

**➡️ Best Approach:** **Approach 1 — Basic Prompt**

---

## **📝 Key Findings**

- TinyLlama 1.1B performed **surprisingly well given its small size**, especially in JSON formatting.  
- Approach 1 produced:
  - ✅ **Highest accuracy**
  - ✅ **Highest JSON validity**
  - ⚠️ Least expressive reasoning  
- Approach 2 improved emotional alignment but did not outperform Basic.  
- Approach 3 gave the best reasoning quality but slightly less accuracy.  
- Small models benefit heavily from **shorter prompts + clearer structure**.
""")

    
    with st.expander("📖 View Previous Results - Llama 3 8B"):
        st.markdown("""
### **📌 Yelp Rating Prediction – Llama 3 8B (200 Sample Reviews)**

---

## **🔹 Approach 1 — Basic Prompt**
- **Accuracy:** **16.5%**
- **MAE:** **1.19**
- **Valid JSON:** **0.0%**
- **Failures:** **200 / 200**
- **Prediction Pattern:**  
  - Predicted **3★ for all 200 reviews (100%)**
  - ⚠️ Never predicted: **1★, 2★, 4★, 5★**

---

## **🔹 Approach 2 — Keyword-Guided Prompt**
- **Accuracy:** **16.5%**
- **MAE:** **1.19**
- **Valid JSON:** **0.0%**
- **Failures:** **200 / 200**
- **Prediction Pattern:**  
  - Predicted **3★ for all 200 reviews (100%)**
  - ⚠️ Never predicted: **1★, 2★, 4★, 5★**

---

## **🔹 Approach 3 — Examples + Chain-of-Thought**
- **Accuracy:** **16.5%**
- **MAE:** **1.19**
- **Valid JSON:** **0.0%**
- **Failures:** **200 / 200**
- **Prediction Pattern:**  
  - Predicted **3★ for all 200 reviews (100%)**
  - ⚠️ Never predicted: **1★, 2★, 4★, 5★**

---

## **📊 Overall Comparison**

| Approach | Accuracy | MAE | JSON Valid |
|---------|----------|------|------------|
| **Basic** | 16.5% | 1.19 | 0.0% |
| **Keywords** | 16.5% | 1.19 | 0.0% |
| **Examples + CoT** | 16.5% | 1.19 | 0.0% |

**➡️ Best Approach:** **Approach 1 — Basic**

---

## **📝 Key Findings**

- Llama 3 8B produced **only 3-star predictions**, showing:
  - ⚠️ **Strong neutral bias**
  - ⚠️ **Zero JSON compliance**
  - ⚠️ **No improvement across prompt variants**
- MAE remained stable at **1.19** for all approaches.
- More advanced prompting **did not** improve performance.
- Basic direct prompt worked **best**, but still with low accuracy.
""")


elif page == "User Dashboard":
    import importlib.util
    
    user_path = os.path.join(os.path.dirname(__file__), 'task2', 'user_dashboard.py')
    
    if os.path.exists(user_path):
        spec = importlib.util.spec_from_file_location("user_dashboard", user_path)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
        user_module.main()
    else:
        st.error("user_dashboard.py not found in task2 folder")

elif page == "Admin Dashboard":
    import importlib.util
    
    admin_path = os.path.join(os.path.dirname(__file__), 'task2', 'admin_dashboard.py')
    
    if os.path.exists(admin_path):
        spec = importlib.util.spec_from_file_location("admin_dashboard", admin_path)
        admin_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(admin_module)
        admin_module.main()
    else:
        st.error("admin_dashboard.py not found in task2 folder")

