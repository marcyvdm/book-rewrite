import { create } from 'zustand';
import { persist, subscribeWithSelector } from 'zustand/middleware';
import type { ProcessedBook, ReadingProgress, ReadingPreferences } from '../types/schema';
import { db } from '../utils/database';

interface BookStoreState {
  // Current reading state
  currentBook: ProcessedBook | null;
  currentProgress: ReadingProgress | null;
  isLoading: boolean;
  error: string | null;
  
  // Reading preferences
  preferences: ReadingPreferences;
  
  // Library state
  allBooks: ProcessedBook[];
  recentBooks: ProcessedBook[];
  
  // Reading interface state
  showOriginal: boolean;
  selectedParagraphId: string | null;
  fontSize: ReadingPreferences['fontSize'];
  theme: ReadingPreferences['theme'];
}

interface BookStoreActions {
  // Book management
  loadBook: (bookId: string) => Promise<void>;
  loadAllBooks: () => Promise<void>;
  addBook: (book: ProcessedBook) => Promise<void>;
  removeBook: (bookId: string) => Promise<void>;
  
  // Reading progress
  updateProgress: (bookId: string, progress: Partial<ReadingProgress>) => Promise<void>;
  setScrollPosition: (position: number) => void;
  setCurrentParagraph: (paragraphId: string) => void;
  
  // Reading interface
  toggleOriginal: (paragraphId?: string) => void;
  setTheme: (theme: ReadingPreferences['theme']) => void;
  setFontSize: (fontSize: ReadingPreferences['fontSize']) => void;
  updatePreferences: (preferences: Partial<ReadingPreferences>) => void;
  
  // UI state
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearSelectedParagraph: () => void;
}

type BookStore = BookStoreState & BookStoreActions;

const defaultPreferences: ReadingPreferences = {
  fontSize: 'medium',
  lineHeight: 'normal',
  fontFamily: 'system',
  theme: 'light',
  showOriginalIndicators: true,
  doubleTapSensitivity: 'medium',
  animationsEnabled: true,
  readingSpeedWpm: 250,
};

export const useBookStore = create<BookStore>()(
  subscribeWithSelector(
    persist(
      (set, get) => ({
        // Initial state
        currentBook: null,
        currentProgress: null,
        isLoading: false,
        error: null,
        preferences: defaultPreferences,
        allBooks: [],
        recentBooks: [],
        showOriginal: false,
        selectedParagraphId: null,
        fontSize: defaultPreferences.fontSize,
        theme: defaultPreferences.theme,

        // Actions
        loadBook: async (bookId: string) => {
          set({ isLoading: true, error: null });
          
          try {
            const book = await db.getBook(bookId);
            if (!book) {
              throw new Error(`Book with ID ${bookId} not found`);
            }
            
            const progress = await db.getReadingProgress(bookId) || {
              bookId,
              userId: 'default',
              currentChapterId: book.rewrittenVersion.chapters[0]?.id || '',
              currentParagraphId: book.rewrittenVersion.paragraphs[0]?.id || '',
              scrollPosition: 0,
              percentComplete: 0,
              readingTimeSpentMs: 0,
              lastReadAt: new Date().toISOString(),
              bookmarks: [],
              notes: [],
              preferences: get().preferences,
            };
            
            set({ 
              currentBook: book, 
              currentProgress: progress,
              isLoading: false 
            });
            
            // Update recent books
            const { recentBooks } = get();
            const filteredRecent = recentBooks.filter(b => b.id !== bookId);
            set({ 
              recentBooks: [book, ...filteredRecent].slice(0, 10) 
            });
            
          } catch (error) {
            console.error('Error loading book:', error);
            set({ 
              error: error instanceof Error ? error.message : 'Failed to load book',
              isLoading: false 
            });
          }
        },

        loadAllBooks: async () => {
          set({ isLoading: true, error: null });
          
          try {
            const books = await db.getAllBooks();
            set({ allBooks: books, isLoading: false });
          } catch (error) {
            console.error('Error loading books:', error);
            set({ 
              error: 'Failed to load library',
              isLoading: false 
            });
          }
        },

        addBook: async (book: ProcessedBook) => {
          try {
            await db.addBook(book);
            const { allBooks } = get();
            set({ allBooks: [...allBooks, book] });
          } catch (error) {
            console.error('Error adding book:', error);
            set({ error: 'Failed to add book' });
          }
        },

        removeBook: async (bookId: string) => {
          try {
            await db.deleteBook(bookId);
            const { allBooks, recentBooks, currentBook } = get();
            
            set({
              allBooks: allBooks.filter(b => b.id !== bookId),
              recentBooks: recentBooks.filter(b => b.id !== bookId),
              ...(currentBook?.id === bookId ? { currentBook: null, currentProgress: null } : {})
            });
          } catch (error) {
            console.error('Error removing book:', error);
            set({ error: 'Failed to remove book' });
          }
        },

        updateProgress: async (bookId: string, progressUpdate: Partial<ReadingProgress>) => {
          const { currentProgress } = get();
          
          if (!currentProgress || currentProgress.bookId !== bookId) {
            return;
          }
          
          const updatedProgress: ReadingProgress = {
            ...currentProgress,
            ...progressUpdate,
            lastReadAt: new Date().toISOString(),
          };
          
          try {
            await db.updateReadingProgress(updatedProgress);
            set({ currentProgress: updatedProgress });
          } catch (error) {
            console.error('Error updating progress:', error);
          }
        },

        setScrollPosition: (position: number) => {
          const { currentBook, currentProgress } = get();
          if (currentBook && currentProgress) {
            const updatedProgress = {
              ...currentProgress,
              scrollPosition: position,
              lastReadAt: new Date().toISOString(),
            };
            
            set({ currentProgress: updatedProgress });
            
            // Debounced save to database
            clearTimeout((window as any).__scrollSaveTimeout);
            (window as any).__scrollSaveTimeout = setTimeout(() => {
              db.updateReadingProgress(updatedProgress);
            }, 1000);
          }
        },

        setCurrentParagraph: (paragraphId: string) => {
          const { currentBook, currentProgress } = get();
          if (!currentBook || !currentProgress) return;
          
          // Calculate progress percentage
          const allParagraphs = currentBook.rewrittenVersion.paragraphs;
          const currentIndex = allParagraphs.findIndex(p => p.id === paragraphId);
          const percentComplete = currentIndex >= 0 
            ? Math.round((currentIndex / allParagraphs.length) * 100) 
            : currentProgress.percentComplete;
          
          get().updateProgress(currentBook.id, {
            currentParagraphId: paragraphId,
            percentComplete,
          });
        },

        toggleOriginal: (paragraphId?: string) => {
          const { showOriginal, selectedParagraphId } = get();
          
          if (paragraphId) {
            if (selectedParagraphId === paragraphId && showOriginal) {
              // Hide original if same paragraph tapped again
              set({ showOriginal: false, selectedParagraphId: null });
            } else {
              // Show original for this paragraph
              set({ showOriginal: true, selectedParagraphId: paragraphId });
            }
          } else {
            // Toggle global original view
            set({ showOriginal: !showOriginal, selectedParagraphId: null });
          }
        },

        setTheme: (theme: ReadingPreferences['theme']) => {
          const { preferences } = get();
          const updatedPreferences = { ...preferences, theme };
          set({ preferences: updatedPreferences, theme });
        },

        setFontSize: (fontSize: ReadingPreferences['fontSize']) => {
          const { preferences } = get();
          const updatedPreferences = { ...preferences, fontSize };
          set({ preferences: updatedPreferences, fontSize });
        },

        updatePreferences: (newPreferences: Partial<ReadingPreferences>) => {
          const { preferences } = get();
          const updatedPreferences = { ...preferences, ...newPreferences };
          set({ preferences: updatedPreferences });
        },

        setLoading: (loading: boolean) => set({ isLoading: loading }),

        setError: (error: string | null) => set({ error }),

        clearSelectedParagraph: () => set({ 
          selectedParagraphId: null, 
          showOriginal: false 
        }),
      }),
      {
        name: 'book-reader-store',
        partialize: (state) => ({
          preferences: state.preferences,
          theme: state.theme,
          fontSize: state.fontSize,
          recentBooks: state.recentBooks,
        }),
      }
    )
  )
);

// Subscribe to theme changes to update document class
useBookStore.subscribe(
  (state) => state.theme,
  (theme) => {
    if (typeof document !== 'undefined') {
      document.documentElement.className = theme === 'dark' ? 'dark' : '';
    }
  }
);