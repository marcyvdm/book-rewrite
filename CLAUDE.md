# Claude Code Instructions

## Book Rewriting Project - Game Feel

This project focuses on enhancing and condensing "Game Feel: A Game Designer's Guide to Virtual Sensation" by Steve Swink while preserving the author's unique voice and pedagogical approach.

## Project Structure

### Data Files
```
game-feel/
├── metadata.json          # Complete voice profile and preservation rules
├── chapter_01.json        # Introduction chapter in structured format
├── chapter_02.json        # Chapter 2 content (repeat for all chapters)
└── images/               # All book images (16.png, 21.png, etc.)
```

### Agent System
```
.claude/
└── agents/
    └── chapter-enhancer.md  # Single comprehensive agent for chapter processing
```

## Chapter Enhancement Workflow

### 1. Input Requirements
To process a chapter, the agent needs:
- **metadata.json**: Voice profile, style guidelines, preservation rules
- **chapter_XX.json**: Original chapter content with paragraphs, headings, images
- **images/**: Referenced images for the chapter

### 2. Processing Goals
- **30% length reduction** while preserving all core concepts
- **Voice preservation**: Maintain Steve Swink's conversational yet professional tone
- **Traceability**: Complete mapping between original and enhanced paragraphs
- **Quality assurance**: Preserve all "never reduce" elements

### 3. Key Preservation Rules

#### MUST PRESERVE (Never Reduce):
- The Three Building Blocks of Game Feel definition
- The Six Metrics (Input, Response, Context, Polish, Metaphor, Rules)
- Step-by-step deconstructions in case studies
- The seven principles of game feel
- Core metaphors (game feel as physical sensation, design as tuning)
- Playable example references and instructions

#### SAFE TO CONDENSE:
- Extended historical context (keep relevance, reduce detail)
- Multiple examples making the same point (keep best 1-2)
- Biographical details not directly related to points
- Repetitive explanations (consolidate pedagogically)

## Voice Profile Summary

### Steve Swink's Writing Style
- **Signature phrases**: "What's interesting is that...", "The question is..."
- **Tone shifts**: Academic for definitions, conversational for stories, instructional for examples
- **Engagement**: Direct reader address with "you," "we," and "I"
- **Structure**: Examples → theory (inductive reasoning)
- **Conclusions**: Clear, punchy endings after complex explanations

### Chapter-Specific Guidelines

#### Introduction/Definition Chapters (1-5)
- Preserve all foundational definitions
- Maintain inductive flow (examples → theory)
- Keep personal anecdotes for relatability

#### Metrics Chapters (6-11)
- Preserve all metric definitions
- Keep at least one concrete example per metric
- Consolidate similar examples

#### Case Study Chapters (12-16)
- Never reduce step-by-step analysis
- Keep all parameter values and relationships
- May condense historical context

#### Principles Chapter (17)
- Preserve all seven principles
- Keep synthesis of earlier concepts
- Ensure actionable takeaways

## Output Format

The enhanced chapter should include:
```json
{
  "chapter_metadata": {
    "chapter_number": 1,
    "title": "Introduction",
    "reduction_percentage": 30,
    "preserved_elements": ["core_thesis", "three_building_blocks"],
    "voice_consistency_score": 0.95
  },
  "enhanced_content": [...],
  "mapping_summary": {...},
  "quality_checks": {...}
}
```

## Quality Validation Checklist

- [ ] Core thesis preserved and clear
- [ ] All "never reduce" elements intact
- [ ] 25-35% reduction achieved
- [ ] Steve Swink's voice maintained
- [ ] Paragraph mappings complete
- [ ] Images properly referenced
- [ ] Learning objectives achievable
- [ ] Technical terms consistent
- [ ] Logical flow maintained

## Usage Instructions

1. **Load the agent prompt**: Use `.claude/agents/chapter-enhancer.md`
2. **Provide input files**: metadata.json, chapter_XX.json, and images
3. **Run enhancement**: Agent will process and return enhanced chapter with mappings
4. **Validate output**: Check quality metrics and preservation rules
5. **Review mappings**: Ensure traceability between original and enhanced content

## Important Notes

- **Voice is paramount**: Every reduction must preserve Swink's distinctive style
- **Pedagogy over brevity**: Never sacrifice learning effectiveness for length
- **Clarity improvements**: Reductions should enhance, not compromise, understanding
- **Respect expertise**: The author's technical accuracy must be maintained