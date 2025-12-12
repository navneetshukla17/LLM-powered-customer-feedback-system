import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests

DATA_FILE = "feedback_data.csv"
HF_API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2-7B-Instruct"
HF_TOKEN = st.secrets.get("HF_TOKEN", "") 

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except:
            return pd.DataFrame(columns=['id', 'timestamp', 'rating', 'review', 'ai_response'])
    return pd.DataFrame(columns=['id', 'timestamp', 'rating', 'review', 'ai_response'])

def save_feedback(rating, review, ai_response):
    df = load_data()
    new_entry = {
        'id': int(datetime.now().timestamp() * 1000),
        'timestamp': datetime.now().isoformat(),
        'rating': rating,
        'review': review,
        'ai_response': ai_response,
        'summary': '',
        'actions': ''
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return True

def generate_ai_response(rating, review):
    try:
        if rating >= 4:
            context = "You are responding to positive feedback. Be warm and grateful (2-3 sentences)."
        elif rating == 3:
            context = "You are responding to neutral feedback. Be understanding (2-3 sentences)."
        else:
            context = "You are responding to negative feedback. Be apologetic and solution-focused (2-3 sentences)."
        
        prompt = f"{context}\n\nCustomer gave {rating}/5 stars: \"{review}\"\n\nYour response:"
        
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                ai_text = result[0].get("generated_text", "").strip()
                if len(ai_text) > 20:
                    return ai_text
        
        raise Exception("API response invalid")
    
    except Exception as e:
        print(f"AI Error: {e}")
        if rating >= 4:
            return "Thank you so much for your wonderful feedback! We're thrilled to hear you had a great experience with us. We look forward to serving you again!"
        elif rating == 3:
            return "Thank you for your feedback. We appreciate you taking the time to share your experience. We're always working to improve!"
        else:
            return "We sincerely apologize for not meeting your expectations. Your feedback is invaluable to us, and we're committed to making things right."

st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .feedback-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .star-rating {
        font-size: 3rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border-radius: 10px;
        width: 100%;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    h1 {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: white;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("<h1>⭐ Share Your Experience with us</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>We value your feedback and strive to improve</p>", unsafe_allow_html=True)
    
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'ai_response' not in st.session_state:
        st.session_state.ai_response = ""
    
    with st.container():
        st.markdown("<div class='feedback-card'>", unsafe_allow_html=True)
        
        st.markdown("### 🌟 Rate Your Experience")
        rating = st.select_slider(
            "Select rating",
            options=[1, 2, 3, 4, 5],
            value=5,
            format_func=lambda x: "⭐" * x,
            label_visibility="collapsed"
        )
        
        st.markdown(f"<div class='star-rating'>{'⭐' * rating}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #666; margin-top: -1rem;'>You selected {rating} star{'s' if rating != 1 else ''}</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📝 Tell Us More")
        review = st.text_area(
            "Share your experience with us...",
            height=150,
            placeholder="Tell us about your experience...",
            label_visibility="collapsed"
        )
        
        st.caption(f"{len(review)} characters")
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.button("🚀 Submit Feedback", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    if submit_button:
        if len(review.strip()) < 10:
            st.error("⚠️ Please write at least 10 characters in your review")
        else:
            with st.spinner("✨ Generating AI response..."):
                ai_response = generate_ai_response(rating, review)
                save_feedback(rating, review, ai_response)
                st.session_state.submitted = True
                st.session_state.ai_response = ai_response
    
    if st.session_state.submitted:
        st.markdown("<div class='success-box'>", unsafe_allow_html=True)
        st.markdown("### ✅ Thank you for your feedback!")
        st.markdown(f"**Our Response:**")
        st.markdown(f"*{st.session_state.ai_response}*")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("📝 Submit Another Review"):
            st.session_state.submitted = False
            st.session_state.ai_response = ""
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: white; padding: 1rem;'>
        <p>Your feedback helps us serve you better</p>
        <p style='font-size: 0.9rem; opacity: 0.8;'>Powered by Qwen AI • Secure & Confidential</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
