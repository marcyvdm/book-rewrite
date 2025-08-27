import React, { useEffect } from 'react';
import type { ParagraphMapping, Paragraph } from '../../types/schema';

interface OriginalOverlayProps {
  paragraphId: string;
  mapping?: ParagraphMapping;
  originalParagraphs: Paragraph[];
  onClose: () => void;
}

export function OriginalOverlay({ 
  paragraphId, 
  mapping, 
  originalParagraphs, 
  onClose 
}: OriginalOverlayProps) {
  
  useEffect(() => {
    // Prevent body scroll when overlay is open
    document.body.style.overflow = 'hidden';
    
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  const getOriginalContent = () => {
    if (!mapping) {
      return "No original mapping found for this paragraph.";
    }

    const originalTexts = mapping.originalParagraphIds
      .map(id => originalParagraphs.find(p => p.id === id))
      .filter(Boolean)
      .map(p => p!.content);

    return originalTexts.join('\n\n');
  };

  const getMappingInfo = () => {
    if (!mapping) return null;

    const mappingTypeLabels = {
      '1:1': 'Direct Enhancement',
      'N:1': 'Condensed from Multiple Paragraphs', 
      '1:N': 'Expanded Content',
      'contextual': 'Enhanced with Additional Context'
    };

    return {
      type: mappingTypeLabels[mapping.mappingType],
      improvements: mapping.improvementTypes,
      confidence: mapping.confidenceScore,
      quality: mapping.qualityMetrics
    };
  };

  const originalContent = getOriginalContent();
  const mappingInfo = getMappingInfo();

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm animate-fade-in">
      {/* Overlay background - clicking closes */}
      <div 
        className="absolute inset-0" 
        onClick={onClose}
        onTouchEnd={onClose}
      />
      
      {/* Content panel */}
      <div className="absolute bottom-0 left-0 right-0 max-h-[80vh] bg-reading-bg dark:bg-reading-bg-dark rounded-t-xl shadow-2xl animate-slide-up">
        {/* Handle bar */}
        <div className="flex justify-center py-3">
          <div className="w-10 h-1 bg-gray-300 dark:bg-gray-600 rounded-full" />
        </div>
        
        {/* Header */}
        <div className="flex items-center justify-between px-4 pb-4 border-b border-gray-200 dark:border-gray-700">
          <div>
            <h3 className="text-lg font-semibold text-reading-text dark:text-reading-text-dark">
              Original Text
            </h3>
            {mappingInfo && (
              <p className="text-sm text-reading-text-muted dark:text-reading-text-muted-dark">
                {mappingInfo.type}
              </p>
            )}
          </div>
          
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(80vh-120px)]">
          <div className="p-4 space-y-4">
            {/* Original text */}
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
              <h4 className="text-sm font-medium mb-2 text-reading-text dark:text-reading-text-dark">
                Original Author's Text
              </h4>
              <div className="selectable-text text-reading-text dark:text-reading-text-dark leading-relaxed whitespace-pre-wrap">
                {originalContent}
              </div>
            </div>
            
            {/* Mapping information */}
            {mappingInfo && (
              <div className="space-y-3">
                {/* Improvements made */}
                {mappingInfo.improvements.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium mb-2 text-reading-text dark:text-reading-text-dark">
                      AI Improvements Applied
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {mappingInfo.improvements.map((improvement, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 text-xs bg-reading-accent/10 text-reading-accent dark:bg-reading-accent-dark/20 dark:text-reading-accent-dark rounded-full"
                        >
                          {improvement.charAt(0).toUpperCase() + improvement.slice(1)}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Quality metrics */}
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-reading-text-muted dark:text-reading-text-muted-dark">
                      AI Confidence
                    </span>
                    <div className="font-medium text-reading-text dark:text-reading-text-dark">
                      {mappingInfo.confidence}/100
                    </div>
                  </div>
                  
                  <div>
                    <span className="text-reading-text-muted dark:text-reading-text-muted-dark">
                      Voice Preservation
                    </span>
                    <div className="font-medium text-reading-text dark:text-reading-text-dark">
                      {Math.round(mappingInfo.quality.voicePreservationScore)}/100
                    </div>
                  </div>
                  
                  <div>
                    <span className="text-reading-text-muted dark:text-reading-text-muted-dark">
                      Clarity Improvement
                    </span>
                    <div className="font-medium text-reading-text dark:text-reading-text-dark">
                      {Math.round(mappingInfo.quality.clarityImprovementScore)}/100
                    </div>
                  </div>
                  
                  <div>
                    <span className="text-reading-text-muted dark:text-reading-text-muted-dark">
                      Length Change
                    </span>
                    <div className="font-medium text-reading-text dark:text-reading-text-dark">
                      {mappingInfo.quality.lengthChangePercentage > 0 ? '+' : ''}
                      {Math.round(mappingInfo.quality.lengthChangePercentage)}%
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
        
        {/* Footer */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
          <p className="text-xs text-center text-reading-text-muted dark:text-reading-text-muted-dark">
            Tap outside this panel to continue reading the AI-enhanced version
          </p>
        </div>
      </div>
    </div>
  );
}