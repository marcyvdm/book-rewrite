// Enhanced Chapter Types - matches our chapter enhancer output format

export interface EnhancedChapterMetadata {
  chapter_number: number;
  title: string;
  original_word_count: number;
  enhanced_word_count: number;
  reduction_percentage: number;
  preserved_elements: string[];
  voice_consistency_score: number;
}

export interface EnhancedContentItem {
  type: 'paragraph' | 'heading' | 'image' | 'footnote' | 'list';
  paragraph_id?: string;
  footnote_id?: string;
  text?: string;
  level?: number;
  src?: string;
  caption?: string;
  items?: string[];
  original_mapping: string[];
  reduction_type?: 'one_to_one' | 'many_to_one' | 'one_to_many' | 'one_to_none' | 'none_to_one';
  preservation_notes?: string;
}

export interface MappingTypeInfo {
  enhanced_id?: string;
  original_id?: string;
  original_ids?: string[];
  enhanced_ids?: string[];
  type?: string;
  reason?: string;
  justification?: string;
}

export interface MappingSummary {
  total_original_paragraphs: number;
  total_enhanced_paragraphs: number;
  mapping_types: {
    one_to_one: MappingTypeInfo[];
    many_to_one: MappingTypeInfo[];
    one_to_many: MappingTypeInfo[];
    one_to_none: MappingTypeInfo[];
    none_to_one: MappingTypeInfo[];
  };
  unchanged_paragraphs: string[];
}

export interface VoiceConsistency {
  signature_phrases_used: number;
  formality_appropriate: boolean;
  pronoun_usage_consistent: boolean;
  conversational_tone_maintained?: boolean;
  personal_anecdotes_preserved?: boolean;
}

export interface PedagogicalFlow {
  learning_objectives_met: boolean;
  examples_to_theory_ratio: number;
  breathing_spaces_included: boolean;
  revelation_beat_preserved?: boolean;
}

export interface TechnicalAccuracy {
  terminology_consistent: boolean;
  definitions_preserved: boolean;
  core_game_feel_definition_intact?: boolean;
  metrics_intact?: boolean;
}

export interface QualityChecks {
  core_concepts_preserved: boolean;
  voice_consistency: VoiceConsistency;
  pedagogical_flow: PedagogicalFlow;
  technical_accuracy: TechnicalAccuracy;
  critical_elements_status?: Record<string, string>;
}

export interface EnhancedChapter {
  chapter_metadata: EnhancedChapterMetadata;
  enhanced_content: EnhancedContentItem[];
  mapping_summary: MappingSummary;
  quality_checks: QualityChecks;
}

export interface OriginalChapterContent {
  chapter_title: string;
  content: Array<{
    type: string;
    text?: string;
    level?: number;
    src?: string;
    caption?: string;
    items?: string[];
  }>;
}

export interface BookData {
  metadata: {
    title: string;
    author: string;
    description: string;
  };
  chapters: {
    [key: string]: {
      enhanced: EnhancedChapter;
      original: OriginalChapterContent;
    };
  };
}