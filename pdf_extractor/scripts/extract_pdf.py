#!/usr/bin/env python3
"""
CLI script for testing the PDF extractor
"""

import asyncio
import sys
import traceback
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pdf_extractor import IntelligentPDFExtractor, ExtractionConfig
from pdf_extractor.utils import setup_logging

console = Console(force_terminal=False, legacy_windows=True)


@click.command()
@click.argument('pdf_path', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output JSON file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose logging')
@click.option('--max-pages', type=int, help='Limit number of pages to process (for testing)')
@click.option('--no-images', is_flag=True, help='Skip image processing')
def main(pdf_path: Path, output: Optional[Path], verbose: bool, max_pages: Optional[int], no_images: bool):
    """
    Extract structured content from a PDF file using intelligent algorithms.
    
    This is a test CLI for the intelligent PDF extractor.
    """
    
    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    import platform
    simple_format = platform.system() == "Windows"
    logger = setup_logging(level=log_level, console_output=True, simple_format=simple_format)
    
    console.print(f"[bold green]Intelligent PDF Extractor v1.0.0[/bold green]")
    console.print(f"[dim]Processing: {pdf_path}[/dim]")
    
    # Configure extraction
    config = ExtractionConfig(
        enable_agent_enhancements=False,  # Disable for initial testing
        include_raw_image_data=not no_images,
        generate_confidence_scores=True,
        create_processing_report=True
    )
    
    if max_pages:
        console.print(f"[yellow]WARNING: Limiting processing to {max_pages} pages for testing[/yellow]")
    
    if no_images:
        console.print("[yellow]WARNING: Skipping image processing[/yellow]")
    
    # Run extraction
    try:
        result = asyncio.run(extract_pdf_async(pdf_path, config, logger, simple_format))
        
        # Determine output path
        if not output:
            output = pdf_path.with_suffix('.extracted.json')
        
        # Save results
        console.print(f"\n[bold cyan]Saving results to: {output}[/bold cyan]")
        result.save_to_file(output)
        
        # Display summary
        display_extraction_summary(result)
        
        # Display quality report
        display_quality_report(result)
        
        console.print(f"\n[bold green]SUCCESS: Extraction completed successfully![/bold green]")
        console.print(f"[dim]Results saved to: {output}[/dim]")
        
    except Exception as e:
        console.print(f"\n[bold red]ERROR: Extraction failed: {e}[/bold red]")
        if verbose:
            console.print(f"[red]{traceback.format_exc()}[/red]")
        sys.exit(1)


async def extract_pdf_async(pdf_path: Path, config: ExtractionConfig, logger, simple_format: bool = False) -> 'ExtractionResult':
    """Run PDF extraction asynchronously with progress display"""
    
    with Progress(
        TextColumn("{task.description}"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
        disable=simple_format,  # Disable progress on Windows to avoid encoding issues
    ) as progress:
        
        task = progress.add_task("Extracting PDF content...", total=None)
        
        # Create extractor
        extractor = IntelligentPDFExtractor(config)
        
        # Run extraction
        progress.update(task, description="[cyan]Analyzing PDF characteristics...")
        result = await extractor.extract(pdf_path)
        
        progress.update(task, description="[green]Extraction complete!")
        progress.stop()
    
    return result


def display_extraction_summary(result: 'ExtractionResult'):
    """Display extraction summary"""
    content = result.book_content
    report = result.processing_report
    
    console.print("\n[bold cyan]Extraction Summary[/bold cyan]")
    console.print("=" * 40)
    
    # Metadata
    console.print(f"Title: [bold]{content.metadata.title}[/bold]")
    console.print(f"Author: [bold]{content.metadata.author}[/bold]")
    console.print(f"Pages: {content.metadata.page_count}")
    console.print(f"Word Count: {content.metadata.word_count:,}")
    
    # Structure
    console.print(f"\n[yellow]Structure:[/yellow]")
    console.print(f"  Chapters: {len(content.chapters)}")
    console.print(f"  Paragraphs: {len(content.paragraphs)}")
    console.print(f"  Images: {len(content.images)}")
    console.print(f"  Citations: {len(content.citations)}")
    console.print(f"  TOC Entries: {len(content.table_of_contents)}")
    
    # Processing time
    processing_time = report.total_processing_time_ms / 1000
    console.print(f"\n[yellow]Performance:[/yellow]")
    console.print(f"  Processing Time: {processing_time:.2f} seconds")
    console.print(f"  Document Type: {report.pdf_profile.document_type}")
    console.print(f"  Text Quality: {report.pdf_profile.text_quality:.2%}")


def display_quality_report(result: 'ExtractionResult'):
    """Display quality assessment"""
    metrics = result.processing_report.quality_metrics
    
    console.print("\n[bold cyan]Quality Assessment[/bold cyan]")
    console.print("=" * 40)
    
    console.print(f"Overall Confidence: [bold green]{metrics.overall_confidence:.1%}[/bold green]")
    console.print(f"Structure Quality: {metrics.structure_confidence:.1%}")
    console.print(f"Content Quality: {metrics.content_confidence:.1%}")
    console.print(f"Image Quality: {metrics.image_confidence:.1%}")
    console.print(f"Citation Quality: {metrics.citation_confidence:.1%}")
    
    # Quality indicator
    if metrics.overall_confidence >= 0.9:
        console.print("\n[bold green]EXCELLENT: No enhancement needed![/bold green]")
    elif metrics.overall_confidence >= 0.8:
        console.print("\n[yellow]GOOD: Minor improvements possible[/yellow]")
    elif metrics.overall_confidence >= 0.7:
        console.print("\n[yellow]MODERATE: Enhancement recommended[/yellow]")
    else:
        console.print("\n[red]LOW QUALITY: Significant enhancement needed[/red]")
    
    # Chapter details
    if result.book_content.chapters:
        console.print("\n[yellow]Chapters detected:[/yellow]")
        for i, chapter in enumerate(result.book_content.chapters[:10]):  # Show first 10
            confidence_color = "green" if chapter.confidence > 0.8 else "yellow" if chapter.confidence > 0.6 else "red"
            console.print(f"  {chapter.number}. [{confidence_color}]{chapter.title}[/{confidence_color}] "
                         f"(Page {chapter.page_number}, {chapter.confidence:.1%} confidence)")
        
        if len(result.book_content.chapters) > 10:
            console.print(f"  ... and {len(result.book_content.chapters) - 10} more chapters")


if __name__ == "__main__":
    main()