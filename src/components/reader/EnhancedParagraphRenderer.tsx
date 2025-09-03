import React from 'react';
import type { EnhancedContentItem, OriginalChapterContent } from '../../types/enhancedChapter';

interface EnhancedParagraphRendererProps {
  item: EnhancedContentItem;
  originalChapter: OriginalChapterContent;
  isSelected: boolean;
  showOriginalIndicators: boolean;
  onParagraphClick: (paragraphId: string, event: React.MouseEvent) => void;
}

export function EnhancedParagraphRenderer({ 
  item, 
  originalChapter, 
  isSelected, 
  showOriginalIndicators,
  onParagraphClick 
}: EnhancedParagraphRendererProps) {
  
  const getMappingIndicator = () => {
    if (!showOriginalIndicators || !item.original_mapping?.length) return null;

    const mappingCount = item.original_mapping.length;
    const reductionType = item.reduction_type;
    
    let indicatorText = '';
    let indicatorClass = 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
    
    switch (reductionType) {
      case 'one_to_one':
        indicatorText = '1:1';
        indicatorClass = 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
        break;
      case 'many_to_one':
        indicatorText = `${mappingCount}:1`;
        indicatorClass = 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300';
        break;
      case 'one_to_many':
        indicatorText = '1:M';
        indicatorClass = 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300';
        break;
      case 'none_to_one':
        indicatorText = 'NEW';
        indicatorClass = 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
        break;
      default:
        indicatorText = `${mappingCount}`;
    }

    return (
      <span className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${indicatorClass} mr-2`}>
        {indicatorText}
      </span>
    );
  };

  const handleClick = (event: React.MouseEvent) => {
    if (item.paragraph_id) {
      onParagraphClick(item.paragraph_id, event);
    }
  };

  const baseClasses = isSelected 
    ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' 
    : 'hover:bg-gray-50 dark:hover:bg-gray-800/50';

  const interactiveClasses = item.paragraph_id 
    ? `cursor-pointer transition-all duration-200 ${baseClasses}` 
    : '';

  switch (item.type) {
    case 'paragraph':
      return (
        <div
          data-paragraph-id={item.paragraph_id}
          className={`p-3 rounded-lg ${interactiveClasses}`}
          onClick={item.paragraph_id ? handleClick : undefined}
        >
          <div className="flex items-start">
            {getMappingIndicator()}
            <p className="text-gray-900 dark:text-gray-100 leading-relaxed flex-1">
              {item.text}
            </p>
          </div>
          {showOriginalIndicators && item.preservation_notes && (
            <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 italic">
              {item.preservation_notes}
            </div>
          )}
        </div>
      );

    case 'heading':
      const level = Math.min(item.level || 2, 6);
      const headingClasses = {
        1: 'text-3xl font-bold',
        2: 'text-2xl font-semibold', 
        3: 'text-xl font-semibold',
        4: 'text-lg font-semibold',
        5: 'text-base font-semibold',
        6: 'text-base font-medium'
      }[level];

      const HeadingComponent = ({ children, className }: { children: React.ReactNode, className: string }) => {
        const props = { className, children };
        switch (level) {
          case 1: return <h1 {...props} />;
          case 2: return <h2 {...props} />;
          case 3: return <h3 {...props} />;
          case 4: return <h4 {...props} />;
          case 5: return <h5 {...props} />;
          case 6: return <h6 {...props} />;
          default: return <h2 {...props} />;
        }
      };

      return (
        <div className="mt-8 mb-4">
          <HeadingComponent className={`${headingClasses} text-gray-900 dark:text-white`}>
            {item.text}
          </HeadingComponent>
        </div>
      );

    case 'image':
      return (
        <div className="my-6">
          <div className="flex justify-center">
            <div className="max-w-full">
              <img
                src={`/game-feel/images/${item.src}`}
                alt={item.caption || 'Figure'}
                className="max-w-full h-auto rounded-lg shadow-md"
              />
              {item.caption && (
                <p className="text-sm text-gray-600 dark:text-gray-400 text-center mt-2 italic">
                  {item.caption}
                </p>
              )}
            </div>
          </div>
        </div>
      );

    case 'footnote':
      return (
        <div className="my-2 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border-l-4 border-blue-500">
          <p className="text-sm text-gray-700 dark:text-gray-300">
            {item.text}
          </p>
        </div>
      );

    case 'list':
      return (
        <div className="my-4">
          <ul className="list-disc list-inside space-y-2 text-gray-900 dark:text-gray-100">
            {item.items?.map((listItem, index) => (
              <li key={index} className="leading-relaxed">
                {listItem}
              </li>
            ))}
          </ul>
        </div>
      );

    default:
      return (
        <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
          <p className="text-yellow-800 dark:text-yellow-200">
            Unknown content type: {item.type}
          </p>
        </div>
      );
  }
}