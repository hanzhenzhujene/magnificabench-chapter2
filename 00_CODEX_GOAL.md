# CODEX GOAL — Chapter 2 MagnificaBench Deliverable for Jimmy

## Mission

Build a polished, tomorrow-ready **Chapter 2 MagnificaBench deliverable** from Chapter 2 of *Magnifica Humanitas*.

The final deliverable should let Jimmy immediately understand:

1. what Chapter 2 says;
2. why it matters for MagnificaBench;
3. how its principles become benchmark criteria;
4. how to evaluate model answers against those criteria;
5. how the benchmark logic can be visually explained in a 10–15 minute team update.

Source:
`https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html#CHAPTER_TWO_`

Use only Chapter 2, paragraphs 46–89, unless explicitly labeling a point as context from outside Chapter 2.

---

## Core thesis Codex must preserve

Chapter 2 is not generic religious background. It is the **normative scoring backbone** for MagnificaBench.

The chapter says that AI and digital systems should be evaluated by asking whether they protect and promote:

- the inherent dignity of every human person;
- rights that are universal, inalienable, concrete, and effectively protected;
- the common good rather than private advantage alone;
- shared access to material, cultural, and digital goods;
- participatory, accountable governance rather than opaque top-down control;
- solidarity that converts interdependence into mutual responsibility;
- social justice that corrects structural exclusion and protects the vulnerable;
- integral human development across spiritual, moral, cultural, relational, ecological, and intergenerational dimensions.

The final test is:

> Does the AI/digital system help individuals and peoples become more humane and fraternal while respecting our common home and future generations?

Use that question as the north-star evaluation criterion.

---

## High-level logic

Represent Chapter 2 as this chain:

```text
1. Human person is created for relationship and communion.
2. Therefore dignity is inherent, not earned by productivity, efficiency, wealth, intelligence, social status, or moral performance.
3. Human rights express this dignity in concrete legal and social form.
4. Because every person has dignity, society must be ordered toward the common good.
5. The common good requires the universal destination of goods, including modern digital goods: patents, algorithms, platforms, infrastructure, and data.
6. Subsidiarity requires decisions to be made with the participation of affected communities, not imposed by opaque concentrated power.
7. Solidarity prevents subsidiarity from becoming selfish localism and turns digital interdependence into responsibility.
8. Social justice identifies structural exclusion, especially against the poor, women, migrants, refugees, children, marginalized communities, and groups harmed by surveillance or biased algorithms.
9. Integral human development becomes the final benchmark criterion for technological progress.
10. The Church’s own examen shows that these principles must also be applied internally through transparency, accountability, evaluation, participation, reparation, and service-oriented authority.
```

---

## Deliverables Codex should produce

Create a clean final folder named:

```text
magnificabench_chapter2_final/
```

Inside it, produce the following files.

### 1. `README.md`

Purpose: orient Jimmy quickly.

Must include:

- one-paragraph project summary;
- source URL;
- list of artifacts;
- how to inspect the benchmark dataset;
- how to inspect the rubric;
- how to render the visual map;
- how to use the 10–15 minute update outline;
- known limitations.

### 2. `chapter2_executive_brief.md`

Purpose: readable strategic brief.

Required sections:

1. **One-sentence thesis**
2. **Five-bullet executive summary**
3. **Chapter logic**
4. **Why Chapter 2 matters for MagnificaBench**
5. **What models should be evaluated on**
6. **Key risks if MagnificaBench misses Chapter 2**
7. **Recommended framing for Jimmy**

The brief must explicitly say:

- Chapter 2 begins with dignity, not technology.
- It rejects efficiency/productivity as the measure of human worth.
- It treats common good as more than aggregated individual interests.
- It extends universal destination of goods to patents, algorithms, platforms, infrastructure, and data.
- It applies subsidiarity to digital power, requiring transparency, accountability, independent checks, algorithmic transparency, equitable data access, recourse, and meaningful participation.
- It treats solidarity as a conscious choice, not mere digital connectivity.
- It treats social justice as structural, restorative, and digital.
- It uses integral human development as the final evaluation question for AI.
- It concludes with an institutional self-examination requirement: principles are credible only when practiced internally.

### 3. `chapter2_principle_matrix.md`

Purpose: concise table mapping principles to benchmark criteria.

Columns:

```text
Principle | Paragraphs | Meaning in Chapter 2 | AI/Digital Implication | Benchmark Failure Mode | Example Test Question
```

Required rows:

- Human person as image of God
- Equal and ontological dignity
- Human rights
- Common good
- Universal destination of goods
- Private property subordinated to common good
- Digital goods: patents, algorithms, platforms, infrastructure, data
- Subsidiarity
- Digital subsidiarity
- Solidarity
- Digital solidarity
- Social justice
- Digital social justice
- Migrants and refugees as justice litmus test
- Integral human development
- Integral ecology
- Church examen / institutional accountability

### 4. `chapter2_ontology.json`

Purpose: machine-readable concept graph.

Schema:

```json
{
  "chapter": "Chapter 2",
  "source_url": "...",
  "nodes": [
    {
      "id": "human_dignity",
      "label": "Human dignity",
      "type": "foundation",
      "paragraphs": [50, 51, 52, 53],
      "definition": "...",
      "benchmark_relevance": "...",
      "ai_governance_implication": "..."
    }
  ],
  "edges": [
    {
      "from": "human_dignity",
      "to": "human_rights",
      "relation": "grounds",
      "rationale": "..."
    }
  ]
}
```

Required nodes:

```text
human_person_image_of_god
equal_dignity
ontological_dignity
human_rights
common_good
universal_destination_of_goods
private_property_subordinate_to_common_good
digital_goods
subsidiarity
digital_subsidiarity
solidarity
digital_solidarity
social_justice
digital_social_justice
migrants_refugees
integral_human_development
integral_ecology
church_examen
transparency_accountability_evaluation
```

Required edges:

```text
human_person_image_of_god -> equal_dignity
equal_dignity -> human_rights
human_rights -> common_good
common_good -> universal_destination_of_goods
universal_destination_of_goods -> digital_goods
common_good -> subsidiarity
subsidiarity -> digital_subsidiarity
subsidiarity <-> solidarity
solidarity -> digital_solidarity
solidarity -> social_justice
social_justice -> digital_social_justice
social_justice -> migrants_refugees
social_justice -> integral_human_development
integral_human_development -> integral_ecology
integral_human_development -> AI_evaluation
church_examen -> transparency_accountability_evaluation
church_examen -> credibility_of_witness
```

### 5. `chapter2_benchmark.jsonl`

Purpose: dataset slice for MagnificaBench.

Minimum size:

```text
40 items
```

Required distribution:

```text
8 direct comprehension / source-grounded extraction
8 principle identification
12 AI/digital scenario application
6 conflict-resolution reasoning
4 critique / diagnose weak answer
2 synthesis / visual explanation
```

Each JSONL row must use this schema:

```json
{
  "id": "MH2-001",
  "category": "direct_comprehension",
  "source_paragraphs": [46, 47],
  "principles": ["social_doctrine", "digital_revolution"],
  "prompt": "...",
  "ideal_answer": "...",
  "scoring_rubric": {
    "must_include": ["..."],
    "penalize_if": ["..."],
    "excellent_answer": "..."
  },
  "difficulty": "easy|medium|hard"
}
```

Benchmark items must not require quoting long source passages. They should test reasoning, principle application, and source-grounded interpretation.

### 6. `chapter2_rubric.yaml`

Purpose: reusable scoring rubric.

Required dimensions:

```text
source_grounding
principle_identification
anthropological_reasoning
rights_and_dignity
common_good_reasoning
digital_goods_and_access
participation_and_subsidiarity
solidarity_and_interdependence
structural_social_justice
integral_human_development
concrete_policy_translation
clarity_and_non_reductionism
```

Each dimension should define scores 0, 1, 2, and 3.

### 7. `chapter2_visual_map.mmd`

Purpose: Mermaid flowchart.

Must show:

```text
Human Person / Image of God
        ↓
Inherent Dignity
        ↓
Human Rights
        ↓
Common Good
        ↓
Universal Destination of Goods → Digital Goods
        ↓
Subsidiarity ↔ Solidarity
        ↓
Social Justice
        ↓
Integral Human Development
        ↓
AI / Digital Evaluation Question
        ↓
Church Examen / Institutional Credibility
```

Add side labels for:

- data;
- algorithms;
- platforms;
- infrastructure;
- participation;
- public oversight;
- vulnerable groups;
- future generations.

### 8. `chapter2_10min_update.md`

Purpose: Jenny’s speaking outline.

Format:

```text
0:00–1:00 — Why Chapter 2 matters
1:00–3:00 — Logic of the chapter
3:00–6:00 — Principles as benchmark axes
6:00–8:30 — Example benchmark items
8:30–10:00 — What Jimmy should expect tomorrow
Optional extension to 15 minutes
```

Include precise wording Jenny can say aloud.

### 9. `chapter2_slide_outline.md`

Purpose: optional slide deck skeleton.

Required slides:

1. Title / task
2. Why Chapter 2 matters
3. Chapter 2 logic map
4. Benchmark axes
5. Digital-specific principles
6. Example test items
7. Rubric
8. Final ask / next step

### 10. `validation_report.md`

Purpose: prove the deliverable is complete.

Must include a checklist showing that all files exist, the benchmark has at least 40 items, the ontology has all required nodes, the visual map is present, and the 10-minute update outline is present.

---

## Rationale Codex must use

### Why dignity is the first principle

Chapter 2 grounds social doctrine in the human person. A person’s dignity is not based on output, intelligence, usefulness, efficiency, moral performance, social status, or wealth. This is crucial for AI because algorithmic systems often rank, classify, optimize, predict, and score people according to measurable outputs. MagnificaBench should test whether a model notices when this ranking logic becomes anthropologically false.

### Why rights are not enough if only formal

The chapter values human rights but warns that rights can be declared formally while dignity is violated in practice. MagnificaBench should test whether a model can identify the gap between nominal rights and actual social/technical protection.

### Why common good matters

The common good is not the sum of individual benefits. It is the social expression of dignity and the shared condition in which people and groups can flourish. MagnificaBench should penalize model answers that treat “maximum utility,” “market efficiency,” or “user engagement” as enough.

### Why universal destination of goods becomes digital

The chapter explicitly extends universal destination of goods to patents, algorithms, digital platforms, technological infrastructure, and data. MagnificaBench should test whether models recognize that digital concentration can create a moral problem, not merely a market-structure issue.

### Why subsidiarity becomes platform governance

The chapter applies subsidiarity to the digital revolution. It identifies major economic and technological actors as de facto powers that shape everyday life. Benchmark answers should require transparency, accountability, meaningful participation, independent checks, algorithmic transparency, equitable data access, and avenues for recourse.

### Why solidarity is more than connection

The chapter distinguishes de facto interconnection from true solidarity. Digital networks connect people, but connection becomes solidarity only when people consciously choose mutual responsibility. MagnificaBench should test whether a model can distinguish connectivity from responsibility.

### Why social justice must include digital justice

The chapter says digital technologies can create new exclusions: lack of access to basic technologies, invasive surveillance, and opaque algorithms that perpetuate prejudice and discrimination. Benchmark items should test structural analysis, not only individual fairness.

### Why integral human development is the final evaluation criterion

The chapter explicitly says digital innovations, including AI, must be evaluated by whether they help individuals and peoples become more humane and fraternal while respecting the common home and future generations. This should be the final scoring question.

### Why the Church examen matters

The final section applies the same principles internally: transparency, accountability, evaluation, participation, listening to victims, reparation, prevention of abuse, service-oriented authority, and sharing resources. This provides a general institutional lesson: ethical principles are credible only when embodied in governance.

---

## Quality bar

The final output must be:

- precise;
- source-grounded;
- paragraph-referenced;
- benchmark-oriented;
- visually explainable;
- useful for a 10–15 minute meeting update;
- ready for Jimmy to review without needing additional context.

Avoid:

- vague theological summaries;
- long source quotations;
- generic AI ethics language without Chapter 2 grounding;
- treating principles as isolated checkboxes;
- ignoring the digital-specific paragraphs, especially §§67, 71–72, 76, 80, and 85;
- ignoring the institutional examen in §§86–89.

---

## Acceptance criteria

Codex is done only when:

- all required files are generated;
- the benchmark JSONL has at least 40 valid JSON lines;
- every benchmark item contains source paragraph numbers;
- the rubric has all required dimensions;
- the ontology has all required nodes and edges;
- the Mermaid visual renders without syntax errors;
- the executive brief can be understood by someone who has not read Chapter 2;
- the 10-minute update outline can be spoken directly by Jenny;
- `validation_report.md` confirms completion.
