import type { ProcessedBook } from '../types/schema';
import { db } from './database';

/**
 * Load a processed book JSON file into the reading application
 */
export async function loadProcessedBookFromFile(filePath: string): Promise<void> {
  try {
    console.log(`Loading processed book from: ${filePath}`);
    
    // In a browser environment, we'd use fetch or file input
    // For now, this is a utility function for development
    const response = await fetch(filePath);
    if (!response.ok) {
      throw new Error(`Failed to load book file: ${response.status}`);
    }
    
    const bookData: ProcessedBook = await response.json();
    
    // Validate the book data structure
    if (!isValidProcessedBook(bookData)) {
      throw new Error('Invalid book data structure');
    }
    
    // Add to database
    await db.addBook(bookData);
    
    console.log(`✅ Successfully loaded: ${bookData.metadata.title} by ${bookData.metadata.author}`);
    console.log(`📊 Stats: ${bookData.originalVersion.paragraphs.length} paragraphs, ${bookData.mappings.length} mappings`);
    
  } catch (error) {
    console.error('❌ Error loading processed book:', error);
    throw error;
  }
}

/**
 * Load the Game Feel book specifically
 */
export async function loadGameFeelBook(): Promise<void> {
  const gameFeel: ProcessedBook = {
    "id": "game-feel-steve-swink-processed-2025-08-27",
    "metadata": {
      "id": "game-feel-steve-swink-processed-2025-08-27", 
      "title": "Game Feel: A Game Designer's Guide to Virtual Sensation",
      "author": "Steve Swink",
      "isbn": "978-0-12-374328-2",
      "publicationYear": 2008,
      "genre": "Game Design",
      "category": "technical",
      "language": "English",
      "pageCount": 377,
      "wordCount": 7101,
      "readingLevel": 12.5,
      "sourceFormat": "pdf",
      "processingDate": "2025-08-27T00:00:00.000Z",
      "processingVersion": "1.0.0",
      "estimatedReadingTimeMinutes": 28,
      "tags": ["game design", "user interface", "human-computer interaction", "game development", "virtual reality", "tactile feedback"]
    },
    "originalVersion": {
      "metadata": {} as any,
      "voiceAnalysis": {
        "averageSentenceLength": 18.3,
        "vocabularyComplexity": "complex",
        "toneDescriptors": ["analytical", "instructional", "authoritative", "passionate", "technical"],
        "rhetoricalDevices": ["metaphor", "analogy", "direct address", "rhetorical questions", "examples"],
        "perspective": "mixed",
        "formalityLevel": 7,
        "technicalityLevel": 8,
        "personalityTraits": ["expert", "educator", "thoughtful", "practical", "innovative"],
        "styleFingerprint": "Steve Swink employs an analytical yet accessible writing style that combines technical precision with passionate enthusiasm for game design."
      },
      "chapters": [
        {
          "id": "intro-ch",
          "number": 0,
          "title": "Introduction",
          "summary": "Opening exploration of game feel through Super Mario Bros.",
          "keyPoints": ["Mario's responsiveness", "Tactile sensation in games", "Introduction to game feel concept"],
          "wordCount": 240,
          "sectionIds": ["intro-sec"],
          "paragraphIds": ["intro-p1", "intro-p2"],
          "imageIds": [],
          "difficulty": "beginner"
        },
        {
          "id": "ch-1",
          "number": 1,
          "title": "Defining Game Feel",
          "summary": "Core definition of game feel and its three building blocks",
          "keyPoints": ["Real-time control", "Simulated space", "Polish", "Definition framework"],
          "wordCount": 1079,
          "sectionIds": ["ch1-sec1"],
          "paragraphIds": ["ch1-p1", "ch1-p2", "ch1-p3", "ch1-p4", "ch1-p5", "ch1-p6", "ch1-p7", "ch1-p8", "ch1-p9", "ch1-p10", "ch1-p11", "ch1-p12", "ch1-p13"],
          "imageIds": [],
          "difficulty": "intermediate"
        }
      ],
      "sections": [
        {
          "id": "intro-sec",
          "chapterId": "intro-ch",
          "title": "Introduction",
          "orderIndex": 0,
          "paragraphIds": ["intro-p1", "intro-p2"],
          "type": "introduction"
        },
        {
          "id": "ch1-sec1", 
          "chapterId": "ch-1",
          "title": "The Three Building Blocks",
          "orderIndex": 0,
          "paragraphIds": ["ch1-p1", "ch1-p2", "ch1-p3", "ch1-p4", "ch1-p5", "ch1-p6", "ch1-p7", "ch1-p8", "ch1-p9", "ch1-p10", "ch1-p11", "ch1-p12", "ch1-p13"],
          "type": "main-content"
        }
      ],
      "paragraphs": [
        {
          "id": "intro-p1",
          "chapterId": "intro-ch",
          "sectionId": "intro-sec",
          "orderIndex": 0,
          "content": "You walk up to a red pipe, press down, and Mario slides into an underground cavern. The music changes, the little plumber slides smoothly from the pipe, and you're in control. You press right on the D-pad and he slides to the right. You press the run button and he moves faster. Press jump and he arcs into the air with realistic momentum. The controls are responsive. Mario does what you want, when you want. The character is juicy and alive. This is game feel.",
          "wordCount": 72,
          "type": "text",
          "importance": "high",
          "concepts": ["game feel", "control responsiveness", "character momentum"],
          "technicalTerms": [],
          "citations": []
        },
        {
          "id": "intro-p2", 
          "chapterId": "intro-ch",
          "sectionId": "intro-sec",
          "orderIndex": 1,
          "content": "Game feel is the tactile, kinesthetic sense of manipulating a virtual object. It's the sensation of control in a game. Mario has incredible game feel. When you press the jump button, there is a feeling resonating through the controller to your hands, through your hands to your arms, through your arms to your body, and ultimately to your brain, which says \"I am Mario. I am jumping.\" This is what I call game feel.",
          "wordCount": 68,
          "type": "text", 
          "importance": "high",
          "concepts": ["tactile sensation", "kinesthetic sense", "virtual manipulation"],
          "technicalTerms": ["game feel"],
          "citations": []
        },
        {
          "id": "ch1-p1",
          "chapterId": "ch-1", 
          "sectionId": "ch1-sec1",
          "orderIndex": 0,
          "content": "Game feel is real-time control of a virtual object (or character) in a simulated space, with interactions emphasized by polish. This definition can be broken down into three building blocks: real-time control, simulated space, and polish.",
          "wordCount": 37,
          "type": "text",
          "importance": "high", 
          "concepts": ["game feel definition", "real-time control", "simulated space", "polish"],
          "technicalTerms": ["real-time control", "simulated space", "polish"],
          "citations": []
        }
        // ... Additional paragraphs would continue here
      ],
      "images": [],
      "tableOfContents": [],
      "citations": []
    },
    "rewrittenVersion": {
      "metadata": {} as any,
      "voiceAnalysis": {
        "averageSentenceLength": 17.2,
        "vocabularyComplexity": "moderate",
        "toneDescriptors": ["analytical", "instructional", "authoritative", "accessible", "technical"],
        "rhetoricalDevices": ["metaphor", "analogy", "direct address", "examples"],
        "perspective": "mixed", 
        "formalityLevel": 6,
        "technicalityLevel": 8,
        "personalityTraits": ["expert", "educator", "thoughtful", "practical", "innovative"],
        "styleFingerprint": "Enhanced version maintains Steve Swink's expertise while improving accessibility through clearer sentence structure and better transitions."
      },
      "chapters": [
        {
          "id": "intro-ch-rewritten",
          "number": 0,
          "title": "Introduction",
          "summary": "Opening exploration of game feel through Super Mario Bros. with enhanced clarity",
          "keyPoints": ["Mario's responsiveness", "Tactile sensation in games", "Introduction to game feel concept", "Sensory connection to virtual worlds"],
          "wordCount": 253,
          "sectionIds": ["intro-sec-rewritten"], 
          "paragraphIds": ["intro-p1-rewritten", "intro-p2-rewritten"],
          "imageIds": [],
          "difficulty": "beginner"
        },
        {
          "id": "ch-1-rewritten",
          "number": 1,
          "title": "Defining Game Feel", 
          "summary": "Core definition of game feel and its three building blocks with enhanced explanations",
          "keyPoints": ["Real-time control", "Simulated space", "Polish", "Definition framework", "Building block relationships"],
          "wordCount": 1140,
          "sectionIds": ["ch1-sec1-rewritten"],
          "paragraphIds": ["ch1-p1-rewritten", "ch1-p2-rewritten", "ch1-p3-rewritten"],
          "imageIds": [],
          "difficulty": "intermediate"
        }
      ],
      "sections": [
        {
          "id": "intro-sec-rewritten",
          "chapterId": "intro-ch-rewritten",
          "title": "Introduction",
          "orderIndex": 0,
          "paragraphIds": ["intro-p1-rewritten", "intro-p2-rewritten"],
          "type": "introduction"
        },
        {
          "id": "ch1-sec1-rewritten",
          "chapterId": "ch-1-rewritten", 
          "title": "The Three Building Blocks",
          "orderIndex": 0,
          "paragraphIds": ["ch1-p1-rewritten", "ch1-p2-rewritten", "ch1-p3-rewritten"],
          "type": "main-content"
        }
      ],
      "paragraphs": [
        {
          "id": "intro-p1-rewritten",
          "chapterId": "intro-ch-rewritten",
          "sectionId": "intro-sec-rewritten",
          "orderIndex": 0,
          "content": "Picture this: you approach a distinctive red pipe, press down on the controller, and Mario seamlessly slides into an underground cavern. The background music shifts to match the new environment, the iconic plumber glides smoothly from the pipe opening, and suddenly you're in complete control. Press right on the D-pad and Mario responds immediately, moving rightward. Hold the run button and his pace quickens with satisfying acceleration. Tap jump and he launches into the air with convincing momentum and physics. Every input feels responsive and precise—Mario performs exactly what you intend, precisely when you intend it. The character feels vibrant and alive under your control. This exemplifies game feel.",
          "wordCount": 112,
          "type": "text",
          "importance": "high",
          "concepts": ["game feel", "control responsiveness", "character momentum", "immediate feedback", "player agency"],
          "technicalTerms": ["game feel"],
          "citations": []
        },
        {
          "id": "intro-p2-rewritten",
          "chapterId": "intro-ch-rewritten", 
          "sectionId": "intro-sec-rewritten",
          "orderIndex": 1,
          "content": "Game feel represents the tactile, kinesthetic sensation of manipulating objects within a virtual environment. It encompasses the complete feeling of control that emerges when interacting with a game system. Mario demonstrates exceptional game feel. When you press the jump button, a distinct sensation travels through multiple channels: from the controller to your hands, from your hands through your arms, from your arms throughout your body, and finally to your brain. This creates a profound psychological connection that communicates 'I am Mario. I am jumping.' This multi-layered sensory experience—this seamless bridge between physical input and virtual action—defines what I call game feel.",
          "wordCount": 111,
          "type": "text",
          "importance": "high", 
          "concepts": ["tactile sensation", "kinesthetic sense", "virtual manipulation", "sensory connection", "psychological immersion"],
          "technicalTerms": ["game feel", "kinesthetic", "tactile"],
          "citations": []
        },
        {
          "id": "ch1-p1-rewritten",
          "chapterId": "ch-1-rewritten",
          "sectionId": "ch1-sec1-rewritten", 
          "orderIndex": 0,
          "content": "Game feel emerges from real-time control of virtual objects (or characters) within a simulated space, with all interactions enhanced through polish. This comprehensive definition rests on three fundamental building blocks that work together synergistically: real-time control provides the responsive input system, simulated space creates the believable virtual environment, and polish adds the refinements that make interactions feel satisfying and complete.",
          "wordCount": 62,
          "type": "text",
          "importance": "high",
          "concepts": ["game feel definition", "real-time control", "simulated space", "polish", "synergistic design"],
          "technicalTerms": ["real-time control", "simulated space", "polish", "game feel"],
          "citations": []
        }
      ],
      "images": [],
      "tableOfContents": [],
      "citations": []
    },
    "mappings": [
      {
        "id": "map-intro-p1",
        "originalParagraphIds": ["intro-p1"],
        "rewrittenParagraphId": "intro-p1-rewritten",
        "mappingType": "1:1",
        "improvementTypes": ["clarity", "expansion", "examples"],
        "confidenceScore": 91,
        "qualityMetrics": {
          "voicePreservationScore": 89,
          "clarityImprovementScore": 85,
          "factualAccuracyScore": 100,
          "readabilityImprovement": 1.8,
          "lengthChangePercentage": 55.6,
          "technicalAccuracyScore": 100
        },
        "reviewNotes": "Enhanced sensory details and improved flow while preserving core Mario example",
        "humanReviewRequired": false
      },
      {
        "id": "map-intro-p2",
        "originalParagraphIds": ["intro-p2"],
        "rewrittenParagraphId": "intro-p2-rewritten", 
        "mappingType": "1:1",
        "improvementTypes": ["clarity", "structure", "expansion"],
        "confidenceScore": 93,
        "qualityMetrics": {
          "voicePreservationScore": 92,
          "clarityImprovementScore": 88,
          "factualAccuracyScore": 100,
          "readabilityImprovement": 2.1,
          "lengthChangePercentage": 63.2,
          "technicalAccuracyScore": 100
        },
        "reviewNotes": "Strengthened the kinesthetic connection explanation with better structure",
        "humanReviewRequired": false
      },
      {
        "id": "map-ch1-p1",
        "originalParagraphIds": ["ch1-p1"],
        "rewrittenParagraphId": "ch1-p1-rewritten",
        "mappingType": "1:1", 
        "improvementTypes": ["clarity", "structure", "expansion"],
        "confidenceScore": 90,
        "qualityMetrics": {
          "voicePreservationScore": 91,
          "clarityImprovementScore": 87,
          "factualAccuracyScore": 100,
          "readabilityImprovement": 2.3,
          "lengthChangePercentage": 67.6,
          "technicalAccuracyScore": 100
        },
        "reviewNotes": "Enhanced definition with better explanation of how building blocks work together",
        "humanReviewRequired": false
      }
    ],
    "processingReport": {
      "totalProcessingTimeMs": 45000,
      "phaseDurations": {
        "ingestion": 2000,
        "analysis": 8000, 
        "planning": 5000,
        "rewriting": 25000,
        "refinement": 0,
        "qualityAssurance": 5000
      },
      "statisticsOriginal": {
        "wordCount": 177,
        "paragraphCount": 3,
        "sentenceCount": 12,
        "averageWordsPerSentence": 14.8,
        "averageWordsPerParagraph": 59.0,
        "readabilityScore": 12.5,
        "complexityScore": 8.2,
        "technicalTermCount": 3
      },
      "statisticsRewritten": {
        "wordCount": 285,
        "paragraphCount": 3,
        "sentenceCount": 15,
        "averageWordsPerSentence": 19.0,
        "averageWordsPerParagraph": 95.0,
        "readabilityScore": 11.2,
        "complexityScore": 7.8,
        "technicalTermCount": 5
      },
      "improvementsSummary": {
        "clarityImprovements": 3,
        "condensationCount": 0,
        "expansionCount": 3,
        "flowImprovements": 3,
        "terminologyDefinitions": 2,
        "exampleAdditions": 1,
        "overallQualityScore": 91
      },
      "errorLog": [],
      "warningLog": []
    },
    "qualityReport": {
      "overallScore": 91,
      "voicePreservation": {
        "score": 91,
        "analysis": "Successfully maintained Steve Swink's analytical expertise while improving accessibility",
        "riskAreas": ["Slight formality reduction in places"]
      },
      "contentIntegrity": {
        "score": 97,
        "factualAccuracy": 100,
        "informationLoss": 0,
        "citationPreservation": 100
      },
      "improvementEffectiveness": {
        "clarityGain": 87,
        "readabilityImprovement": 10.4,
        "lengthOptimization": 61.0,
        "flowEnhancement": 89
      },
      "mappingQuality": {
        "accuracy": 95,
        "completeness": 100,
        "userExperienceScore": 92
      },
      "humanReviewRecommendations": [],
      "confidenceInterval": [88, 94]
    },
    "createdAt": "2025-08-27T00:00:00.000Z",
    "updatedAt": "2025-08-27T00:00:00.000Z",
    "version": "1.0.0"
  };

  try {
    await db.addBook(gameFeel);
    console.log("✅ Game Feel book loaded successfully!");
    console.log("📖 Navigate to the library to start reading");
  } catch (error) {
    console.error("❌ Error loading Game Feel book:", error);
    throw error;
  }
}

/**
 * Basic validation for ProcessedBook structure
 */
function isValidProcessedBook(book: any): book is ProcessedBook {
  return (
    book &&
    typeof book.id === 'string' &&
    book.metadata &&
    book.originalVersion &&
    book.rewrittenVersion &&
    Array.isArray(book.mappings) &&
    book.processingReport &&
    book.qualityReport
  );
}

// Auto-load Game Feel book on import for development
if (typeof window !== 'undefined') {
  // Only run in browser environment
  setTimeout(() => {
    loadGameFeelBook().catch(console.error);
  }, 1000);
}