import React, { useState } from 'react';
import type { ProcessedBook } from '../../types/schema';
import { useBookStore } from '../../stores/bookStore';

interface ReaderHeaderProps {
  book: ProcessedBook;
  isScrolling: boolean;
}

export function ReaderHeader({ book, isScrolling }: ReaderHeaderProps) {
  const { preferences, setTheme, setFontSize, updatePreferences } = useBookStore();
  const [showSettings, setShowSettings] = useState(false);

  const toggleTheme = () => {
    setTheme(preferences.theme === 'light' ? 'dark' : 'light');
  };

  const adjustFontSize = (direction: 'up' | 'down') => {
    const sizes: Array<typeof preferences.fontSize> = ['small', 'medium', 'large', 'extra-large'];
    const currentIndex = sizes.indexOf(preferences.fontSize);
    
    if (direction === 'up' && currentIndex < sizes.length - 1) {
      setFontSize(sizes[currentIndex + 1]);
    } else if (direction === 'down' && currentIndex > 0) {
      setFontSize(sizes[currentIndex - 1]);
    }
  };

  return (
    <>
      {/* Header */}
      <header 
        className={`
          sticky top-0 z-40 bg-reading-bg/90 dark:bg-reading-bg-dark/90 
          backdrop-blur-sm border-b border-gray-200 dark:border-gray-700
          transition-all duration-300
          ${isScrolling ? 'py-2' : 'py-3'}
        `}
      >
        <div className="flex items-center justify-between px-4 md:px-6">
          {/* Back button and title */}
          <div className="flex items-center space-x-3 flex-1 min-w-0">
            <button
              onClick={() => window.history.back()}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              aria-label="Go back"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            
            <div className="min-w-0 flex-1">
              <h1 className={`
                font-medium text-reading-text dark:text-reading-text-dark
                truncate transition-all duration-300
                ${isScrolling ? 'text-sm' : 'text-base'}
              `}>
                {book.metadata.title}
              </h1>
              {!isScrolling && (
                <p className="text-xs text-reading-text-muted dark:text-reading-text-muted-dark truncate">
                  {book.metadata.author}
                </p>
              )}
            </div>
          </div>

          {/* Reading controls */}
          <div className="flex items-center space-x-2">
            {/* Font size controls */}
            <div className="flex items-center space-x-1">
              <button
                onClick={() => adjustFontSize('down')}
                disabled={preferences.fontSize === 'small'}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors disabled:opacity-50"
                aria-label="Decrease font size"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <text x="10" y="15" textAnchor="middle" fontSize="12" fontFamily="serif">A</text>
                </svg>
              </button>
              <button
                onClick={() => adjustFontSize('up')}
                disabled={preferences.fontSize === 'extra-large'}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors disabled:opacity-50"
                aria-label="Increase font size"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <text x="10" y="15" textAnchor="middle" fontSize="16" fontFamily="serif">A</text>
                </svg>
              </button>
            </div>

            {/* Theme toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              aria-label="Toggle theme"
            >
              {preferences.theme === 'light' ? (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              )}
            </button>

            {/* Settings button */}
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              aria-label="Settings"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      {/* Settings Panel */}
      {showSettings && (
        <div className="absolute top-full left-0 right-0 z-50 bg-reading-bg dark:bg-reading-bg-dark border-b border-gray-200 dark:border-gray-700 shadow-lg">
          <div className="p-4 space-y-4">
            {/* Reading preferences */}
            <div>
              <h3 className="text-sm font-medium mb-2 text-reading-text dark:text-reading-text-dark">
                Reading Preferences
              </h3>
              
              <div className="space-y-3">
                {/* Font Family */}
                <div>
                  <label className="text-xs text-reading-text-muted dark:text-reading-text-muted-dark">
                    Font Family
                  </label>
                  <select
                    value={preferences.fontFamily}
                    onChange={(e) => updatePreferences({ fontFamily: e.target.value as any })}
                    className="w-full mt-1 p-2 text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md"
                  >
                    <option value="system">System Default</option>
                    <option value="serif">Serif (Crimson Text)</option>
                    <option value="sans-serif">Sans Serif (Inter)</option>
                    <option value="monospace">Monospace (JetBrains)</option>
                  </select>
                </div>

                {/* Line Height */}
                <div>
                  <label className="text-xs text-reading-text-muted dark:text-reading-text-muted-dark">
                    Line Spacing
                  </label>
                  <select
                    value={preferences.lineHeight}
                    onChange={(e) => updatePreferences({ lineHeight: e.target.value as any })}
                    className="w-full mt-1 p-2 text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md"
                  >
                    <option value="compact">Compact</option>
                    <option value="normal">Normal</option>
                    <option value="relaxed">Relaxed</option>
                  </select>
                </div>

                {/* Original indicators toggle */}
                <div className="flex items-center justify-between">
                  <label className="text-xs text-reading-text-muted dark:text-reading-text-muted-dark">
                    Show AI Enhancement Indicators
                  </label>
                  <button
                    onClick={() => updatePreferences({ showOriginalIndicators: !preferences.showOriginalIndicators })}
                    className={`
                      relative inline-flex h-6 w-11 items-center rounded-full transition-colors
                      ${preferences.showOriginalIndicators ? 'bg-reading-accent dark:bg-reading-accent-dark' : 'bg-gray-200 dark:bg-gray-700'}
                    `}
                  >
                    <span
                      className={`
                        inline-block h-4 w-4 transform rounded-full bg-white shadow-lg transition-transform
                        ${preferences.showOriginalIndicators ? 'translate-x-6' : 'translate-x-1'}
                      `}
                    />
                  </button>
                </div>

                {/* Double-tap sensitivity */}
                <div>
                  <label className="text-xs text-reading-text-muted dark:text-reading-text-muted-dark">
                    Double-tap Sensitivity
                  </label>
                  <select
                    value={preferences.doubleTapSensitivity}
                    onChange={(e) => updatePreferences({ doubleTapSensitivity: e.target.value as any })}
                    className="w-full mt-1 p-2 text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Close button */}
            <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
              <button
                onClick={() => setShowSettings(false)}
                className="w-full py-2 text-sm text-reading-text-muted dark:text-reading-text-muted-dark hover:text-reading-text dark:hover:text-reading-text-dark transition-colors"
              >
                Close Settings
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}