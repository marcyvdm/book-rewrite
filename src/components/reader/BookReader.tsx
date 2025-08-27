import React, { useEffect, useRef, useState } from 'react';
import { useBookStore } from '../../stores/bookStore';
import { ParagraphRenderer } from './ParagraphRenderer';
import { ReaderHeader } from './ReaderHeader';
import { ProgressBar } from './ProgressBar';
import { OriginalOverlay } from './OriginalOverlay';

interface BookReaderProps {
  bookId: string;
}

export default function BookReader({ bookId }: BookReaderProps) {
  const {
    currentBook,
    currentProgress,
    isLoading,
    error,
    loadBook,
    setScrollPosition,
    setCurrentParagraph,
    showOriginal,
    selectedParagraphId,
  } = useBookStore();

  const scrollRef = useRef<HTMLDivElement>(null);
  const [isScrolling, setIsScrolling] = useState(false);

  useEffect(() => {
    if (bookId) {
      loadBook(bookId);
    }
  }, [bookId, loadBook]);

  useEffect(() => {
    // Restore scroll position when book loads
    if (currentProgress && scrollRef.current) {
      scrollRef.current.scrollTop = currentProgress.scrollPosition;
    }
  }, [currentBook, currentProgress]);

  useEffect(() => {
    const scrollContainer = scrollRef.current;
    if (!scrollContainer) return;

    let scrollTimeout: NodeJS.Timeout;

    const handleScroll = () => {
      setIsScrolling(true);
      
      // Clear existing timeout
      clearTimeout(scrollTimeout);
      
      // Update scroll position in store
      setScrollPosition(scrollContainer.scrollTop);
      
      // Set scrolling to false after scroll ends
      scrollTimeout = setTimeout(() => {
        setIsScrolling(false);
      }, 150);

      // Update current paragraph based on scroll position
      updateCurrentParagraphFromScroll();
    };

    const updateCurrentParagraphFromScroll = () => {
      if (!currentBook) return;

      const paragraphElements = scrollContainer.querySelectorAll('[data-paragraph-id]');
      const containerTop = scrollContainer.scrollTop;
      const containerHeight = scrollContainer.clientHeight;
      const centerPoint = containerTop + (containerHeight / 2);

      let closestParagraph = '';
      let closestDistance = Infinity;

      paragraphElements.forEach((element) => {
        const rect = element.getBoundingClientRect();
        const elementTop = rect.top + containerTop;
        const elementCenter = elementTop + (rect.height / 2);
        const distance = Math.abs(elementCenter - centerPoint);

        if (distance < closestDistance) {
          closestDistance = distance;
          closestParagraph = element.getAttribute('data-paragraph-id') || '';
        }
      });

      if (closestParagraph && closestParagraph !== currentProgress?.currentParagraphId) {
        setCurrentParagraph(closestParagraph);
      }
    };

    scrollContainer.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      scrollContainer.removeEventListener('scroll', handleScroll);
      clearTimeout(scrollTimeout);
    };
  }, [currentBook, currentProgress, setScrollPosition, setCurrentParagraph]);

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="animate-pulse-slow">
          <div className="text-reading-text-muted dark:text-reading-text-muted-dark text-lg">
            Loading book...
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-screen flex items-center justify-center p-6">
        <div className="text-center">
          <div className="text-red-500 text-lg font-medium mb-2">Error</div>
          <div className="text-reading-text-muted dark:text-reading-text-muted-dark">
            {error}
          </div>
        </div>
      </div>
    );
  }

  if (!currentBook) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="text-reading-text-muted dark:text-reading-text-muted-dark">
          Book not found
        </div>
      </div>
    );
  }

  const currentVersion = currentBook.rewrittenVersion;
  
  return (
    <div className="h-screen flex flex-col bg-reading-bg dark:bg-reading-bg-dark">
      {/* Header */}
      <ReaderHeader 
        book={currentBook}
        isScrolling={isScrolling}
      />
      
      {/* Progress Bar */}
      <ProgressBar 
        progress={currentProgress?.percentComplete || 0}
        isVisible={!isScrolling}
      />

      {/* Main Reading Area */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-4 md:px-6 lg:px-8"
        style={{ 
          scrollBehavior: 'smooth',
          WebkitOverflowScrolling: 'touch'
        }}
      >
        <div className="max-w-reading mx-auto py-6 md:py-8 lg:py-12">
          {/* Book Title and Author */}
          <div className="mb-8 md:mb-12 text-center">
            <h1 className="text-2xl md:text-3xl font-bold text-reading-text dark:text-reading-text-dark mb-2">
              {currentBook.metadata.title}
            </h1>
            <p className="text-lg text-reading-text-muted dark:text-reading-text-muted-dark">
              by {currentBook.metadata.author}
            </p>
          </div>

          {/* Chapters */}
          {currentVersion.chapters.map((chapter) => (
            <div key={chapter.id} className="mb-8 md:mb-12">
              <h2 className="text-xl md:text-2xl font-semibold text-reading-text dark:text-reading-text-dark mb-4 md:mb-6">
                {chapter.title}
              </h2>
              
              {/* Chapter Paragraphs */}
              <div className="space-y-4 md:space-y-6">
                {chapter.paragraphIds
                  .map(paragraphId => currentVersion.paragraphs.find(p => p.id === paragraphId))
                  .filter(Boolean)
                  .map((paragraph) => (
                    <ParagraphRenderer
                      key={paragraph!.id}
                      paragraph={paragraph!}
                      mapping={currentBook.mappings.find(m => m.rewrittenParagraphId === paragraph!.id)}
                      originalParagraphs={currentBook.originalVersion.paragraphs}
                      isSelected={selectedParagraphId === paragraph!.id}
                      showOriginal={showOriginal}
                    />
                  ))}
              </div>
            </div>
          ))}

          {/* Bottom padding for reading comfort */}
          <div className="h-32"></div>
        </div>
      </div>

      {/* Original Text Overlay */}
      {showOriginal && selectedParagraphId && (
        <OriginalOverlay
          paragraphId={selectedParagraphId}
          mapping={currentBook.mappings.find(m => m.rewrittenParagraphId === selectedParagraphId)}
          originalParagraphs={currentBook.originalVersion.paragraphs}
          onClose={() => useBookStore.getState().clearSelectedParagraph()}
        />
      )}
    </div>
  );
}