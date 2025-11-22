import streamlit as st
import openai

st.set_page_config(page_title="SwissHost Assistant", page_icon="🏨")

st.title("🏨 SwissHost Assistant")
st.subheader("Boutique Hotel Review Responder")

# --- Sidebar ---
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    
    if not api_key:
        st.warning("Please enter your API Key to proceed.")
    else:
        openai.api_key = api_key

# --- Main App ---
review_text = st.text_area("Paste Guest Review Here:", height=150)
guest_name = st.text_input("Guest Name (Optional):")
tone = st.selectbox("Select Tone:", ["Warm & Grateful", "Professional & Apologetic", "Neutral"])
language = st.selectbox("Output Language:", ["English", "German (Swiss Standard)", "French", "Italian"])

if st.button("Generate Response", type="primary"):
    if not api_key:
        st.error("Please enter your API key in the sidebar first!")
    elif not review_text:
        st.warning("Please paste a review first.")
    else:
        with st.spinner("Drafting response..."):
            try:
                prompt = f"""
                You are a professional General Manager of a boutique hotel in Switzerland.
                Write a short response to this review: "{review_text}".
                Guest Name: {guest_name if guest_name else 'Guest'}.
                Tone: {tone}.
                Language: {language}.
                """
                
                response = openai.chat.completions.create(
                    model="gpt-4o-mini", # or gpt-3.5-turbo
                    messages=[{"role": "user", "content": prompt}]
                )
                reply = response.choices[0].message.content
                st.success("Response Generated!")
                st.text_area("Copy your response:", value=reply, height=200)
            except Exception as e:
                st.error(f"Error: {e}")
