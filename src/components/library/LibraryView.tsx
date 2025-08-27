import React, { useEffect, useState } from 'react';
import { useBookStore } from '../../stores/bookStore';
import { BookCard } from './BookCard';
import { SearchBar } from './SearchBar';
import { FilterTabs } from './FilterTabs';
import { EmptyState } from './EmptyState';

export default function LibraryView() {
  const { 
    allBooks, 
    recentBooks,
    isLoading, 
    error, 
    loadAllBooks 
  } = useBookStore();
  
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  useEffect(() => {
    loadAllBooks();
    
    // Load Game Feel book for demo
    import('../../utils/loadProcessedBook').then(module => {
      module.loadGameFeelBook().then(() => {
        // Reload books after adding Game Feel
        loadAllBooks();
      }).catch(console.error);
    }).catch(console.error);
  }, [loadAllBooks]);

  // Filter books based on search and category
  const filteredBooks = allBooks.filter(book => {
    const matchesSearch = !searchQuery || 
      book.metadata.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      book.metadata.author.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesCategory = selectedCategory === 'all' || 
      book.metadata.category === selectedCategory;
    
    return matchesSearch && matchesCategory;
  });

  // Get unique categories for filtering
  const categories = ['all', ...new Set(allBooks.map(book => book.metadata.category))];

  if (isLoading && allBooks.length === 0) {
    return (
      <div className="min-h-screen bg-reading-bg dark:bg-reading-bg-dark">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-center h-64">
            <div className="animate-pulse-slow">
              <div className="text-reading-text-muted dark:text-reading-text-muted-dark text-lg">
                Loading library...
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-reading-bg dark:bg-reading-bg-dark">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="text-red-500 text-lg font-medium mb-2">Error</div>
              <div className="text-reading-text-muted dark:text-reading-text-muted-dark">
                {error}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-reading-bg dark:bg-reading-bg-dark">
      {/* Header */}
      <header className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col space-y-4">
            {/* Title and view toggle */}
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl md:text-3xl font-bold text-reading-text dark:text-reading-text-dark">
                  AI Book Library
                </h1>
                <p className="text-reading-text-muted dark:text-reading-text-muted-dark mt-1">
                  {allBooks.length} {allBooks.length === 1 ? 'book' : 'books'} in your collection
                </p>
              </div>
              
              {/* View mode toggle */}
              <div className="flex items-center space-x-2 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 rounded-md transition-colors ${
                    viewMode === 'grid' 
                      ? 'bg-white dark:bg-gray-700 shadow-sm' 
                      : 'hover:bg-gray-200 dark:hover:bg-gray-700'
                  }`}
                  aria-label="Grid view"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                  </svg>
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 rounded-md transition-colors ${
                    viewMode === 'list' 
                      ? 'bg-white dark:bg-gray-700 shadow-sm' 
                      : 'hover:bg-gray-200 dark:hover:bg-gray-700'
                  }`}
                  aria-label="List view"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 8a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 12a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 16a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Search and filters */}
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <SearchBar 
                  value={searchQuery}
                  onChange={setSearchQuery}
                  placeholder="Search by title or author..."
                />
              </div>
              <FilterTabs
                categories={categories}
                selectedCategory={selectedCategory}
                onCategoryChange={setSelectedCategory}
              />
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="container mx-auto px-4 py-8">
        {/* Recent books section */}
        {recentBooks.length > 0 && selectedCategory === 'all' && !searchQuery && (
          <section className="mb-12">
            <h2 className="text-xl font-semibold text-reading-text dark:text-reading-text-dark mb-6">
              Continue Reading
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {recentBooks.slice(0, 4).map(book => (
                <BookCard 
                  key={`recent-${book.id}`}
                  book={book}
                  viewMode="grid"
                  showProgress={true}
                />
              ))}
            </div>
          </section>
        )}

        {/* All books section */}
        <section>
          {selectedCategory !== 'all' || searchQuery ? (
            <h2 className="text-xl font-semibold text-reading-text dark:text-reading-text-dark mb-6">
              {searchQuery ? `Search Results (${filteredBooks.length})` : 
               `${selectedCategory.charAt(0).toUpperCase() + selectedCategory.slice(1)} Books`}
            </h2>
          ) : (
            <h2 className="text-xl font-semibold text-reading-text dark:text-reading-text-dark mb-6">
              All Books
            </h2>
          )}

          {filteredBooks.length === 0 ? (
            <EmptyState 
              hasBooks={allBooks.length > 0}
              searchQuery={searchQuery}
              selectedCategory={selectedCategory}
            />
          ) : (
            <div className={
              viewMode === 'grid' 
                ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'
                : 'space-y-4'
            }>
              {filteredBooks.map(book => (
                <BookCard 
                  key={book.id}
                  book={book}
                  viewMode={viewMode}
                  showProgress={false}
                />
              ))}
            </div>
          )}
        </section>

      </main>
    </div>
  );
}