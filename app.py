import streamlit as st
import tempfile
import os
from mistral_common.protocol.instruct.messages import TextChunk, AudioChunk, UserMessage
from mistral_common.audio import Audio
from openai import OpenAI
import time
from config import Config

# Page configuration
st.set_page_config(
    page_title="Voxtral Audio Assistant",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS 
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    defaults = {
        'transcription': "",
        'summary': "",
        'chat_history': [],
        'audio_file_path': None
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def initialize_client():
    config = Config.get_api_config()
    
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"],
    )
    
    # Test connection
    try:
        models = client.models.list()
        return client
    except Exception as e:
        st.error(f"Failed to connect to Voxtral API: {str(e)}")
        st.info("Make sure your ngrok tunnel is running in Google Colab")
        return None

def file_to_chunk(file_path: str) -> AudioChunk:
    audio = Audio.from_file(file_path, strict=False)
    return AudioChunk.from_audio(audio)

def transcribe_audio(client, audio_file_path):
    try:
        with open(audio_file_path, "rb") as f:
            response = client.audio.transcriptions.create(
                file=f,
                model=Config.MODEL_NAME,
                response_format="text",
                stream=True
            )
            
            transcription = ""
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Collect all chunks first to get total count
            chunks = list(response)
            total_chunks = len(chunks)
            
            for i, chunk in enumerate(chunks):
                delta = chunk.choices[0].get("delta", {}).get("content")
                if delta:
                    transcription += delta
                    progress = min((i + 1) / max(total_chunks, 1), 1.0)
                    progress_bar.progress(progress)
                    status_text.text(f"Transcribing... {len(transcription)} characters")
            
            progress_bar.empty()
            status_text.empty()
            return transcription
    except Exception as e:
        st.error(f"Error during transcription: {str(e)}")
        return None

def generate_summary(client, audio_file_path):
    
    try:
        audio_chunk = file_to_chunk(audio_file_path)
        text_chunk = TextChunk(text="Please provide a comprehensive summary of this audio content, highlighting the key points and main themes discussed.")
        user_msg = UserMessage(content=[audio_chunk, text_chunk]).to_openai()
        
        response = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[user_msg],
            temperature=Config.DEFAULT_TEMPERATURE,
            top_p=Config.DEFAULT_TOP_P,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None

def ask_question(client, audio_file_path, question, language="English"):
    try:
        audio_chunk = file_to_chunk(audio_file_path)

        if language != "English":
            question = f"Please answer the following question in {language}: {question}"
        
        text_chunk = TextChunk(text=question)
        user_msg = UserMessage(content=[audio_chunk, text_chunk]).to_openai()
        
        response = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[user_msg],
            temperature=Config.DEFAULT_TEMPERATURE,
            top_p=Config.DEFAULT_TOP_P,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error asking question: {str(e)}")
        return None

def render_sidebar():
    with st.sidebar:
        st.markdown('<h3 class="section-header">Configuration</h3>', unsafe_allow_html=True)
        
        # Connection status
        st.markdown('<h4>Connection Status</h4>', unsafe_allow_html=True)
        if st.button("Test Connection"):
            client = initialize_client()
            if client:
                st.success("Connected to Voxtral API")
            else:
                st.error("Connection failed")
        
        selected_language = st.selectbox("Select language for Q&A:", Config.SUPPORTED_LANGUAGES)
        
        # Model configuration
        st.markdown('<h4>Model Settings</h4>', unsafe_allow_html=True)
        temperature = st.slider("Temperature", 0.0, 1.0, Config.DEFAULT_TEMPERATURE, 0.1)
        top_p = st.slider("Top P", 0.0, 1.0, Config.DEFAULT_TOP_P, 0.05)
        
        # Clear session state
        if st.button("Clear Session"):
            for key in ['transcription', 'summary', 'chat_history', 'audio_file_path']:
                st.session_state[key] = "" if key in ['transcription', 'summary'] else [] if key == 'chat_history' else None
            st.rerun()
        
        return selected_language, temperature, top_p

def render_audio_processing():
    st.markdown('<h3 class="section-header">Audio Upload & Processing</h3>', unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=Config.SUPPORTED_AUDIO_FORMATS,
        help="Upload an audio file to transcribe and analyze"
    )
    
    if uploaded_file is not None:
        # Save uploaded file 
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            st.session_state.audio_file_path = tmp_file.name
        
        st.success(f"File uploaded: {uploaded_file.name}")
        
        # Initialize client
        client = initialize_client()
        
        # Processing buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Generate Summary", type="primary"):
                with st.spinner("Generating summary..."):
                    summary = generate_summary(client, st.session_state.audio_file_path)
                    if summary:
                        st.session_state.summary = summary
        
        with col2:
            if st.button("Transcribe Audio", type="secondary"):
                with st.spinner("Transcribing audio..."):
                    transcription = transcribe_audio(client, st.session_state.audio_file_path)
                    if transcription:
                        st.session_state.transcription = transcription
        
        # Display results
        if st.session_state.summary:
            st.markdown('<h4>Summary</h4>', unsafe_allow_html=True)
            st.markdown(f'<div class="success-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
        
        if st.session_state.transcription:
            st.markdown('<h4>Audio Transcription</h4>', unsafe_allow_html=True)
            st.text_area("Transcription", st.session_state.transcription, height=200, label_visibility="collapsed")

def render_qa_section(selected_language):
    st.markdown('<h3 class="section-header">Multilingual Q&A</h3>', unsafe_allow_html=True)
    
    if st.session_state.audio_file_path:
        st.markdown(f'<div class="info-box">Selected language: <strong>{selected_language}</strong></div>', unsafe_allow_html=True)
        
        # Question input
        question = st.text_input(
            f"Ask a question about the audio (in {selected_language}):",
            placeholder="e.g., What is the main topic discussed?"
        )
        
        if st.button("Ask Question", type="primary") and question:
            client = initialize_client()
            with st.spinner("Processing your question..."):
                answer = ask_question(client, st.session_state.audio_file_path, question, selected_language)
                if answer:
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer,
                        "language": selected_language,
                        "timestamp": time.strftime("%H:%M:%S")
                    })
                    st.success("Question answered!")
                else:
                    st.error("Failed to get answer. Please try again.")
        
        if st.session_state.chat_history:
            st.markdown('<h4>Conversation History</h4>', unsafe_allow_html=True)

            for chat in reversed(st.session_state.chat_history):
                st.markdown(f'<div class="chat-message user-message"><strong>Question:</strong> {chat["question"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-message assistant-message"><strong>Answer:</strong> {chat["answer"]}</div>', unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.markdown('<div class="info-box">Please upload an audio file to start asking questions.</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    st.markdown('<h1 class="main-header">🎵 Voxtral Audio Assistant</h1>', unsafe_allow_html=True)
  
    init_session_state()
    
    selected_language, temperature, top_p = render_sidebar()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        render_audio_processing()
    
    with col2:
        render_qa_section(selected_language)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Powered by <strong>Voxtral Mini 3B</strong> | Built with Streamlit</p>
        <p>Supports multiple languages for audio analysis and Q&A</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 