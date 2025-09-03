import React from 'react';
import type { EnhancedChapter, OriginalChapterContent } from '../../types/enhancedChapter';

interface OriginalMappingOverlayProps {
  enhancedParagraphId: string;
  enhancedChapter: EnhancedChapter;
  originalChapter: OriginalChapterContent;
  onClose: () => void;
}

export function OriginalMappingOverlay({
  enhancedParagraphId,
  enhancedChapter,
  originalChapter,
  onClose
}: OriginalMappingOverlayProps) {
  
  // Find the enhanced paragraph
  const enhancedItem = enhancedChapter.enhanced_content.find(
    item => item.paragraph_id === enhancedParagraphId
  );

  if (!enhancedItem) {
    return null;
  }

  // Get original paragraph IDs that map to this enhanced paragraph
  const originalParagraphIds = enhancedItem.original_mapping || [];

  // Find the original paragraphs
  const originalParagraphs = originalParagraphIds.map(id => {
    // The ID format might be "p1", "p2", etc., but we need to find the actual content
    // Since we don't have indexed paragraphs in the original, we'll search by content matching
    const paragraphIndex = parseInt(id.replace('p', '')) - 1; // Convert p1 to index 0
    return originalChapter.content[paragraphIndex];
  }).filter(Boolean);

  const getMappingTypeInfo = () => {
    const type = enhancedItem.reduction_type;
    const count = originalParagraphIds.length;
    
    switch (type) {
      case 'one_to_one':
        return { 
          badge: '1:1 Enhancement', 
          color: 'green',
          description: 'One original paragraph enhanced directly'
        };
      case 'many_to_one':
        return { 
          badge: `${count}:1 Merge`, 
          color: 'orange',
          description: `${count} original paragraphs merged into one`
        };
      case 'one_to_many':
        return { 
          badge: '1:M Split', 
          color: 'purple',
          description: 'One original paragraph split for clarity'
        };
      case 'none_to_one':
        return { 
          badge: 'New Content', 
          color: 'yellow',
          description: 'New transitional content added'
        };
      default:
        return { 
          badge: 'Mapped', 
          color: 'blue',
          description: 'Content transformation applied'
        };
    }
  };

  const mappingInfo = getMappingTypeInfo();
  const badgeClasses = {
    green: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    orange: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
    purple: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
    yellow: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
    blue: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
  }[mappingInfo.color];

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-6xl max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Original Content Mapping
              </h3>
              <div className="flex items-center mt-1">
                <span className={`inline-block px-3 py-1 text-xs font-medium rounded-full ${badgeClasses} mr-3`}>
                  {mappingInfo.badge}
                </span>
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {mappingInfo.description}
                </span>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto">
          <div className="grid md:grid-cols-2 gap-6 p-6">
            
            {/* Enhanced Version */}
            <div>
              <h4 className="text-md font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
                <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                Enhanced Version
              </h4>
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
                <p className="text-gray-900 dark:text-gray-100 leading-relaxed">
                  {enhancedItem.text}
                </p>
                {enhancedItem.preservation_notes && (
                  <div className="mt-3 pt-3 border-t border-blue-200 dark:border-blue-800">
                    <p className="text-sm text-blue-700 dark:text-blue-300 italic">
                      <strong>Notes:</strong> {enhancedItem.preservation_notes}
                    </p>
                  </div>
                )}
              </div>
              
              {/* Enhancement Stats */}
              <div className="mt-3 text-sm text-gray-600 dark:text-gray-400">
                Words: ~{enhancedItem.text?.split(' ').length || 0}
              </div>
            </div>

            {/* Original Version(s) */}
            <div>
              <h4 className="text-md font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
                <span className="w-2 h-2 bg-gray-500 rounded-full mr-2"></span>
                Original Version{originalParagraphs.length > 1 ? 's' : ''}
              </h4>
              <div className="space-y-4">
                {originalParagraphs.length > 0 ? (
                  originalParagraphs.map((paragraph, index) => (
                    <div key={index} className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                      {paragraph.type === 'paragraph' && (
                        <p className="text-gray-900 dark:text-gray-100 leading-relaxed">
                          {paragraph.text}
                        </p>
                      )}
                      {paragraph.type === 'heading' && (
                        <h5 className="font-semibold text-gray-900 dark:text-gray-100">
                          {paragraph.text}
                        </h5>
                      )}
                      {paragraph.type === 'footnote' && (
                        <p className="text-sm text-gray-700 dark:text-gray-300 italic">
                          {paragraph.text}
                        </p>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                    <p className="text-gray-500 dark:text-gray-400 italic">
                      Original content not available for mapping IDs: {originalParagraphIds.join(', ')}
                    </p>
                  </div>
                )}
              </div>
              
              {/* Original Stats */}
              <div className="mt-3 text-sm text-gray-600 dark:text-gray-400">
                Total words: ~{originalParagraphs.reduce((total, p) => 
                  total + (p.text?.split(' ').length || 0), 0
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
          <div className="flex justify-between items-center text-sm">
            <div className="text-gray-600 dark:text-gray-400">
              Reduction: {enhancedChapter.chapter_metadata.reduction_percentage}% • 
              Voice Score: {(enhancedChapter.chapter_metadata.voice_consistency_score * 100).toFixed(0)}%
            </div>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}