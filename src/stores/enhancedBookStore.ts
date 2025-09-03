import { create } from 'zustand';
import { persist, subscribeWithSelector } from 'zustand/middleware';
import type { EnhancedChapter, OriginalChapterContent, BookData } from '../types/enhancedChapter';
import { chapterLoader } from '../utils/enhancedChapterLoader';

interface ReadingProgress {
  chapterId: string;
  currentParagraphId: string | null;
  scrollPosition: number;
  percentComplete: number;
  lastReadAt: string;
}

interface ReadingPreferences {
  fontSize: 'small' | 'medium' | 'large' | 'extra-large';
  theme: 'light' | 'dark' | 'sepia';
  showOriginalIndicators: boolean;
  doubleTapSensitivity: 'low' | 'medium' | 'high';
}

interface EnhancedBookState {
  // Current reading state
  bookData: BookData | null;
  currentChapterId: string | null;
  currentChapter: { enhanced: EnhancedChapter; original: OriginalChapterContent } | null;
  readingProgress: Record<string, ReadingProgress>;
  isLoading: boolean;
  error: string | null;

  // Reading preferences
  preferences: ReadingPreferences;

  // UI state
  showOriginal: boolean;
  selectedParagraphId: string | null;
  originalMappingVisible: boolean;
}

interface EnhancedBookActions {
  // Book loading
  loadBook: () => Promise<void>;
  loadChapter: (chapterId: string) => Promise<void>;
  
  // Reading progress
  setCurrentParagraph: (paragraphId: string) => void;
  setScrollPosition: (position: number) => void;
  updateProgress: (chapterId: string, progress: Partial<ReadingProgress>) => void;
  
  // UI actions
  toggleOriginalView: (paragraphId?: string) => void;
  setSelectedParagraph: (paragraphId: string | null) => void;
  showOriginalMapping: (paragraphId: string) => void;
  hideOriginalMapping: () => void;
  
  // Preferences
  setTheme: (theme: ReadingPreferences['theme']) => void;
  setFontSize: (fontSize: ReadingPreferences['fontSize']) => void;
  updatePreferences: (prefs: Partial<ReadingPreferences>) => void;
  
  // Utility
  getOriginalParagraphs: (enhancedParagraphId: string) => string[];
  getMappingInfo: (enhancedParagraphId: string) => { type: string; originalIds: string[]; notes?: string } | null;
  getChapterProgress: (chapterId: string) => { currentIndex: number; totalParagraphs: number; percentComplete: number } | null;
}

type EnhancedBookStore = EnhancedBookState & EnhancedBookActions;

const defaultPreferences: ReadingPreferences = {
  fontSize: 'medium',
  theme: 'light',
  showOriginalIndicators: true,
  doubleTapSensitivity: 'medium',
};

export const useEnhancedBookStore = create<EnhancedBookStore>()(
  subscribeWithSelector(
    persist(
      (set, get) => ({
        // Initial state
        bookData: null,
        currentChapterId: null,
        currentChapter: null,
        readingProgress: {},
        isLoading: false,
        error: null,
        preferences: defaultPreferences,
        showOriginal: false,
        selectedParagraphId: null,
        originalMappingVisible: false,

        // Actions
        loadBook: async () => {
          set({ isLoading: true, error: null });
          
          try {
            const bookData = await chapterLoader.loadGameFeelBook();
            
            // Auto-load first chapter
            const chapterIds = Object.keys(bookData.chapters);
            const firstChapterId = chapterIds[0];
            let firstChapter = null;
            
            if (firstChapterId) {
              firstChapter = await chapterLoader.getChapter(firstChapterId);
            }
            
            set({
              bookData,
              currentChapterId: firstChapterId,
              currentChapter: firstChapter,
              isLoading: false
            });

            console.log('✅ Book loaded successfully');
          } catch (error) {
            console.error('❌ Error loading book:', error);
            set({
              error: error instanceof Error ? error.message : 'Failed to load book',
              isLoading: false
            });
          }
        },

        loadChapter: async (chapterId: string) => {
          const { bookData } = get();
          if (!bookData) {
            await get().loadBook();
          }

          try {
            const chapter = await chapterLoader.getChapter(chapterId);
            if (!chapter) {
              throw new Error(`Chapter ${chapterId} not found`);
            }

            set({
              currentChapterId: chapterId,
              currentChapter: chapter,
              selectedParagraphId: null,
              showOriginal: false,
              originalMappingVisible: false
            });

          } catch (error) {
            console.error(`❌ Error loading chapter ${chapterId}:`, error);
            set({
              error: error instanceof Error ? error.message : 'Failed to load chapter'
            });
          }
        },

        setCurrentParagraph: (paragraphId: string) => {
          const { currentChapterId } = get();
          if (!currentChapterId) return;

          // Calculate progress
          const progress = chapterLoader.calculateChapterProgress(currentChapterId, paragraphId);
          
          if (progress) {
            get().updateProgress(currentChapterId, {
              currentParagraphId: paragraphId,
              percentComplete: progress.percentComplete
            });
          }
        },

        setScrollPosition: (position: number) => {
          const { currentChapterId } = get();
          if (!currentChapterId) return;

          get().updateProgress(currentChapterId, {
            scrollPosition: position
          });
        },

        updateProgress: (chapterId: string, progressUpdate: Partial<ReadingProgress>) => {
          const { readingProgress } = get();
          const currentProgress = readingProgress[chapterId] || {
            chapterId,
            currentParagraphId: null,
            scrollPosition: 0,
            percentComplete: 0,
            lastReadAt: new Date().toISOString()
          };

          const updatedProgress: ReadingProgress = {
            ...currentProgress,
            ...progressUpdate,
            lastReadAt: new Date().toISOString()
          };

          set({
            readingProgress: {
              ...readingProgress,
              [chapterId]: updatedProgress
            }
          });
        },

        toggleOriginalView: (paragraphId?: string) => {
          const { showOriginal, selectedParagraphId } = get();
          
          if (paragraphId) {
            if (selectedParagraphId === paragraphId && showOriginal) {
              // Hide if same paragraph tapped again
              set({ showOriginal: false, selectedParagraphId: null });
            } else {
              // Show original for this paragraph
              set({ showOriginal: true, selectedParagraphId: paragraphId });
            }
          } else {
            // Toggle global view
            set({ showOriginal: !showOriginal });
          }
        },

        setSelectedParagraph: (paragraphId: string | null) => {
          set({ selectedParagraphId: paragraphId });
        },

        showOriginalMapping: (paragraphId: string) => {
          set({
            selectedParagraphId: paragraphId,
            originalMappingVisible: true
          });
        },

        hideOriginalMapping: () => {
          set({
            originalMappingVisible: false,
            selectedParagraphId: null
          });
        },

        setTheme: (theme: ReadingPreferences['theme']) => {
          const { preferences } = get();
          set({
            preferences: { ...preferences, theme }
          });
        },

        setFontSize: (fontSize: ReadingPreferences['fontSize']) => {
          const { preferences } = get();
          set({
            preferences: { ...preferences, fontSize }
          });
        },

        updatePreferences: (prefs: Partial<ReadingPreferences>) => {
          const { preferences } = get();
          set({
            preferences: { ...preferences, ...prefs }
          });
        },

        getOriginalParagraphs: (enhancedParagraphId: string): string[] => {
          const { currentChapter } = get();
          if (!currentChapter) return [];

          const enhancedItem = currentChapter.enhanced.enhanced_content.find(
            item => item.paragraph_id === enhancedParagraphId
          );

          return enhancedItem?.original_mapping || [];
        },

        getMappingInfo: (enhancedParagraphId: string) => {
          const { currentChapter } = get();
          if (!currentChapter) return null;

          const enhancedItem = currentChapter.enhanced.enhanced_content.find(
            item => item.paragraph_id === enhancedParagraphId
          );

          if (!enhancedItem) return null;

          return {
            type: enhancedItem.reduction_type || 'one_to_one',
            originalIds: enhancedItem.original_mapping,
            notes: enhancedItem.preservation_notes
          };
        },

        getChapterProgress: (chapterId: string) => {
          const { readingProgress } = get();
          const progress = readingProgress[chapterId];
          
          if (!progress?.currentParagraphId) return null;
          
          return chapterLoader.calculateChapterProgress(chapterId, progress.currentParagraphId);
        }

      }),
      {
        name: 'enhanced-book-store',
        partialize: (state) => ({
          readingProgress: state.readingProgress,
          preferences: state.preferences,
          currentChapterId: state.currentChapterId
        })
      }
    )
  )
);

// Subscribe to theme changes
useEnhancedBookStore.subscribe(
  (state) => state.preferences.theme,
  (theme) => {
    if (typeof document !== 'undefined') {
      const root = document.documentElement;
      root.classList.remove('light', 'dark', 'sepia');
      root.classList.add(theme);
    }
  }
);