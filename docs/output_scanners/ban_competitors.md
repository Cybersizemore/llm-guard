# Ban Competitors Scanner

The `BanCompetitors` Scanner is designed to identify and handle mentions of competitors in text generated by Large Language Models (LLMs).
This scanner is essential for businesses and individuals who wish to avoid inadvertently promoting or acknowledging competitors in their automated content.

## Motivation

In the realm of business and marketing, it's crucial to maintain a strategic focus on one's own brand and offerings.
LLMs, while generating content, might unintentionally include references to competing entities. This can be counterproductive, especially in marketing materials, business reports, or any content representing a specific brand or organization.

The `BanCompetitors` Scanner addresses this issue by detecting and managing mentions of competitors.

## How it works

The scanner uses a Named Entity Recognition (NER) model to identify organizations within the text.
After extracting these entities, it cross-references them with a user-provided list of known competitors, which should include all common variations of their names.
If a competitor is detected, the scanner can either flag the text or redact the competitor's name based on user preference.

Models:
- [tomaarsen/span-marker-bert-small-orgs](https://huggingface.co/tomaarsen/span-marker-bert-small-orgs)
- [tomaarsen/span-marker-bert-base-orgs](https://huggingface.co/tomaarsen/span-marker-bert-base-orgs)

## Usage

```python
from llm_guard.output_scanners import BanCompetitors

competitor_list = ["Competitor1", "CompetitorOne", "C1", ...]  # Extensive list of competitors
scanner = BanCompetitors(competitors=competitor_list, redact=False, threshold=0.5)
sanitized_output, is_valid, risk_score = scanner.scan(prompt, output)
```

**An effective competitor list should include:**

- The official names of all known competitors.
- Common abbreviations or variations of these names.
- Any subsidiaries or associated brands of the competitors.
- The completeness and accuracy of this list are vital for the effectiveness of the scanner.

## Considerations and Limitations

- **Accuracy**: The accuracy of competitor detection relies heavily on the NER model's capabilities and the comprehensiveness of the competitor list.
- **Context Awareness**: The scanner may not fully understand the context in which a competitor's name is used, leading to potential over-redaction.
- **Performance**: The scanning process might add additional computational overhead, especially for large texts with numerous entities.

## Optimization Strategies

ONNX support for this scanner is currently in development ([PR](https://github.com/tomaarsen/SpanMarkerNER/pull/43)).

## Benchmark

Environment:

- Platform: Amazon Linux 2
- Python Version: 3.11.6

Run the following script:

```sh
python benchmarks/run.py output BanCompetitors
```

Results:

WIP