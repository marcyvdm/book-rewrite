import React from 'react';

interface EmptyStateProps {
  hasBooks: boolean;
  searchQuery: string;
  selectedCategory: string;
}

export function EmptyState({ hasBooks, searchQuery, selectedCategory }: EmptyStateProps) {
  if (searchQuery) {
    return (
      <div className="text-center py-16">
        <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <h3 className="text-lg font-medium text-reading-text dark:text-reading-text-dark mb-2">
          No books found
        </h3>
        <p className="text-reading-text-muted dark:text-reading-text-muted-dark">
          No books match your search for "{searchQuery}". Try adjusting your search terms.
        </p>
      </div>
    );
  }

  if (selectedCategory !== 'all') {
    return (
      <div className="text-center py-16">
        <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <h3 className="text-lg font-medium text-reading-text dark:text-reading-text-dark mb-2">
          No {selectedCategory} books yet
        </h3>
        <p className="text-reading-text-muted dark:text-reading-text-muted-dark">
          You don't have any books in the {selectedCategory} category. Try browsing all books or adding new ones.
        </p>
      </div>
    );
  }

  if (!hasBooks) {
    return (
      <div className="text-center py-16">
        <div className="mx-auto h-24 w-24 bg-gradient-to-br from-reading-accent to-reading-accent-dark dark:from-reading-accent-dark dark:to-reading-accent rounded-full flex items-center justify-center mb-6">
          <svg className="h-12 w-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-reading-text dark:text-reading-text-dark mb-4">
          Welcome to your AI Book Library
        </h3>
        <p className="text-reading-text-muted dark:text-reading-text-muted-dark mb-8 max-w-md mx-auto">
          Transform your reading experience with AI-enhanced books. Upload your first book to get started with intelligent rewriting and improved comprehension.
        </p>
        
        <div className="space-y-4">
          <div className="text-sm text-reading-text-muted dark:text-reading-text-muted-dark">
            Add books via VS Code by processing files in the to-be-processed folder
          </div>
        </div>

        {/* Features preview */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="text-center">
            <div className="mx-auto h-12 w-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center mb-4">
              <svg className="h-6 w-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h4 className="font-medium text-reading-text dark:text-reading-text-dark mb-2">
              AI Enhancement
            </h4>
            <p className="text-sm text-reading-text-muted dark:text-reading-text-muted-dark">
              Improve clarity and comprehension while preserving the author's voice
            </p>
          </div>

          <div className="text-center">
            <div className="mx-auto h-12 w-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mb-4">
              <svg className="h-6 w-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
              </svg>
            </div>
            <h4 className="font-medium text-reading-text dark:text-reading-text-dark mb-2">
              Original Access
            </h4>
            <p className="text-sm text-reading-text-muted dark:text-reading-text-muted-dark">
              Double-tap any paragraph to see the original text and understand AI changes
            </p>
          </div>

          <div className="text-center">
            <div className="mx-auto h-12 w-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center mb-4">
              <svg className="h-6 w-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <h4 className="font-medium text-reading-text dark:text-reading-text-dark mb-2">
              Mobile First
            </h4>
            <p className="text-sm text-reading-text-muted dark:text-reading-text-muted-dark">
              Optimized reading experience designed for mobile devices and touch interaction
            </p>
          </div>
        </div>
      </div>
    );
  }

  // This shouldn't happen, but just in case
  return (
    <div className="text-center py-16">
      <h3 className="text-lg font-medium text-reading-text dark:text-reading-text-dark mb-2">
        Something went wrong
      </h3>
      <p className="text-reading-text-muted dark:text-reading-text-muted-dark">
        Unable to display books. Please try refreshing the page.
      </p>
    </div>
  );
}