# 🎵 Voxtral Audio Assistant

A comprehensive Streamlit application that leverages Voxtral Mini 3B for audio processing, transcription, summarization, and multilingual Q&A capabilities.

## ✨ Features

- **🎯 Audio Transcription**: Automatically transcribe uploaded audio files
- **📋 Content Summarization**: Generate comprehensive summaries of audio content
- **💬 Multilingual Q&A**: Ask questions about audio content in multiple languages
- **🎨 Modern UI**: Beautiful, responsive interface with real-time progress indicators
- **📱 Session Management**: Persistent chat history and file management
- **⚙️ Configurable**: Adjustable model parameters (temperature, top_p)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Voxtral API endpoint (you can run Voxtral locally or use a hosted service)
- For Google Colab setup: ngrok account (free at https://ngrok.com)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd Voxtral-Demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Voxtral API**
   
   Edit `app.py` and update the API endpoint:
   ```python
   # In the initialize_client() function
   openai_api_base = "https://your-voxtral-endpoint.com/v1"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

### 🚀 Google Colab Setup (Recommended for T4 GPU)

For users with limited local resources, you can run Voxtral in Google Colab with T4 GPU:

1. **Run the Colab setup script:**
   ```bash
   python colab_setup.py
   ```

2. **Upload `colab_vllm_setup.ipynb` to Google Colab**

3. **Get your ngrok auth token** from https://dashboard.ngrok.com/get-started/your-authtoken

4. **Run the notebook in Colab** - this will start vLLM and create an ngrok tunnel

5. **Copy the ngrok URL** and update your local configuration:
   ```bash
   python update_ngrok_url.py https://your-ngrok-url.ngrok-free.app
   ```

6. **Run the Streamlit app locally:**
   ```bash
   streamlit run app.py
   ```

**Note:** Keep the Colab notebook running to maintain the ngrok tunnel.

## 📖 Usage Guide

### 1. Audio Upload
- Click "Browse files" to upload an audio file
- Supported formats: MP3, WAV, M4A, FLAC, OGG
- The file will be temporarily stored for processing

### 2. Audio Processing
- **Generate Summary**: Click to create a comprehensive summary of the audio content
- **Transcribe Audio**: Click to get the full text transcription with real-time progress

### 3. Multilingual Q&A
- Select your preferred language from the sidebar
- Type your question in the text input
- Click "Ask Question" to get an AI-powered response
- View conversation history in expandable sections

### 4. Configuration
- **Language Selection**: Choose from 12 supported languages
- **Model Parameters**: Adjust temperature and top_p for response generation
- **Session Management**: Clear session data when needed

## 🌍 Supported Languages

- English
- Spanish
- French
- German
- Italian
- Portuguese
- Russian
- Chinese
- Japanese
- Korean
- Arabic
- Hindi

## 🔧 Configuration

### Voxtral API Setup

1. **Local Setup** (Recommended for development):
   ```bash
   # Install vLLM
   pip install vllm
   
   # Run Voxtral locally
   vllm serve mistralai/Voxtral-Mini-3B-2507 --host 0.0.0.0 --port 8000
   ```

2. **Update API endpoint in app.py**:
   ```python
   openai_api_base = "http://localhost:8000/v1"
   ```

### Environment Variables

You can also use environment variables for configuration:
```bash
export VOXTRAL_API_BASE="http://localhost:8000/v1"
export VOXTRAL_API_KEY="your-api-key"
```

## 📁 Project Structure

```
Voxtral-Demo/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── audio_qa.ipynb        # Original Q&A notebook
├── transcription.ipynb   # Original transcription notebook
├── translation.ipynb     # Original translation notebook
├── sample_audio.mp3      # Sample audio file
└── output.wav           # Output file
```

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: OpenAI-compatible API client for Voxtral
- **Audio Processing**: Mistral Common library for audio chunking
- **Session Management**: Streamlit session state for persistence

### Key Functions
- `initialize_client()`: Sets up OpenAI client for Voxtral API
- `file_to_chunk()`: Converts audio files to AudioChunk format
- `transcribe_audio()`: Handles audio transcription with streaming
- `generate_summary()`: Creates content summaries
- `ask_question()`: Processes multilingual Q&A requests

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Verify your Voxtral endpoint is running
   - Check network connectivity
   - Ensure correct API base URL

2. **Audio Processing Errors**
   - Verify audio file format is supported
   - Check file size (recommended < 100MB)
   - Ensure audio file is not corrupted

3. **Memory Issues**
   - Reduce audio file size
   - Clear session data periodically
   - Restart the application if needed

### Debug Mode

Enable debug logging by adding this to your environment:
```bash
export STREAMLIT_LOG_LEVEL=debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Mistral AI](https://mistral.ai/) for Voxtral model
- [Streamlit](https://streamlit.io/) for the web framework
- [vLLM](https://github.com/vllm-project/vllm) for model serving

## 📞 Support

For issues and questions:
- Create an issue in this repository
- Check the troubleshooting section above
- Refer to Voxtral documentation at [Hugging Face](https://huggingface.co/mistralai/Voxtral-Mini-3B-2507) 