import type { ProcessedBook } from '../types/schema';
import { db } from './database';

/**
 * Load a processed book JSON file into the reading application
 */
export async function loadProcessedBookFromFile(filePath: string): Promise<void> {
  try {
    console.log(`Loading processed book from: ${filePath}`);
    
    // In a browser environment, we'd use fetch or file input
    // For now, this is a utility function for development
    const response = await fetch(filePath);
    if (!response.ok) {
      throw new Error(`Failed to load book file: ${response.status}`);
    }
    
    const bookData: ProcessedBook = await response.json();
    
    // Validate the book data structure
    if (!isValidProcessedBook(bookData)) {
      throw new Error('Invalid book data structure');
    }
    
    // Add to database
    await db.addBook(bookData);
    
    console.log(`✅ Successfully loaded: ${bookData.metadata.title} by ${bookData.metadata.author}`);
    console.log(`📊 Stats: ${bookData.originalVersion.paragraphs.length} paragraphs, ${bookData.mappings.length} mappings`);
    
  } catch (error) {
    console.error('❌ Error loading processed book:', error);
    throw error;
  }
}

/**
 * Load processed books from the processed-books directory
 */
export async function loadProcessedBooksFromDirectory(directory: string = 'processed-books'): Promise<void> {
  try {
    // In a browser environment, we'd need to fetch a list of available books
    // For now, this is a placeholder for the loading mechanism
    console.log(`Looking for processed books in: ${directory}`);
    
    // This would be implemented to scan for available JSON files
    // and load them into the database
    console.log("📚 No processed books found. Use the /process-book command to create some.");
    
  } catch (error) {
    console.error("❌ Error loading processed books:", error);
    throw error;
  }
}

/**
 * Basic validation for ProcessedBook structure
 */
function isValidProcessedBook(book: any): book is ProcessedBook {
  return (
    book &&
    typeof book.id === 'string' &&
    book.metadata &&
    book.originalVersion &&
    book.rewrittenVersion &&
    Array.isArray(book.mappings) &&
    book.processingReport &&
    book.qualityReport
  );
}

// Auto-load functionality moved to enhancedChapterLoader.ts