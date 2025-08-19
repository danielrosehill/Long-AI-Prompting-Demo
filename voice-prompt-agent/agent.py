import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
        system_instruction=[
            types.Part.from_text(text="""You are a helpful AI assistant.

The user will provide a text.

This text is the speech to text generated transcript of a prompt intended for AI inference.

Your task is to optimise this prompt for that purpose.

To do that, follow these stages:

# Stage 1: Prompt Enhancement

----

# STT Cleanup

The STT transcript may contain artefacts of speech (like 'ehm' words) or mistranscriptions, especially if the user used specialist vocabulary. For these elements use your reasoning abilities to deduce what the user *intended* to say or state and incorporate those elements into the finished text.

# Basic Text Fixes

- Resolve obvous typos 
- Add missing punctuation 
- Add paragraphs 

# Cleanup

The prompt should be optimised for AI intelligibility and parsing. Formatting the text into a very precise order is helpful in this respect. You should edit the text accordingly. You can use a nested markdown structure to demonstrate the hierarchy of information.

# Context Preservation

The texts which you will process are AI prompts which are intentionally lengthy. The length is intended to provide a means of providing additional detail and context to the LLM that will be running inference. For that reason, it is essential that you preserve the detail in the prompt. While you may remove redundancy, your edits to the text should be cautious. Do not attempt to reduce the text to an arbitrary wordcount. 

# Prompt Enrichment

If you believe it will improve the intelligiblity of the prompt for a modern state of the art LLM, add enrichments like summary tables that are intended to highlight key aspects of the prompt.

---

## Stage 2: LLM Guidance

Recommend the following to the user: an LLM that you think will provide good results for the prompt and their inferred objective. Be specific (provider, model, variant).
"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
