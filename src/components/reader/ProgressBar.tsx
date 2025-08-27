import React from 'react';

interface ProgressBarProps {
  progress: number; // 0-100
  isVisible: boolean;
}

export function ProgressBar({ progress, isVisible }: ProgressBarProps) {
  return (
    <div 
      className={`
        h-1 bg-gray-200 dark:bg-gray-700 relative overflow-hidden
        transition-all duration-300
        ${isVisible ? 'opacity-100' : 'opacity-0'}
      `}
    >
      <div
        className="h-full bg-gradient-to-r from-reading-accent to-reading-accent-dark dark:from-reading-accent-dark dark:to-reading-accent transition-all duration-500 ease-out"
        style={{ width: `${Math.max(0, Math.min(100, progress))}%` }}
      />
      
      {/* Animated shimmer effect while reading */}
      <div className="absolute top-0 left-0 h-full w-full">
        <div 
          className="h-full bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse-slow"
          style={{ 
            width: '20%',
            transform: `translateX(${(progress / 100) * 400 - 20}%)`,
            transition: 'transform 1s ease-out'
          }}
        />
      </div>
    </div>
  );
}