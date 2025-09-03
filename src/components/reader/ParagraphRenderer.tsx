import React, { useRef, useState } from 'react';
import { useBookStore } from '../../stores/bookStore';
import type { Paragraph, ParagraphMapping } from '../../types/schema';

interface ParagraphRendererProps {
  paragraph: Paragraph;
  mapping?: ParagraphMapping;
  originalParagraphs: Paragraph[];
  isSelected: boolean;
  showOriginal: boolean;
}

export function ParagraphRenderer({
  paragraph,
  mapping,
  originalParagraphs,
  isSelected,
  showOriginal,
}: ParagraphRendererProps) {
  const { toggleOriginal, preferences } = useBookStore();
  const [tapCount, setTapCount] = useState(0);
  const tapTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleTap = (event: React.TouchEvent | React.MouseEvent) => {
    event.preventDefault();
    
    // Clear existing timeout
    if (tapTimeoutRef.current) {
      clearTimeout(tapTimeoutRef.current);
    }

    const newTapCount = tapCount + 1;
    setTapCount(newTapCount);

    if (newTapCount === 2) {
      // Double tap detected
      setTapCount(0);
      toggleOriginal(paragraph.id);
    } else {
      // Single tap - wait to see if there's a second tap
      tapTimeoutRef.current = setTimeout(() => {
        setTapCount(0);
      }, 300); // 300ms window for double tap
    }
  };

  // Get font size classes
  const getFontSizeClass = () => {
    switch (preferences.fontSize) {
      case 'small': return 'text-sm md:text-base';
      case 'medium': return 'text-base md:text-lg';
      case 'large': return 'text-lg md:text-xl';
      case 'extra-large': return 'text-xl md:text-2xl';
      default: return 'text-base md:text-lg';
    }
  };

  // Get line height classes
  const getLineHeightClass = () => {
    switch (preferences.lineHeight) {
      case 'compact': return 'leading-normal';
      case 'normal': return 'leading-relaxed';
      case 'relaxed': return 'leading-loose';
      default: return 'leading-relaxed';
    }
  };

  // Get font family classes
  const getFontFamilyClass = () => {
    switch (preferences.fontFamily) {
      case 'serif': return 'font-serif';
      case 'sans-serif': return 'font-sans';
      case 'monospace': return 'font-mono';
      default: return 'font-sans';
    }
  };

  // Check if this paragraph has been rewritten (has mapping)
  const isRewritten = Boolean(mapping);
  
  // Get improvement types for styling
  const improvementTypes = mapping?.improvementTypes || [];
  
  const paragraphClasses = [
    'selectable-text p-4 rounded-lg transition-all duration-200',
    getFontSizeClass(),
    getLineHeightClass(),
    getFontFamilyClass(),
    'text-reading-text dark:text-reading-text-dark',
    
    // Rewritten paragraph styling
    ...(isRewritten && preferences.showOriginalIndicators
      ? [
          'bg-reading-original dark:bg-reading-original-dark',
          'border-l-4 border-reading-original-border dark:border-reading-original-border-dark',
          'tap-highlight cursor-pointer'
        ]
      : ['tap-highlight cursor-pointer']
    ),
    
    // Selected state
    ...(isSelected ? ['ring-2 ring-reading-accent dark:ring-reading-accent-dark'] : []),
    
    // Hover state for interactive paragraphs
    ...(isRewritten ? ['hover:bg-opacity-80 dark:hover:bg-opacity-80'] : []),
  ].join(' ');

  return (
    <div 
      className={paragraphClasses}
      data-paragraph-id={paragraph.id}
      onTouchEnd={handleTap}
      onClick={handleTap}
      style={{
        // Prevent text selection during double-tap
        WebkitUserSelect: tapCount > 0 ? 'none' : 'text',
        userSelect: tapCount > 0 ? 'none' : 'text',
      }}
    >
      {/* Improvement indicator */}
      {isRewritten && preferences.showOriginalIndicators && (
        <div className="flex items-center gap-2 mb-2 text-xs text-reading-text-muted dark:text-reading-text-muted-dark">
          <span className="inline-block w-2 h-2 rounded-full bg-reading-original-border dark:bg-reading-original-border-dark"></span>
          <span>
            AI Enhanced
            {improvementTypes.length > 0 && (
              <span className="ml-1">
                ({improvementTypes.map(type => 
                  type.charAt(0).toUpperCase() + type.slice(1)
                ).join(', ')})
              </span>
            )}
          </span>
          <span className="ml-auto text-xs opacity-60">Double-tap for original</span>
        </div>
      )}

      {/* Paragraph content */}
      <div className="leading-relaxed">
        {paragraph.content}
      </div>

      {/* Quality indicator */}
      {mapping && mapping.confidenceScore && (
        <div className="mt-2 flex items-center justify-end">
          <div className="text-xs text-reading-text-muted dark:text-reading-text-muted-dark opacity-60">
            Quality: {mapping.confidenceScore}/100
            {mapping.qualityMetrics.voicePreservationScore && (
              <span className="ml-2">
                Voice: {Math.round(mapping.qualityMetrics.voicePreservationScore)}/100
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}