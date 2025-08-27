import Dexie, { type EntityTable } from 'dexie';
import type { ProcessedBook, ReadingProgress, BookLibrary } from '../types/schema';

export class BookReaderDB extends Dexie {
  books!: EntityTable<ProcessedBook, 'id'>;
  progress!: EntityTable<ReadingProgress, 'bookId'>;
  libraries!: EntityTable<BookLibrary, 'userId'>;

  constructor() {
    super('BookReaderDB');
    
    this.version(1).stores({
      books: 'id, metadata.title, metadata.author, metadata.category, metadata.processingDate',
      progress: 'bookId, userId, lastReadAt, percentComplete',
      libraries: 'userId, lastUpdated'
    });
  }

  async addBook(book: ProcessedBook): Promise<void> {
    await this.books.put(book);
  }

  async getBook(id: string): Promise<ProcessedBook | undefined> {
    return await this.books.get(id);
  }

  async getAllBooks(): Promise<ProcessedBook[]> {
    return await this.books.toArray();
  }

  async updateReadingProgress(progress: ReadingProgress): Promise<void> {
    await this.progress.put(progress);
  }

  async getReadingProgress(bookId: string, userId: string = 'default'): Promise<ReadingProgress | undefined> {
    return await this.progress.get(bookId);
  }

  async getUserLibrary(userId: string = 'default'): Promise<BookLibrary | undefined> {
    return await this.libraries.get(userId);
  }

  async updateUserLibrary(library: BookLibrary): Promise<void> {
    await this.libraries.put(library);
  }

  async searchBooks(query: string): Promise<ProcessedBook[]> {
    const lowerQuery = query.toLowerCase();
    return await this.books
      .filter(book => 
        book.metadata.title.toLowerCase().includes(lowerQuery) ||
        book.metadata.author.toLowerCase().includes(lowerQuery)
      )
      .toArray();
  }

  async getBooksByCategory(category: string): Promise<ProcessedBook[]> {
    return await this.books
      .where('metadata.category')
      .equals(category)
      .toArray();
  }

  async deleteBook(id: string): Promise<void> {
    await this.books.delete(id);
    // Also delete associated progress
    await this.progress.where('bookId').equals(id).delete();
  }

  async clearAllData(): Promise<void> {
    await this.books.clear();
    await this.progress.clear();
    await this.libraries.clear();
  }
}

// Create singleton instance
export const db = new BookReaderDB();