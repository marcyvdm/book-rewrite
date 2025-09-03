import React, { useEffect, useRef, useState } from 'react';
import { useEnhancedBookStore } from '../../stores/enhancedBookStore';
import { EnhancedParagraphRenderer } from './EnhancedParagraphRenderer';
import { OriginalMappingOverlay } from './OriginalMappingOverlay';

interface EnhancedBookReaderProps {
  chapterId?: string;
}

export default function EnhancedBookReader({ chapterId }: EnhancedBookReaderProps) {
  const {
    bookData,
    currentChapter,
    currentChapterId,
    readingProgress,
    isLoading,
    error,
    preferences,
    selectedParagraphId,
    originalMappingVisible,
    loadBook,
    loadChapter,
    setCurrentParagraph,
    setScrollPosition,
    hideOriginalMapping,
    showOriginalMapping
  } = useEnhancedBookStore();

  const scrollRef = useRef<HTMLDivElement>(null);
  const [isScrolling, setIsScrolling] = useState(false);

  // Load book on mount
  useEffect(() => {
    if (!bookData) {
      loadBook();
    }
  }, [bookData, loadBook]);

  // Load specific chapter if provided
  useEffect(() => {
    if (chapterId && chapterId !== currentChapterId) {
      loadChapter(chapterId);
    }
  }, [chapterId, currentChapterId, loadChapter]);

  // Restore scroll position when chapter loads (only once per chapter load)
  useEffect(() => {
    if (currentChapter && currentChapterId && scrollRef.current) {
      const progress = readingProgress[currentChapterId];
      if (progress?.scrollPosition) {
        // Use requestAnimationFrame to ensure DOM is ready
        requestAnimationFrame(() => {
          if (scrollRef.current) {
            scrollRef.current.scrollTop = progress.scrollPosition;
          }
        });
      }
    }
  }, [currentChapter, currentChapterId]); // Removed readingProgress dependency

  // Handle scroll events for progress tracking
  useEffect(() => {
    const scrollContainer = scrollRef.current;
    if (!scrollContainer || !currentChapter) return;

    let scrollTimeout: NodeJS.Timeout;
    let saveTimeout: NodeJS.Timeout;

    const handleScroll = () => {
      setIsScrolling(true);
      clearTimeout(scrollTimeout);
      clearTimeout(saveTimeout);

      // Update current paragraph based on viewport (immediate)
      updateCurrentParagraphFromScroll();

      // Debounce scroll position saving (don't interfere with scrolling)
      saveTimeout = setTimeout(() => {
        setScrollPosition(scrollContainer.scrollTop);
      }, 1000);

      scrollTimeout = setTimeout(() => {
        setIsScrolling(false);
      }, 500); // Increased timeout to reduce flickering
    };

    const updateCurrentParagraphFromScroll = () => {
      const paragraphElements = scrollContainer.querySelectorAll('[data-paragraph-id]');
      const containerTop = scrollContainer.scrollTop;
      const containerHeight = scrollContainer.clientHeight;
      const viewportCenter = containerTop + (containerHeight / 2);

      let closestParagraph = '';
      let closestDistance = Infinity;

      paragraphElements.forEach((element) => {
        const rect = element.getBoundingClientRect();
        const elementTop = rect.top + containerTop;
        const elementCenter = elementTop + (rect.height / 2);
        const distance = Math.abs(elementCenter - viewportCenter);

        if (distance < closestDistance) {
          closestDistance = distance;
          closestParagraph = element.getAttribute('data-paragraph-id') || '';
        }
      });

      if (closestParagraph) {
        setCurrentParagraph(closestParagraph);
      }
    };

    scrollContainer.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      scrollContainer.removeEventListener('scroll', handleScroll);
      clearTimeout(scrollTimeout);
      clearTimeout(saveTimeout);
    };
  }, [currentChapter, setScrollPosition, setCurrentParagraph]);

  // Handle paragraph clicks
  const handleParagraphClick = (paragraphId: string, event: React.MouseEvent) => {
    // Double-tap/click detection for showing original
    const now = Date.now();
    const lastClickTime = (event.target as any).__lastClickTime || 0;
    const timeDiff = now - lastClickTime;
    (event.target as any).__lastClickTime = now;

    const sensitivity = preferences.doubleTapSensitivity;
    const threshold = sensitivity === 'low' ? 500 : sensitivity === 'high' ? 200 : 300;

    if (timeDiff < threshold) {
      // Double-tap detected - show original mapping
      showOriginalMapping(paragraphId);
    }
  };

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-pulse-slow text-xl text-gray-600 dark:text-gray-400 mb-2">
            Loading Game Feel...
          </div>
          <div className="text-sm text-gray-500 dark:text-gray-500">
            Enhanced chapters with mapping
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-screen flex items-center justify-center p-6">
        <div className="text-center max-w-md">
          <div className="text-red-500 text-lg font-medium mb-2">Error Loading Book</div>
          <div className="text-gray-600 dark:text-gray-400 mb-4">{error}</div>
          <button 
            onClick={loadBook}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!currentChapter || !bookData) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="text-gray-500 dark:text-gray-400">
          No chapter loaded
        </div>
      </div>
    );
  }

  const fontSizeClass = {
    small: 'text-base',
    medium: 'text-lg', 
    large: 'text-xl',
    'extra-large': 'text-2xl'
  }[preferences.fontSize];

  const progress = currentChapterId ? readingProgress[currentChapterId] : null;

  return (
    <div className={`h-screen flex flex-col ${preferences.theme}`}>
      {/* Header */}
      <div className="flex-shrink-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 px-4 py-3">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-gray-900 dark:text-white">
              {bookData.metadata.title}
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {currentChapter.enhanced.chapter_metadata.title} • {currentChapter.enhanced.chapter_metadata.reduction_percentage}% reduced
            </p>
          </div>
          <div className="text-right">
            {progress && (
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {progress.percentComplete}% complete
              </div>
            )}
          </div>
        </div>

        {/* Progress Bar */}
        {progress && (
          <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1">
            <div 
              className="bg-blue-500 h-1 rounded-full transition-all duration-300"
              style={{ width: `${progress.percentComplete}%` }}
            />
          </div>
        )}
      </div>

      {/* Main Reading Area */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto"
        style={{ 
          WebkitOverflowScrolling: 'touch' 
        }}
      >
        <div className={`max-w-4xl mx-auto px-6 py-8 ${fontSizeClass}`}>
          {/* Chapter Title */}
          <div className="mb-8 text-center">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Chapter {currentChapter.enhanced.chapter_metadata.chapter_number}
            </h2>
            <h3 className="text-2xl text-gray-700 dark:text-gray-300">
              {currentChapter.enhanced.chapter_metadata.title}
            </h3>
            <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Enhanced • {currentChapter.enhanced.chapter_metadata.enhanced_word_count.toLocaleString()} words
              {preferences.showOriginalIndicators && (
                <span className="ml-2">• Double-tap paragraphs to see original</span>
              )}
            </div>
          </div>

          {/* Chapter Content */}
          <div className="space-y-6">
            {currentChapter.enhanced.enhanced_content.map((item, index) => (
              <EnhancedParagraphRenderer
                key={`${item.type}-${index}`}
                item={item}
                originalChapter={currentChapter.original}
                isSelected={selectedParagraphId === item.paragraph_id}
                showOriginalIndicators={preferences.showOriginalIndicators}
                onParagraphClick={handleParagraphClick}
              />
            ))}
          </div>

          {/* Bottom padding for comfortable reading */}
          <div className="h-32" />
        </div>
      </div>

      {/* Original Mapping Overlay */}
      {originalMappingVisible && selectedParagraphId && (
        <OriginalMappingOverlay
          enhancedParagraphId={selectedParagraphId}
          enhancedChapter={currentChapter.enhanced}
          originalChapter={currentChapter.original}
          onClose={hideOriginalMapping}
        />
      )}
    </div>
  );
}