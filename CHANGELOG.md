# Changelog

## v2.0.0 - 2025-07-25

### Optimized
- Improved memory usage in `transcribe_audio` function by processing chunks as they arrive instead of collecting all chunks first
- Reduced UI update frequency during transcription to improve performance
- Ensured proper cleanup of UI elements after transcription completion

### Fixed
- Fixed handling of None delta values in transcription chunks

## v1.0.0 - 2025-07-24

### Added
- Initial release of Voxtral Audio Assistant
- Audio transcription with real-time progress
- Content summarization
- Multilingual Q&A capabilities
- Clean, responsive Streamlit UI