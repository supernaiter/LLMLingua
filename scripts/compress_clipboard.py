#!/usr/bin/env python3
"""
CLI script to compress text from clipboard using LLMLingua.
"""

import argparse
import sys
from typing import Optional

try:
    import pyperclip
except ImportError:
    print("Error: pyperclip is required. Install with: pip install pyperclip")
    sys.exit(1)

try:
    from llmlingua import PromptCompressor
except ImportError:
    print("Error: llmlingua is required. Install with: pip install .")
    sys.exit(1)


def compress_clipboard_text(
    ratio: float = 0.5,
    target_model: str = "microsoft/DialoGPT-medium",
    device: str = "cpu",
    max_length: Optional[int] = None,
) -> None:
    """
    Compress text from clipboard and copy result back to clipboard.
    
    Args:
        ratio: Compression ratio (0.0 to 1.0)
        target_model: Target model for compression
        device: Device to use ('cpu' or 'cuda')
        max_length: Maximum length of compressed text
    """
    try:
        # Get text from clipboard
        text = pyperclip.paste()
        if not text.strip():
            print("Error: No text found in clipboard")
            return
        
        print(f"Original text length: {len(text)} characters")
        print(f"Compressing with ratio: {ratio}")
        
        # Initialize compressor
        compressor = PromptCompressor(
            model_name=target_model,
            device=device,
        )
        
        # Compress text
        compressed_text = compressor.compress_prompt(
            text,
            ratio=ratio,
            max_length=max_length,
        )
        
        # Copy result to clipboard
        pyperclip.copy(compressed_text)
        
        print(f"Compressed text length: {len(compressed_text)} characters")
        print(f"Compression ratio achieved: {len(compressed_text)/len(text):.2f}")
        print("Compressed text copied to clipboard!")
        
    except Exception as e:
        print(f"Error during compression: {e}")
        sys.exit(1)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Compress text from clipboard using LLMLingua"
    )
    parser.add_argument(
        "--ratio",
        type=float,
        default=0.5,
        help="Compression ratio (0.0 to 1.0, default: 0.5)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="microsoft/DialoGPT-medium",
        help="Target model for compression (default: microsoft/DialoGPT-medium)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "cuda"],
        help="Device to use (default: cpu)"
    )
    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum length of compressed text"
    )
    
    args = parser.parse_args()
    
    # Validate ratio
    if not 0.0 <= args.ratio <= 1.0:
        print("Error: ratio must be between 0.0 and 1.0")
        sys.exit(1)
    
    compress_clipboard_text(
        ratio=args.ratio,
        target_model=args.model,
        device=args.device,
        max_length=args.max_length,
    )


if __name__ == "__main__":
    main() 