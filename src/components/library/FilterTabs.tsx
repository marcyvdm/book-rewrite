import React from 'react';

interface FilterTabsProps {
  categories: string[];
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

export function FilterTabs({ categories, selectedCategory, onCategoryChange }: FilterTabsProps) {
  const getCategoryLabel = (category: string) => {
    const labels = {
      all: 'All Books',
      business: 'Business',
      academic: 'Academic', 
      biography: 'Biography',
      science: 'Science',
      'self-help': 'Self Help',
      technical: 'Technical',
      other: 'Other'
    };
    return labels[category as keyof typeof labels] || category.charAt(0).toUpperCase() + category.slice(1);
  };

  return (
    <div className="flex items-center space-x-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-1 overflow-x-auto">
      {categories.map((category) => (
        <button
          key={category}
          onClick={() => onCategoryChange(category)}
          className={`
            px-3 py-1.5 text-sm font-medium rounded-md transition-all whitespace-nowrap
            ${selectedCategory === category
              ? 'bg-white dark:bg-gray-700 text-reading-text dark:text-reading-text-dark shadow-sm'
              : 'text-reading-text-muted dark:text-reading-text-muted-dark hover:text-reading-text dark:hover:text-reading-text-dark hover:bg-gray-200 dark:hover:bg-gray-700'
            }
          `}
        >
          {getCategoryLabel(category)}
        </button>
      ))}
    </div>
  );
}