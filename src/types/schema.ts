// AI Book Rewriting System - TypeScript Schema Definitions

export interface BookMetadata {
  id: string;
  title: string;
  author: string;
  isbn?: string;
  publicationYear?: number;
  genre: string;
  category: 'business' | 'academic' | 'biography' | 'science' | 'self-help' | 'technical' | 'other';
  language: string;
  pageCount?: number;
  wordCount: number;
  readingLevel: number; // Flesch-Kincaid grade level
  sourceFormat: 'pdf' | 'epub' | 'txt' | 'copypaste';
  processingDate: string;
  processingVersion: string;
  estimatedReadingTimeMinutes: number;
  tags: string[];
}

export interface VoiceAnalysis {
  averageSentenceLength: number;
  vocabularyComplexity: 'simple' | 'moderate' | 'complex';
  toneDescriptors: string[];
  rhetoricalDevices: string[];
  perspective: 'first-person' | 'third-person' | 'mixed';
  formalityLevel: number; // 1-10 scale
  technicalityLevel: number; // 1-10 scale
  personalityTraits: string[];
  styleFingerprint: string; // Compressed style description
}

export interface Paragraph {
  id: string;
  chapterId: string;
  sectionId?: string;
  orderIndex: number;
  content: string;
  wordCount: number;
  type: 'text' | 'quote' | 'list' | 'heading' | 'caption';
  importance: 'high' | 'medium' | 'low';
  concepts: string[]; // Key concepts discussed
  technicalTerms: string[];
  citations: Citation[];
}

export interface Citation {
  id: string;
  type: 'footnote' | 'endnote' | 'inline' | 'bibliography';
  content: string;
  pageNumber?: number;
  url?: string;
}

export interface Chapter {
  id: string;
  number: number;
  title: string;
  summary: string;
  keyPoints: string[];
  wordCount: number;
  sectionIds: string[];
  paragraphIds: string[];
  imageIds: string[];
  learningObjectives?: string[];
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

export interface Section {
  id: string;
  chapterId: string;
  title?: string;
  orderIndex: number;
  paragraphIds: string[];
  type: 'introduction' | 'main-content' | 'conclusion' | 'example' | 'case-study';
}

export interface ImageData {
  id: string;
  chapterId: string;
  paragraphId?: string; // If associated with specific paragraph
  type: 'chart' | 'diagram' | 'photo' | 'illustration' | 'graph' | 'table';
  fileName: string;
  fileSize: number;
  width: number;
  height: number;
  caption?: string;
  altText: string;
  description: string;
  relevanceScore: number; // 1-10, how relevant to surrounding content
  preservationNotes: string;
  improvementSuggestions: string[];
}

export interface ParagraphMapping {
  id: string;
  originalParagraphIds: string[];
  rewrittenParagraphId: string;
  mappingType: '1:1' | 'N:1' | '1:N' | 'contextual';
  improvementTypes: ImprovementType[];
  confidenceScore: number; // 0-100
  qualityMetrics: QualityMetrics;
  reviewNotes?: string;
  humanReviewRequired: boolean;
  contextualSources?: string[]; // Additional paragraph IDs that influenced rewrite
  refinementHistory?: RefinementEntry[]; // Track post-mapping refinements
}

export interface RefinementEntry {
  timestamp: string;
  refinementType: 'information-recovery' | 'voice-realignment' | 'cross-reference-repair' | 'terminology-harmonization' | 'context-enrichment';
  reason: string;
  beforeMetrics: Partial<QualityMetrics>;
  afterMetrics: Partial<QualityMetrics>;
  changeDescription: string;
  confidenceImprovement: number;
}

export type ImprovementType = 
  | 'clarity'
  | 'condensation'
  | 'expansion'
  | 'flow'
  | 'accuracy'
  | 'terminology'
  | 'examples'
  | 'transitions'
  | 'structure';

export interface QualityMetrics {
  voicePreservationScore: number; // 0-100
  clarityImprovementScore: number; // 0-100
  factualAccuracyScore: number; // 0-100
  readabilityImprovement: number; // Change in Flesch-Kincaid score
  lengthChangePercentage: number; // Positive for expansion, negative for condensation
  technicalAccuracyScore: number; // 0-100
}

export interface BookContent {
  metadata: BookMetadata;
  voiceAnalysis: VoiceAnalysis;
  chapters: Chapter[];
  sections: Section[];
  paragraphs: Paragraph[];
  images: ImageData[];
  tableOfContents: TableOfContentsEntry[];
  citations: Citation[];
  glossary?: GlossaryEntry[];
}

export interface TableOfContentsEntry {
  id: string;
  title: string;
  level: number; // 1 for chapter, 2 for section, etc.
  pageNumber?: number;
  chapterId?: string;
  sectionId?: string;
  children: TableOfContentsEntry[];
}

export interface GlossaryEntry {
  term: string;
  definition: string;
  firstAppearanceChapterId: string;
  firstAppearanceParagraphId: string;
  complexity: 'basic' | 'intermediate' | 'advanced';
}

export interface ProcessedBook {
  id: string;
  metadata: BookMetadata;
  originalVersion: BookContent;
  rewrittenVersion: BookContent;
  mappings: ParagraphMapping[];
  processingReport: ProcessingReport;
  qualityReport: QualityReport;
  createdAt: string;
  updatedAt: string;
  version: string;
}

export interface ProcessingReport {
  totalProcessingTimeMs: number;
  phaseDurations: {
    ingestion: number;
    analysis: number;
    planning: number;
    rewriting: number;
    refinement: number; // Post-mapping selective improvements
    qualityAssurance: number;
  };
  statisticsOriginal: ContentStatistics;
  statisticsRewritten: ContentStatistics;
  statisticsPostRefinement?: ContentStatistics; // Optional: only if refinements were made
  improvementsSummary: ImprovementsSummary;
  refinementSummary?: RefinementSummary; // Track refinement phase results
  errorLog: ProcessingError[];
  warningLog: ProcessingWarning[];
}

export interface RefinementSummary {
  paragraphsAnalyzed: number;
  paragraphsRefined: number;
  informationRecovered: number;
  voiceRealignments: number;
  crossReferencesRepaired: number;
  terminologyHarmonized: number;
  averageConfidenceImprovement: number;
  refinementDecisions: string[]; // Log of why certain paragraphs were or weren't refined
}

export interface ContentStatistics {
  wordCount: number;
  paragraphCount: number;
  sentenceCount: number;
  averageWordsPerSentence: number;
  averageWordsPerParagraph: number;
  readabilityScore: number;
  complexityScore: number;
  technicalTermCount: number;
}

export interface ImprovementsSummary {
  clarityImprovements: number;
  condensationCount: number;
  expansionCount: number;
  flowImprovements: number;
  terminologyDefinitions: number;
  exampleAdditions: number;
  overallQualityScore: number; // 0-100
  postMappingRefinements?: number; // Count of paragraphs refined after initial mapping
}

export interface ProcessingError {
  phase: string;
  errorCode: string;
  message: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  timestamp: string;
  affectedParagraphIds: string[];
  resolution?: string;
}

export interface ProcessingWarning {
  phase: string;
  warningCode: string;
  message: string;
  timestamp: string;
  affectedParagraphIds: string[];
  recommendation: string;
}

export interface QualityReport {
  overallScore: number; // 0-100
  voicePreservation: {
    score: number;
    analysis: string;
    riskAreas: string[];
  };
  contentIntegrity: {
    score: number;
    factualAccuracy: number;
    informationLoss: number;
    citationPreservation: number;
  };
  improvementEffectiveness: {
    clarityGain: number;
    readabilityImprovement: number;
    lengthOptimization: number;
    flowEnhancement: number;
  };
  mappingQuality: {
    accuracy: number;
    completeness: number;
    userExperienceScore: number;
  };
  humanReviewRecommendations: string[];
  confidenceInterval: [number, number]; // Lower and upper bounds
}

// User reading progress and preferences
export interface ReadingProgress {
  bookId: string;
  userId: string;
  currentChapterId: string;
  currentParagraphId: string;
  scrollPosition: number; // Pixel position within the content
  percentComplete: number; // 0-100
  readingTimeSpentMs: number;
  lastReadAt: string;
  bookmarks: Bookmark[];
  notes: Note[];
  preferences: ReadingPreferences;
}

export interface Bookmark {
  id: string;
  paragraphId: string;
  title: string;
  note?: string;
  createdAt: string;
  color: string;
}

export interface Note {
  id: string;
  paragraphId: string;
  content: string;
  isPrivate: boolean;
  createdAt: string;
  updatedAt: string;
  tags: string[];
}

export interface ReadingPreferences {
  fontSize: 'small' | 'medium' | 'large' | 'extra-large';
  lineHeight: 'compact' | 'normal' | 'relaxed';
  fontFamily: 'system' | 'serif' | 'sans-serif' | 'monospace';
  theme: 'light' | 'dark' | 'sepia' | 'high-contrast';
  showOriginalIndicators: boolean;
  doubleTapSensitivity: 'low' | 'medium' | 'high';
  animationsEnabled: boolean;
  readingSpeedWpm: number;
}

// Library management
export interface BookLibrary {
  userId: string;
  books: LibraryBook[];
  collections: Collection[];
  readingStats: ReadingStats;
  lastUpdated: string;
}

export interface LibraryBook {
  bookId: string;
  addedAt: string;
  status: 'unread' | 'reading' | 'completed' | 'paused';
  rating?: number; // 1-5 stars
  review?: string;
  tags: string[];
  collectionIds: string[];
  downloadedAt?: string;
  fileSize: number;
}

export interface Collection {
  id: string;
  name: string;
  description: string;
  color: string;
  bookIds: string[];
  createdAt: string;
  isPublic: boolean;
}

export interface ReadingStats {
  totalBooksRead: number;
  totalReadingTimeMs: number;
  averageReadingSpeedWpm: number;
  favoriteGenres: string[];
  readingStreak: number; // Days
  monthlyGoal?: number;
  yearlyGoal?: number;
  achievements: Achievement[];
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  unlockedAt: string;
  iconName: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'legendary';
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message: string;
  timestamp: string;
  version: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    hasNext: boolean;
    hasPrevious: boolean;
  };
}

// Search and filtering
export interface SearchFilters {
  query?: string;
  genres?: string[];
  authors?: string[];
  categories?: string[];
  readingStatus?: ('unread' | 'reading' | 'completed' | 'paused')[];
  rating?: [number, number]; // Min and max rating
  dateRange?: [string, string]; // ISO date strings
  tags?: string[];
  sortBy?: 'title' | 'author' | 'addedDate' | 'rating' | 'readingProgress';
  sortOrder?: 'asc' | 'desc';
}

// Export utilities
export interface ExportOptions {
  format: 'json' | 'epub' | 'pdf' | 'txt' | 'markdown';
  includeOriginal: boolean;
  includeRewritten: boolean;
  includeMappings: boolean;
  includeNotes: boolean;
  includeProgress: boolean;
  chapterRange?: [number, number];
}

// Validation schemas (for use with libraries like Zod)
export const BookMetadataSchema = {
  id: 'string',
  title: 'string',
  author: 'string',
  category: 'enum',
  language: 'string',
  wordCount: 'number',
  sourceFormat: 'enum',
  processingDate: 'string',
  // ... additional validation rules
};

// Type guards
export function isProcessedBook(obj: any): obj is ProcessedBook {
  return obj && 
    typeof obj.id === 'string' &&
    obj.metadata &&
    obj.originalVersion &&
    obj.rewrittenVersion &&
    Array.isArray(obj.mappings);
}

export function isParagraphMapping(obj: any): obj is ParagraphMapping {
  return obj &&
    typeof obj.id === 'string' &&
    Array.isArray(obj.originalParagraphIds) &&
    typeof obj.rewrittenParagraphId === 'string' &&
    typeof obj.confidenceScore === 'number';
}

// Constants
export const SUPPORTED_FORMATS = ['pdf', 'epub', 'txt', 'copypaste'] as const;
export const BOOK_CATEGORIES = ['business', 'academic', 'biography', 'science', 'self-help', 'technical', 'other'] as const;
export const IMPROVEMENT_TYPES = ['clarity', 'condensation', 'expansion', 'flow', 'accuracy', 'terminology', 'examples', 'transitions', 'structure'] as const;
export const MAPPING_TYPES = ['1:1', 'N:1', '1:N', 'contextual'] as const;

// Utility types
export type BookId = string;
export type ParagraphId = string;
export type ChapterId = string;
export type UserId = string;

// Database table interfaces (for IndexedDB/local storage)
export interface BookStore {
  keyPath: 'id';
  data: ProcessedBook;
  indexes: {
    byAuthor: 'metadata.author';
    byCategory: 'metadata.category';
    byTitle: 'metadata.title';
    byProcessingDate: 'metadata.processingDate';
  };
}

export interface ProgressStore {
  keyPath: 'bookId';
  data: ReadingProgress;
  indexes: {
    byUserId: 'userId';
    byLastRead: 'lastReadAt';
    byPercentComplete: 'percentComplete';
  };
}

export interface LibraryStore {
  keyPath: 'userId';
  data: BookLibrary;
  indexes: {
    byLastUpdated: 'lastUpdated';
  };
}