from setuptools import setup, find_packages

setup(
    name="intelligent-pdf-extractor",
    version="1.0.0",
    description="Intelligent PDF extraction with multi-algorithm consensus and AI enhancement",
    author="Book Rewrite Project",
    packages=find_packages(),
    install_requires=[
        "pdfplumber>=0.10.0",
        "PyPDF2>=3.0.1", 
        "pdfminer.six>=20231228",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
        "nltk>=3.8.1",
        "textstat>=0.7.3",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "tqdm>=4.66.0",
        "structlog>=23.2.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0", 
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "isort>=5.13.0",
            "mypy>=1.8.0",
            "flake8>=7.0.0",
        ],
        "ocr": [
            "opencv-python>=4.8.0",
            "scikit-image>=0.22.0",
        ],
        "fast": [
            "pymupdf>=1.23.0",  # Note: AGPL license
        ]
    },
    entry_points={
        "console_scripts": [
            "extract-pdf=pdf_extractor.scripts.extract_pdf:main",
        ],
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)