# Agent Output Contracts

## Voice Analyzer Output
**Location**: `processing/voice-analysis/voice-fingerprint.json`

**Required Structure**:
```json
{
  "agentType": "voice-analyzer",
  "authorId": "author-name-slug",
  "status": "completed",
  "timestamp": "2025-01-01T00:00:00Z",
  "voiceMetrics": {
    "averageSentenceLength": 18.3,
    "vocabularyComplexity": "complex",
    "formalityLevel": 7,
    "technicalityLevel": 8
  },
  "preservationRules": [
    "Maintain sentence length 15-22 words",
    "Keep technical terminology density high",
    "Preserve analytical tone with passion markers"
  ],
  "riskAreas": ["Oversimplification", "Lost metaphors"],
  "confidenceScore": 91
}
```

## Chapter Processor Output  
**Location**: `processing/chapter-analysis/ch{XX}-analysis.json`

**Required Structure**:
```json
{
  "agentType": "chapter-processor", 
  "chapterId": "ch-01",
  "status": "completed",
  "timestamp": "2025-01-01T00:00:00Z",
  "structure": {
    "sections": 3,
    "paragraphs": 15,
    "keyConceptCount": 8
  },
  "improvementAreas": [
    {"paragraphId": "p001", "issues": ["clarity", "flow"]},
    {"paragraphId": "p005", "issues": ["expansion"]}
  ],
  "crossReferences": ["ch-02", "ch-05"],
  "confidenceScore": 88
}
```

## Paragraph Rewriter Output
**Location**: `processing/paragraph-enhancement/enhanced-p{XXX}.json`

**Required Structure**:  
```json
{
  "agentType": "paragraph-rewriter",
  "originalId": "p001", 
  "status": "completed",
  "timestamp": "2025-01-01T00:00:00Z",
  "enhancedText": "Enhanced paragraph content...",
  "improvementTypes": ["clarity", "flow"],
  "qualityMetrics": {
    "voicePreservationScore": 89,
    "clarityImprovementScore": 85,
    "factualAccuracyScore": 100,
    "lengthChangePercentage": 15.3
  },
  "confidenceScore": 91
}
```

## Mapping Validator Output
**Location**: `processing/mappings/validation-report.json`

**Required Structure**:
```json
{
  "agentType": "mapping-validator",
  "status": "completed", 
  "timestamp": "2025-01-01T00:00:00Z",
  "overallAccuracy": 95,
  "validatedMappings": 156,
  "errors": [
    {"paragraphId": "p023", "severity": "high", "issue": "Missing mapping"}
  ],
  "recommendations": [
    "Fix orphaned paragraph p023",
    "Verify voice scores for p045-p050"
  ],
  "productionReady": false
}
```

## State Tracking Output
**Location**: `processing/state/progress.json`

**Required Structure**:
```json
{
  "bookId": "game-feel-processed",
  "currentPhase": "paragraph-enhancement",
  "overallProgress": 65,
  "agents": {
    "voice-analyzer": "completed",
    "chapter-processor": "completed", 
    "paragraph-rewriter": "in-progress",
    "mapping-validator": "pending"
  },
  "startTime": "2025-01-01T00:00:00Z",
  "lastUpdate": "2025-01-01T00:15:30Z"
}
```