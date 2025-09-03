import React from 'react';

interface Chapter {
  id: string;
  number: number;
  title: string;
  description: string;
  enhanced: boolean;
}

const chapters: Chapter[] = [
  {
    id: 'chapter-01',
    number: 1,
    title: 'Introduction',
    description: 'Opening exploration of game feel with enhanced clarity and 29.4% reduction',
    enhanced: true
  },
  {
    id: 'chapter-04', 
    number: 4,
    title: 'The Game Feel Model of Interactivity',
    description: 'Comprehensive model with technical precision and 29.4% reduction',
    enhanced: true
  }
];

interface ChapterNavigationProps {
  currentChapterId?: string;
}

export default function ChapterNavigation({ currentChapterId }: ChapterNavigationProps) {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Game Feel: Enhanced Edition
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          A Game Designer's Guide to Virtual Sensation by Steve Swink
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
          Enhanced with 30% length reduction while preserving the author's unique voice
        </p>
      </div>

      <div className="grid gap-4 md:gap-6">
        {chapters.map((chapter) => (
          <ChapterCard 
            key={chapter.id}
            chapter={chapter} 
            isActive={currentChapterId === chapter.id}
          />
        ))}
      </div>

      <div className="mt-8 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
        <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
          📚 Enhanced Reading Experience
        </h3>
        <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-1">
          <li>• <strong>Double-tap</strong> any paragraph to see original content</li>
          <li>• <strong>Mapping indicators</strong> show how content was transformed</li>
          <li>• <strong>Automatic progress saving</strong> tracks your reading position</li>
          <li>• <strong>Voice preservation</strong> maintains Steve Swink's distinctive style</li>
        </ul>
      </div>
    </div>
  );
}

interface ChapterCardProps {
  chapter: Chapter;
  isActive: boolean;
}

function ChapterCard({ chapter, isActive }: ChapterCardProps) {
  const cardClasses = isActive
    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600';

  return (
    <a 
      href={`/reader/${chapter.id}`}
      className={`block p-6 rounded-lg border-2 transition-all duration-200 ${cardClasses}`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <span className="inline-block px-3 py-1 text-sm font-medium bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-full mr-3">
              Chapter {chapter.number}
            </span>
            {chapter.enhanced && (
              <span className="inline-block px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full">
                Enhanced
              </span>
            )}
          </div>
          
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            {chapter.title}
          </h3>
          
          <p className="text-gray-600 dark:text-gray-400 mb-3">
            {chapter.description}
          </p>
          
          <div className="flex items-center text-sm text-gray-500 dark:text-gray-500">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            Click to read
          </div>
        </div>
        
        <div className="flex-shrink-0 ml-4">
          <svg className="w-6 h-6 text-gray-400 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>
    </a>
  );
}