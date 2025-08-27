import React from 'react';
import type { ProcessedBook } from '../../types/schema';
import { useBookStore } from '../../stores/bookStore';

interface BookCardProps {
  book: ProcessedBook;
  viewMode: 'grid' | 'list';
  showProgress: boolean;
}

export function BookCard({ book, viewMode, showProgress }: BookCardProps) {
  const { allBooks } = useBookStore();
  
  // Get reading progress for this book (mock for now)
  const getReadingProgress = () => {
    // This would normally come from the reading progress store
    // For now, return a mock progress
    return Math.floor(Math.random() * 100);
  };

  const progress = showProgress ? getReadingProgress() : 0;

  const handleCardClick = () => {
    window.location.href = `/reader/${book.id}`;
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      business: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
      academic: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
      biography: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      science: 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200',
      'self-help': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      technical: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
      other: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
    };
    return colors[category as keyof typeof colors] || colors.other;
  };

  const formatReadingTime = (minutes: number) => {
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
  };

  if (viewMode === 'list') {
    return (
      <div
        onClick={handleCardClick}
        className="bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer border border-gray-200 dark:border-gray-700 p-4"
      >
        <div className="flex items-center space-x-4">
          {/* Book cover placeholder */}
          <div className="flex-shrink-0">
            <div className="w-16 h-20 bg-gradient-to-br from-reading-accent to-reading-accent-dark dark:from-reading-accent-dark dark:to-reading-accent rounded-md shadow-sm flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>

          {/* Book info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <h3 className="text-lg font-semibold text-reading-text dark:text-reading-text-dark truncate">
                  {book.metadata.title}
                </h3>
                <p className="text-reading-text-muted dark:text-reading-text-muted-dark mt-1">
                  by {book.metadata.author}
                </p>
                
                <div className="flex items-center gap-3 mt-2">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getCategoryColor(book.metadata.category)}`}>
                    {book.metadata.category}
                  </span>
                  <span className="text-xs text-reading-text-muted dark:text-reading-text-muted-dark">
                    {formatReadingTime(book.metadata.estimatedReadingTimeMinutes)} read
                  </span>
                </div>
              </div>

              {/* Reading progress */}
              {showProgress && progress > 0 && (
                <div className="text-right flex-shrink-0 ml-4">
                  <div className="text-sm font-medium text-reading-text dark:text-reading-text-dark">
                    {progress}%
                  </div>
                  <div className="w-16 h-2 bg-gray-200 dark:bg-gray-700 rounded-full mt-1">
                    <div 
                      className="h-full bg-reading-accent dark:bg-reading-accent-dark rounded-full transition-all duration-300"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      onClick={handleCardClick}
      className="bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-lg transition-all duration-200 cursor-pointer border border-gray-200 dark:border-gray-700 overflow-hidden group"
    >
      {/* Book cover */}
      <div className="aspect-[3/4] bg-gradient-to-br from-reading-accent to-reading-accent-dark dark:from-reading-accent-dark dark:to-reading-accent relative overflow-hidden">
        <div className="absolute inset-0 bg-black/10 group-hover:bg-black/5 transition-colors" />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-white text-center px-4">
            <svg className="w-12 h-12 mx-auto mb-2 opacity-90" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="text-xs font-medium opacity-75">AI Enhanced</div>
          </div>
        </div>
        
        {/* Progress indicator */}
        {showProgress && progress > 0 && (
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-white/20">
            <div 
              className="h-full bg-white transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        )}
      </div>

      {/* Book details */}
      <div className="p-4">
        <div className="mb-3">
          <h3 className="font-semibold text-reading-text dark:text-reading-text-dark line-clamp-2 mb-1">
            {book.metadata.title}
          </h3>
          <p className="text-sm text-reading-text-muted dark:text-reading-text-muted-dark line-clamp-1">
            by {book.metadata.author}
          </p>
        </div>

        <div className="flex items-center justify-between">
          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(book.metadata.category)}`}>
            {book.metadata.category}
          </span>
          
          <div className="text-xs text-reading-text-muted dark:text-reading-text-muted-dark">
            {formatReadingTime(book.metadata.estimatedReadingTimeMinutes)}
          </div>
        </div>

        {/* Reading progress for continue reading cards */}
        {showProgress && progress > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs text-reading-text-muted dark:text-reading-text-muted-dark">
                Progress
              </span>
              <span className="text-xs font-medium text-reading-text dark:text-reading-text-dark">
                {progress}%
              </span>
            </div>
            <div className="w-full h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full">
              <div 
                className="h-full bg-reading-accent dark:bg-reading-accent-dark rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Add CSS for line-clamp utility (if not available in Tailwind)
const style = `
  .line-clamp-1 {
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
`;

// Inject styles if needed
if (typeof document !== 'undefined' && !document.getElementById('line-clamp-styles')) {
  const styleElement = document.createElement('style');
  styleElement.id = 'line-clamp-styles';
  styleElement.textContent = style;
  document.head.appendChild(styleElement);
}