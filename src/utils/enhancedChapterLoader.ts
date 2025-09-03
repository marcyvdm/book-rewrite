import type { EnhancedChapter, OriginalChapterContent, BookData } from '../types/enhancedChapter';

/**
 * Load enhanced chapter data from JSON files
 */
export class EnhancedChapterLoader {
  private static instance: EnhancedChapterLoader;
  private bookData: BookData | null = null;

  static getInstance(): EnhancedChapterLoader {
    if (!EnhancedChapterLoader.instance) {
      EnhancedChapterLoader.instance = new EnhancedChapterLoader();
    }
    return EnhancedChapterLoader.instance;
  }

  async loadGameFeelBook(): Promise<BookData> {
    if (this.bookData) {
      return this.bookData;
    }

    try {
      console.log('🔄 Loading Game Feel enhanced chapters...');

      // Load enhanced chapters
      const [chapter1Enhanced, chapter4Enhanced] = await Promise.all([
        this.loadEnhancedChapter('/game-feel/chapter_01_enhanced.json'),
        this.loadEnhancedChapter('/enhanced_chapter_04.json')
      ]);

      // Load original chapters
      const [chapter1Original, chapter4Original] = await Promise.all([
        this.loadOriginalChapter('/game-feel/chapter_01.json'),
        this.loadOriginalChapter('/game-feel/chapter_04.json')
      ]);

      this.bookData = {
        metadata: {
          title: 'Game Feel: A Game Designer\'s Guide to Virtual Sensation',
          author: 'Steve Swink',
          description: 'Enhanced version with 30% length reduction while preserving the author\'s unique voice and pedagogical approach.'
        },
        chapters: {
          'chapter-01': {
            enhanced: chapter1Enhanced,
            original: chapter1Original
          },
          'chapter-04': {
            enhanced: chapter4Enhanced,
            original: chapter4Original
          }
        }
      };

      console.log('✅ Successfully loaded Game Feel book data');
      console.log(`📊 Chapters: ${Object.keys(this.bookData.chapters).length}`);
      console.log(`📝 Chapter 1: ${chapter1Enhanced.chapter_metadata.enhanced_word_count} words (${chapter1Enhanced.chapter_metadata.reduction_percentage}% reduction)`);
      console.log(`📝 Chapter 4: ${chapter4Enhanced.chapter_metadata.enhanced_word_count} words (${chapter4Enhanced.chapter_metadata.reduction_percentage}% reduction)`);

      return this.bookData;

    } catch (error) {
      console.error('❌ Error loading Game Feel book:', error);
      throw new Error(`Failed to load Game Feel book: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async getChapter(chapterId: string): Promise<{ enhanced: EnhancedChapter; original: OriginalChapterContent } | null> {
    const bookData = await this.loadGameFeelBook();
    return bookData.chapters[chapterId] || null;
  }

  async getAllChapterIds(): Promise<string[]> {
    const bookData = await this.loadGameFeelBook();
    return Object.keys(bookData.chapters);
  }

  getBookMetadata(): { title: string; author: string; description: string } | null {
    return this.bookData?.metadata || null;
  }

  private async loadEnhancedChapter(path: string): Promise<EnhancedChapter> {
    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      // Validate the structure
      if (!this.isValidEnhancedChapter(data)) {
        throw new Error('Invalid enhanced chapter structure');
      }

      return data;
    } catch (error) {
      throw new Error(`Failed to load enhanced chapter from ${path}: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  private async loadOriginalChapter(path: string): Promise<OriginalChapterContent> {
    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      // Validate the structure
      if (!this.isValidOriginalChapter(data)) {
        throw new Error('Invalid original chapter structure');
      }

      return data;
    } catch (error) {
      throw new Error(`Failed to load original chapter from ${path}: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  private isValidEnhancedChapter(data: any): data is EnhancedChapter {
    return (
      data &&
      data.chapter_metadata &&
      typeof data.chapter_metadata.chapter_number === 'number' &&
      typeof data.chapter_metadata.title === 'string' &&
      Array.isArray(data.enhanced_content) &&
      data.mapping_summary &&
      data.quality_checks
    );
  }

  private isValidOriginalChapter(data: any): data is OriginalChapterContent {
    return (
      data &&
      typeof data.chapter_title === 'string' &&
      Array.isArray(data.content)
    );
  }

  /**
   * Get reading progress information for a chapter
   */
  calculateChapterProgress(chapterId: string, currentParagraphId: string): {
    currentIndex: number;
    totalParagraphs: number;
    percentComplete: number;
  } | null {
    if (!this.bookData || !this.bookData.chapters[chapterId]) {
      return null;
    }

    const chapter = this.bookData.chapters[chapterId].enhanced;
    const paragraphs = chapter.enhanced_content.filter(item => item.type === 'paragraph');
    const currentIndex = paragraphs.findIndex(p => p.paragraph_id === currentParagraphId);
    
    if (currentIndex === -1) {
      return null;
    }

    return {
      currentIndex: currentIndex + 1,
      totalParagraphs: paragraphs.length,
      percentComplete: Math.round(((currentIndex + 1) / paragraphs.length) * 100)
    };
  }
}

// Export singleton instance
export const chapterLoader = EnhancedChapterLoader.getInstance();