# Prompt Parameters & Word Counts

## File Statistics

| File | Word Count | Characters | Est. Tokens (Conservative) | Est. Tokens (Optimistic) | Type | Description |
|------|------------|------------|----------------------------|---------------------------|------|-------------|
| `control.md` | 30 words | 230 | ~58 tokens | ~40 tokens | Control/Baseline | Short, direct question about IP camera monitoring setup |
| `gemini-optimised.md` | 981 words | 6,875 | ~1,719 tokens | ~1,307 tokens | Structured/Optimized | Comprehensive, well-organized technical consultation request |
| `raw-audio.md` | 2,617 words | 13,945 | ~3,486 tokens | ~3,488 tokens | Voice Transcript | Unstructured voice-to-text transcription with detailed context |
 

## Analysis Summary

- **Total corpus**: 3,818 words / 22,325 characters across 4 files
- **Total tokens**: ~5,582 tokens (conservative) / ~5,088 tokens (optimistic)
- **Average length**: 955 words per file (excluding params.md)
- **Token range**: 40 - 3,488 tokens (139x difference between shortest and longest)
- **Primary domain**: Technical consultation for home automation/monitoring systems
- **Common themes**: IP cameras, baby monitoring, AI/ML integration, hardware recommendations, Home Assistant

## Tokenization Methodology

- **Conservative estimate**: 4 characters per token (accounts for punctuation and formatting)
- **Optimistic estimate**: 1.33 tokens per word (typical English text ratio)
- **Most efficient**: `control.md` at ~1.3-1.9 tokens per word
- **Least efficient**: `raw-audio.md` due to conversational redundancy

## Prompt Characteristics

- **Technical depth**: High technical detail with specific hardware/software references
- **Personal context**: Strong personal motivation (newborn safety)
- **Multi-faceted requests**: Hardware, software, integration, and implementation guidance
- **Local constraints**: Geographic limitations (Israel), specific vendor preferences
- **Integration requirements**: Home Assistant, MQTT, alerting systems
