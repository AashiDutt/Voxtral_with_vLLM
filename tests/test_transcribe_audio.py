import pytest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import transcribe_audio


class TestTranscribeAudio:
    """Test cases for the transcribe_audio function."""

    @patch('app.OpenAI')
    def test_transcribe_audio_success(self, mock_openai):
        """Test successful transcription with mock response."""
        # Create a mock client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Create mock response chunks
        mock_chunks = [
            MagicMock(choices=[{"delta": {"content": "Hello"}}]),
            MagicMock(choices=[{"delta": {"content": " world"}}]),
            MagicMock(choices=[{"delta": {"content": "!"}}]),
        ]
        
        # Configure the mock client to return our mock chunks
        mock_client.audio.transcriptions.create.return_value = mock_chunks
        
        # Mock the file opening
        with patch('builtins.open', mock_open()):
            result = transcribe_audio(mock_client, 'test_audio.mp3')
            
        # Assertions
        assert result == "Hello world!"
        mock_client.audio.transcriptions.create.assert_called_once()
        
    @patch('app.OpenAI')
    def test_transcribe_audio_with_none_delta(self, mock_openai):
        """Test transcription when some chunks have None delta."""
        # Create a mock client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Create mock response chunks with some None deltas
        mock_chunks = [
            MagicMock(choices=[{"delta": {"content": "Hello"}}]),
            MagicMock(choices=[{"delta": None}]),
            MagicMock(choices=[{"delta": {"content": " world"}}]),
        ]
        
        # Configure the mock client to return our mock chunks
        mock_client.audio.transcriptions.create.return_value = mock_chunks
        
        # Mock the file opening
        with patch('builtins.open', mock_open()):
            result = transcribe_audio(mock_client, 'test_audio.mp3')
            
        # Assertions
        assert result == "Hello world"
        mock_client.audio.transcriptions.create.assert_called_once()
        
    @patch('app.st')
    @patch('app.OpenAI')
    def test_transcribe_audio_exception_handling(self, mock_openai, mock_st):
        """Test exception handling in transcribe_audio function."""
        # Create a mock client that raises an exception
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.audio.transcriptions.create.side_effect = Exception("Test error")
        
        # Mock the file opening
        with patch('builtins.open', mock_open()):
            result = transcribe_audio(mock_client, 'test_audio.mp3')
            
        # Assertions
        assert result is None
        mock_st.error.assert_called_once_with("Error during transcription: Test error")
        
    @patch('app.time.sleep')  # Mock time.sleep to speed up tests
    @patch('app.st')
    @patch('app.OpenAI')
    def test_transcribe_audio_ui_elements(self, mock_openai, mock_st, mock_sleep):
        """Test that UI elements are properly managed during transcription."""
        # Create a mock client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Create mock response chunks
        mock_chunks = [
            MagicMock(choices=[{"delta": {"content": "Hello"}}]),
            MagicMock(choices=[{"delta": {"content": " world"}}]),
        ]
        
        # Configure the mock client to return our mock chunks
        mock_client.audio.transcriptions.create.return_value = mock_chunks
        
        # Create mock UI elements
        mock_progress_bar = MagicMock()
        mock_status_text = MagicMock()
        mock_st.progress.return_value = mock_progress_bar
        mock_st.empty.return_value = mock_status_text
        
        # Mock the file opening
        with patch('builtins.open', mock_open()):
            result = transcribe_audio(mock_client, 'test_audio.mp3')
            
        # Assertions
        assert result == "Hello world"
        # Check that progress bar was called with 1.0 (completion)
        mock_progress_bar.progress.assert_called_with(1.0)
        # Check that UI elements were cleaned up
        mock_progress_bar.empty.assert_called_once()
        mock_status_text.empty.assert_called_once()