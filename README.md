# Long Prompting Experiment

## Description 

Modern LLMs show continuously more powerful abilities to handle large context windows. While research [has shown](https://ar5iv.labs.arxiv.org/html/2402.14848v1) that the coherence of inference can degrade with longer prompts, the curve can be expected to get progressively flatter. 

Gemini 2.5 Lite supports a maximum context of a little over one million tokens. The "raw" unredacted transcript prompt and the AI enhanced (and streamlined) prompt use up just 0.35% and 0.17% of that window respectively! 

The upside to using lengthier prompting is that it provides models with the ability to ingest context data from a direct mechanism that does not require complex mechanisms like RAG. The downside - besides potentially degraded inference if taken 'too far' - is that it requires significant effort on the part of the user. 

This experiment/demo compares the differences in inference quality for a hypothetical tech projects between:

1: A minimalist "low effort" user prompt (formulated to reflect typical casual conversational LLM usage)

2: A voice prompt (transcribed with spech to text) that underwent preprocessing by a specialised voice prompt refinement agent whose task was to optimise the prompt for clear and useful inference 

3: The same voice prompt without the preprocessing agent. In this model the raw STT transcript was fed directly to the LLM as the user prompt

To allow for the best possiblity of success while standardising conditions the same LLM (Gemini 2.5 Lite), system prompt, and temperature (default, 1.0) was used across runs.

---

## Analyses

Gemini's [/analysis/gemini-self-analysis](self reflections!)

