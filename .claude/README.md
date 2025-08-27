# Claude Code Agents & Workflows

This `.claude` folder contains specialized subagents and workflows for our advanced AI book processing system.

## 📁 Structure

```
.claude/
├── agents/           # Specialized subagents
├── commands/         # Custom slash commands  
├── settings.json     # Project permissions
└── README.md         # This file
```

## 🤖 Specialized Agents

### Core Processing Agents

**`voice-analyzer`** - Author Style Analysis
- Analyzes writing patterns and creates voice fingerprints
- Ensures AI enhancement preserves author authenticity
- Generates preservation guidelines for other agents

**`chapter-processor`** - Parallel Chapter Analysis  
- Processes individual chapters with structural analysis
- Identifies improvement opportunities and content patterns
- Enables parallel processing for faster book conversion

**`paragraph-rewriter`** - Content Enhancement
- Enhances individual paragraphs while preserving voice
- Applies context-aware improvements (clarity, flow, structure)
- Tracks quality metrics and confidence scores

**`mapping-validator`** - Quality Assurance
- Validates all original↔enhanced paragraph mappings
- Ensures accurate traceability for double-tap functionality
- Comprehensive quality control and error detection

**`refinement-analyzer`** - Phase 5 Selective Refinement
- Analyzes completed mappings for systematic improvement opportunities
- Implements selective refinement based on data-driven criteria
- Focuses on high-impact improvements with surgical precision

## ⚡ Custom Commands

### `/process-book <pdf-path>`
Complete book processing workflow:
```bash
/process-book "to-be-processed/game-feel.pdf" --max-pages 50
```

### `/analyze-voice <content-path>`  
Deep author voice analysis:
```bash
/analyze-voice "extracted-content/book-extracted.json"
```

### `/validate-mappings <processed-book-path>`
Quality assurance validation:
```bash
/validate-mappings "processed-books/book-processed.json"
```

### `/refine-selective <processed-book-path>`
Phase 5 selective refinement:
```bash
/refine-selective "processed-books/book-processed.json"
```

## 🔧 Agent Coordination

### Parallel Processing Flow
1. **PDF Extraction** → Extract content with Python script
2. **Voice Analysis** → `voice-analyzer` creates style fingerprint  
3. **Chapter Processing** → Multiple `chapter-processor` agents in parallel
4. **Paragraph Enhancement** → `paragraph-rewriter` with voice guidelines
5. **Quality Validation** → `mapping-validator` ensures accuracy
6. **Selective Refinement** → `refinement-analyzer` for final improvements

### Context Sharing Strategy
- **Voice Guidelines**: Shared from analyzer to all rewriting agents
- **Chapter Context**: Cross-chapter dependencies tracked
- **Quality Standards**: Consistent metrics across all agents
- **Mapping Integrity**: Validated end-to-end traceability

## 🎯 Design Principles

### Specialized Expertise
Each agent has a focused purpose with deep domain knowledge:
- Voice analysis requires literary sensitivity
- Chapter processing needs structural understanding  
- Paragraph rewriting demands linguistic precision
- Validation requires systematic quality assessment

### Quality-First Approach
- Multiple validation layers prevent errors
- Confidence scoring enables quality measurement
- Human review triggers for low-confidence results
- Complete audit trails for transparency

### Scalable Architecture  
- Parallel processing reduces conversion time
- Modular agents enable easy workflow customization
- Reusable components across different book types
- Clear interfaces between agent responsibilities

## 🚀 Usage Examples

### Processing a Technical Book
```bash
# Full pipeline for technical book
/process-book "to-be-processed/technical-manual.pdf"

# Validate quality 
/validate-mappings "processed-books/technical-manual-processed.json"

# Apply selective refinements
/refine-selective "processed-books/technical-manual-processed.json"
```

### Quick Voice Analysis
```bash
# Just analyze writing style
/analyze-voice "extracted-content/author-sample.json"
```

## 📊 Quality Metrics

Each agent tracks specific metrics:
- **Voice Preservation**: >85% similarity to original style
- **Technical Accuracy**: 100% factual content preservation
- **Clarity Improvement**: Measured readability gains
- **Mapping Accuracy**: >95% correct traceability
- **Confidence Scores**: 0-100 enhancement quality rating

## 🔒 Security & Permissions

The `settings.json` file restricts access to:
- Environment files and secrets
- Node modules and build artifacts  
- Git history and logs
- Source PDFs and processing artifacts

This ensures agents focus on book content while protecting sensitive information.

---

**Result**: A sophisticated multi-agent system that can process books with the quality of human editors while maintaining complete transparency and traceability.