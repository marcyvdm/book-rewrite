# AI Book Reader

A modern, mobile-first reading application that transforms books using AI to improve clarity and comprehension while preserving the author's voice and style. Features intelligent paragraph-level mapping that allows readers to double-tap any enhanced text to see the original version.

## 🚀 Features

### Reading Experience
- **Mobile-First Design**: Optimized for touch interactions and mobile reading
- **Double-Tap Original Access**: Tap any paragraph to see the original text and understand AI improvements
- **Progress Tracking**: Automatic reading progress saved with IndexedDB
- **Customizable Reading**: Adjustable font size, theme, and reading preferences
- **Smart Scrolling**: Automatic paragraph tracking and position restoration

### AI Enhancement
- **Voice Preservation**: Maintains author's unique tone, style, and personality
- **Intelligent Improvements**: Clarity enhancement, better flow, expanded explanations
- **Quality Metrics**: Transparency with confidence scores and improvement types
- **Paragraph Mapping**: 1:1, N:1, 1:N, and contextual paragraph relationships

### Technical Features
- **Offline-First**: Local storage with IndexedDB for reading progress
- **Modern Stack**: Astro + React + TypeScript + Tailwind CSS
- **Responsive**: Works seamlessly across devices
- **Performance**: Optimized loading and smooth interactions

## 📖 Project Structure

```
book-rewrite/
├── src/
│   ├── components/
│   │   ├── reader/           # Reading interface components
│   │   │   ├── BookReader.tsx
│   │   │   ├── ParagraphRenderer.tsx
│   │   │   ├── ReaderHeader.tsx
│   │   │   ├── ProgressBar.tsx
│   │   │   └── OriginalOverlay.tsx
│   │   ├── library/          # Library and book management
│   │   │   ├── LibraryView.tsx
│   │   │   ├── BookCard.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   ├── FilterTabs.tsx
│   │   │   └── EmptyState.tsx
│   │   └── ui/              # Shared UI components
│   ├── pages/
│   │   ├── index.astro      # Library homepage
│   │   └── reader/
│   │       └── [bookId].astro # Reading interface
│   ├── stores/
│   │   └── bookStore.ts     # Zustand state management
│   ├── types/
│   │   └── schema.ts        # TypeScript definitions
│   ├── utils/
│   │   ├── database.ts      # IndexedDB utilities
│   │   └── sampleData.ts    # Test data
│   └── layouts/
│       └── Layout.astro     # Base HTML layout
├── AI_REWRITING_FRAMEWORK.md # AI enhancement guidelines
├── CONVERSION_PROCEDURE.md   # Step-by-step conversion process
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd book-rewrite
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:4321`

### Development Commands

```bash
# Development
npm run dev          # Start dev server
npm run start        # Alias for dev

# Production
npm run build        # Build for production
npm run preview      # Preview production build

# Other
npm run astro --help # Astro CLI help
```

## 📚 AI Rewriting Framework

This project includes a comprehensive framework for converting books into AI-enhanced versions:

### Core Principles
- **Voice Preservation**: Maintain the author's unique style and tone
- **Clarity Enhancement**: Improve understanding without losing meaning
- **Intelligent Mapping**: Track every change for transparency
- **Quality Assurance**: Multi-layered validation and confidence scoring

### Conversion Process
1. **Content Ingestion**: Support for PDF, EPUB, TXT, copy-paste
2. **Multi-Agent Analysis**: Chapter-level and book-level understanding
3. **Strategic Planning**: Voice calibration and improvement prioritization  
4. **Paragraph Rewriting**: Context-aware enhancement with mapping
5. **Quality Assurance**: Validation and accuracy verification

### Enhancement Types
- **Clarity**: Simplify complex sentences and improve flow
- **Expansion**: Add context to underexplained concepts
- **Condensation**: Tighten verbose explanations  
- **Structure**: Improve logical progression and transitions
- **Examples**: Add concrete examples and analogies

## 🎨 Design System

### Color Scheme
- **Reading Colors**: Optimized for long reading sessions
- **Original Indicators**: Light green background for AI-enhanced paragraphs
- **Dark Mode**: Full dark theme support
- **Accessibility**: High contrast ratios throughout

### Typography
- **Inter**: Primary sans-serif font
- **Crimson Text**: Serif option for traditional reading
- **JetBrains Mono**: Monospace for technical content
- **Responsive Sizing**: Scales appropriately across devices

### Interactions
- **Double-Tap**: Show original text (300ms window)
- **Smooth Scrolling**: Touch-optimized scroll behavior
- **Haptic Feedback**: On supported devices
- **Progress Indication**: Visual reading progress

## 📱 Mobile Optimizations

### Touch Interactions
- **Double-Tap Detection**: Reliable paragraph-level original text access
- **Touch Callouts**: Disabled to prevent accidental selections
- **Scroll Restoration**: Maintains reading position across sessions
- **Gesture Support**: Native mobile gesture handling

### Performance
- **Code Splitting**: Lazy load reading components
- **Image Optimization**: Responsive images with proper sizing
- **Bundle Size**: Optimized dependencies and tree shaking
- **Caching**: Service worker for offline reading (future)

## 🔄 Data Schema

### Book Structure
```typescript
interface ProcessedBook {
  id: string;
  metadata: BookMetadata;           # Title, author, genre, etc.
  originalVersion: BookContent;     # Original text structure
  rewrittenVersion: BookContent;    # AI-enhanced version
  mappings: ParagraphMapping[];     # Original ↔ Rewritten relationships
  processingReport: ProcessingReport; # Conversion statistics
  qualityReport: QualityReport;     # Quality metrics and scores
}
```

### Reading Progress
```typescript
interface ReadingProgress {
  bookId: string;
  currentChapterId: string;
  currentParagraphId: string;
  scrollPosition: number;
  percentComplete: number;
  lastReadAt: string;
  bookmarks: Bookmark[];
  notes: Note[];
}
```

## 🎯 Usage Examples

### Adding Sample Data (Development)
```typescript
import { addSampleData } from '@/utils/sampleData';

// Add test books to IndexedDB
await addSampleData();
```

### Reading Interface
1. Navigate to library homepage
2. Select a book to start reading
3. Double-tap any paragraph to see original text
4. Use header controls to adjust font size and theme
5. Progress is automatically saved as you read

### Customization
- **Theme**: Light/Dark mode toggle in reader header
- **Font Size**: Adjustable from small to extra-large
- **Font Family**: System, serif, sans-serif, monospace options
- **Line Height**: Compact, normal, relaxed spacing
- **Indicators**: Toggle AI enhancement indicators

## 🧪 Testing & Development

### Sample Data
The project includes comprehensive sample data demonstrating:
- Multi-paragraph chapters with various improvement types
- Quality metrics and confidence scores
- Different mapping types (1:1, N:1, 1:N, contextual)
- Realistic reading progress and metadata

### Development Tools
- **TypeScript**: Full type safety throughout
- **ESLint**: Code quality and consistency
- **Hot Reload**: Instant feedback during development
- **Build Optimization**: Production-ready builds with Vite

## 🚀 Production Deployment

### Build for Production
```bash
npm run build
```

### Deployment Options
- **Static Sites**: Netlify, Vercel, GitHub Pages
- **CDN**: Any static file host
- **Docker**: Container-ready builds
- **Self-hosted**: Standard web server deployment

### Environment Variables
```bash
# Optional configurations
PUBLIC_APP_NAME="AI Book Reader"
PUBLIC_APP_VERSION="1.0.0"
```

## 📈 Future Enhancements

### Phase 2 Features
- [ ] **Book Upload Interface**: Direct PDF/EPUB upload and processing
- [ ] **AI Integration**: Live book conversion with Claude API
- [ ] **User Accounts**: Cloud sync and multi-device reading
- [ ] **Social Features**: Notes sharing and book recommendations
- [ ] **Analytics**: Reading statistics and insights

### Technical Improvements
- [ ] **Service Worker**: Offline reading capability
- [ ] **Web Streams**: Large book processing optimization
- [ ] **Virtual Scrolling**: Performance for very long books  
- [ ] **Text-to-Speech**: Audio reading with highlighting
- [ ] **Export Options**: PDF, EPUB, Kindle format export

### AI Enhancements
- [ ] **Real-time Processing**: Live paragraph enhancement
- [ ] **Multiple Versions**: Different enhancement styles per user
- [ ] **Learning System**: Improve based on user preferences
- [ ] **Custom Prompts**: User-defined enhancement instructions

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style
- Use TypeScript for all new code
- Follow existing naming conventions
- Add JSDoc comments for complex functions
- Ensure mobile-first responsive design
- Test on multiple devices and browsers

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Astro**: Modern web framework
- **React**: UI component library
- **Tailwind CSS**: Utility-first styling
- **Zustand**: Lightweight state management
- **Dexie**: IndexedDB wrapper for offline storage
- **TypeScript**: Type-safe development

---

**Happy Reading! 📚✨**

*Transform your reading experience with AI-enhanced clarity while preserving the author's authentic voice.*