import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
import requests
import plotly.express as px
import plotly.graph_objects as go

DATA_FILE = "feedback_data.csv"
HF_API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2-7B-Instruct"
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            if 'summary' not in df.columns:
                df['summary'] = ''
            if 'actions' not in df.columns:
                df['actions'] = ''
            return df
        except:
            return pd.DataFrame(columns=['id', 'timestamp', 'rating', 'review', 'ai_response', 'summary', 'actions'])
    return pd.DataFrame(columns=['id', 'timestamp', 'rating', 'review', 'ai_response', 'summary', 'actions'])

def generate_admin_analysis(rating, review):    
    try:
        prompt = f"""Analyze this customer feedback professionally:

Rating: {rating}/5 stars
Review: "{review}"

Provide:
1. One sentence summary of the key issue/sentiment
2. Three specific actionable recommendations

Format your response as:
SUMMARY: [one sentence]
ACTION 1: [specific action]
ACTION 2: [specific action]
ACTION 3: [specific action]"""
        
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "").strip()
                
                summary = ""
                actions = []
                
                if "SUMMARY:" in text:
                    summary_part = text.split("SUMMARY:")[1].split("ACTION")[0].strip()
                    summary = summary_part.split("\n")[0].strip()
                
                for i in range(1, 4):
                    if f"ACTION {i}:" in text:
                        action_text = text.split(f"ACTION {i}:")[1]
                        if f"ACTION {i+1}:" in action_text:
                            action_text = action_text.split(f"ACTION {i+1}:")[0]
                        action = action_text.strip().split("\n")[0].strip()
                        if action and len(action) > 10:
                            actions.append(action)
                
                if summary and len(summary) > 20 and len(actions) >= 2:
                    return summary, actions
        
        raise Exception("AI parsing failed")
    
    except Exception as e:
        print(f"AI Error: {e}")
        pass
    
    review_lower = review.lower()
    
    if rating >= 4:
        summary = f"Customer is highly satisfied with the service and experience (rated {rating}/5)"
        actions = [
            "Send personalized thank you message to customer",
            "Request permission to use review as testimonial",
            "Analyze what went well to replicate success"
        ]
    elif rating == 3:
        summary = f"Customer had a mixed experience with room for improvement (rated {rating}/5)"
        actions = [
            "Contact customer to understand specific pain points",
            "Identify service gaps mentioned in the feedback",
            "Implement improvements in areas of concern"
        ]
    else:
        summary = f"Customer expressed dissatisfaction with the service experience (rated {rating}/5)"
        actions = [
            "Reach out immediately to apologize and resolve issue",
            "Conduct internal investigation into problems raised",
            "Offer compensation to recover customer relationship"
        ]
    
    return summary, actions

def update_analysis(df, idx):
    rating = df.loc[idx, 'rating']
    review = df.loc[idx, 'review']
    
    summary, actions = generate_admin_analysis(rating, review)
    
    df.loc[idx, 'summary'] = summary
    df.loc[idx, 'actions'] = json.dumps(actions)
    df.to_csv(DATA_FILE, index=False)
    
    return summary, actions

def get_rating_color(rating):
    return "🟢" if rating >= 4 else ("🟡" if rating == 3 else "🔴")

def get_border_class(rating):
    return "positive-border" if rating >= 4 else ("neutral-border" if rating == 3 else "negative-border")

st.markdown("""
<style>
    .main {
        background: #f8f9fa;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    .feedback-item {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 4px solid #e0e0e0;
    }
    
    .positive-border {
        border-left-color: #4caf50 !important;
    }
    
    .neutral-border {
        border-left-color: #ff9800 !important;
    }
    
    .negative-border {
        border-left-color: #f44336 !important;
    }
    
    .analysis-box {
        background: #f0f4ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #667eea;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def create_rating_distribution(df):
    if len(df) == 0:
        return None
    
    rating_counts = df['rating'].value_counts().sort_index()
    
    fig = go.Figure(data=[
        go.Bar(
            x=[f"{i} ⭐" for i in rating_counts.index],
            y=rating_counts.values,
            marker_color=['#f44336', '#ff9800', '#ffc107', '#8bc34a', '#4caf50'][:len(rating_counts)],
            text=rating_counts.values,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Rating Distribution",
        xaxis_title="Rating",
        yaxis_title="Count",
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_timeline_chart(df):
    if len(df) == 0:
        return None
    
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_counts = df.groupby('date').size().reset_index(name='count')
    
    fig = px.line(
        daily_counts,
        x='date',
        y='count',
        title='Feedback Submissions Over Time',
        markers=True
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Submissions",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def main():
    st.title("📊 Admin Dashboard")
    st.markdown("### Customer Feedback Management System")
    
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    df = load_data()
    
    if len(df) == 0:
        st.info("📭 No feedback submissions yet. Waiting for customer reviews...")
        st.markdown("### 🚀 Getting Started")
        st.markdown("""
        1. Users can submit feedback through the User Dashboard
        2. Feedback will appear here automatically
        3. Click 'Generate Analysis' to get AI insights
        """)
        return
    
    st.markdown("## 📈 Analytics Overview")
    
    total_reviews = len(df)
    avg_rating = df['rating'].mean()
    positive_count = len(df[df['rating'] >= 4])
    negative_count = len(df[df['rating'] <= 2])
    positive_pct = (positive_count / total_reviews * 100) if total_reviews > 0 else 0
    negative_pct = (negative_count / total_reviews * 100) if total_reviews > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="📊 Total Reviews", value=total_reviews, delta="Active")
    
    with col2:
        st.metric(label="⭐ Average Rating", value=f"{avg_rating:.1f}", delta=f"{'📈' if avg_rating >= 3.5 else '📉'}")
    
    with col3:
        st.metric(label="✅ Positive", value=f"{positive_pct:.0f}%", delta=f"{positive_count} reviews")
    
    with col4:
        st.metric(label="⚠️ Negative", value=f"{negative_pct:.0f}%", delta=f"{negative_count} reviews")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rating_chart = create_rating_distribution(df)
        if rating_chart:
            st.plotly_chart(rating_chart, use_container_width=True)
    
    with col2:
        timeline_chart = create_timeline_chart(df)
        if timeline_chart:
            st.plotly_chart(timeline_chart, use_container_width=True)
    
    st.markdown("---")
    st.markdown("## 📋 Recent Feedback")
    
    df = df.sort_values('timestamp', ascending=False).reset_index(drop=True)
    
    for idx in range(len(df)):
        row = df.iloc[idx]
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {get_rating_color(row['rating'])} {'⭐' * int(row['rating'])} ({row['rating']}/5)")
            
            with col2:
                timestamp = pd.to_datetime(row['timestamp']).strftime("%Y-%m-%d %H:%M")
                st.markdown(f"**🕐 {timestamp}**")
            
            border_class = get_border_class(row['rating'])
            
            st.markdown("**📝 Customer Review:**")
            st.info(row['review'])
            
            st.markdown("**💬 AI Response Sent:**")
            st.success(f"*\"{row['ai_response']}\"*")
            
            has_analysis = row['summary'] and str(row['summary']) != '' and str(row['summary']) != 'nan'
            
            if has_analysis:
                st.markdown("---")
                st.markdown("**🔍 AI Analysis Summary:**")
                st.markdown(f"<div class='analysis-box'><strong>{row['summary']}</strong></div>", unsafe_allow_html=True)
                
                st.markdown("**✅ Recommended Actions:**")
                try:
                    actions = json.loads(row['actions'])
                    icons = ["🎯", "📋", "💡"]
                    for i, action in enumerate(actions, 1):
                        icon = icons[i-1] if i <= 3 else "💡"
                        st.markdown(f"{icon} **{i}.** {action}")
                except:
                    st.markdown("- Review feedback and take appropriate action")
                
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    if st.button("🔄 Regenerate", key=f"regen_{idx}"):
                        with st.spinner("🔄 Re-analyzing feedback..."):
                            summary, actions = update_analysis(df, idx)
                            st.success("✅ Analysis updated!")
                            st.rerun()
            else:
                st.markdown("---")
                st.warning("⚠️ AI analysis not generated yet - Click below to analyze")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button(f"🤖 Generate AI Analysis", key=f"analyze_{idx}", use_container_width=True):
                        with st.spinner("🔄 Analyzing feedback with AI..."):
                            summary, actions = update_analysis(df, idx)
                            st.success("✅ Analysis generated!")
                            st.rerun()
            
            st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Powered by Qwen 2 7B • Real-time Feedback Analysis</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()