#!/usr/bin/env python3
"""
Japanese Prompt Compression Demo

This script demonstrates the Japanese text compression capabilities of LLMLingua-JP.
"""

import time
from llmlingua import PromptCompressor


def demo_japanese_compression():
    """Demonstrate Japanese text compression."""
    
    print("🌸 LLMLingua-JP Japanese Compression Demo")
    print("=" * 50)
    
    # Initialize compressor
    print("Loading compressor...")
    compressor = PromptCompressor(device_map="cpu")
    
    # Sample Japanese text
    japanese_context = [
        "自然言語処理（Natural Language Processing、NLP）は、",
        "人間が日常的に使っている自然言語をコンピュータに処理させる一連の技術であり、",
        "人工知能と言語学の一分野である。",
        "自然言語処理の研究は、計算言語学（computational linguistics）と密接に関連しており、",
        "両者を合わせて計算言語学と呼ばれることもある。",
        "自然言語処理は、音声認識、機械翻訳、情報抽出、質問応答システム、",
        "テキスト要約、感情分析など、様々な応用分野がある。",
        "近年では、深層学習の発展により、自然言語処理の性能が大幅に向上している。",
        "特に、Transformerアーキテクチャに基づくモデルが多くのタスクで優れた性能を示している。"
    ]
    
    question = "自然言語処理とは何ですか？その応用分野について教えてください。"
    
    print(f"\n📝 Original Text ({len(japanese_context)} sentences):")
    for i, text in enumerate(japanese_context, 1):
        print(f"  {i}. {text}")
    
    print(f"\n❓ Question: {question}")
    
    # Test different compression rates
    rates = [0.8, 0.6, 0.4, 0.2]
    
    for rate in rates:
        print(f"\n🔧 Compressing with rate {rate}...")
        start_time = time.time()
        
        result = compressor.compress_prompt(
            context=japanese_context,
            question=question,
            rate=rate,
            lang="ja"
        )
        
        end_time = time.time()
        
        print(f"⏱️  Compression time: {end_time - start_time:.2f}s")
        print(f"📊 Original tokens: {result['origin_tokens']}")
        print(f"📊 Compressed tokens: {result['compressed_tokens']}")
        print(f"📊 Compression ratio: {result['ratio']}")
        print(f"💰 Estimated savings: {result['saving']}")
        
        print(f"\n📄 Compressed text:")
        print(f"  {result['compressed_prompt'][:200]}...")
        print("-" * 50)


def demo_auto_detection():
    """Demonstrate automatic language detection."""
    
    print("\n🌐 Language Auto-Detection Demo")
    print("=" * 50)
    
    compressor = PromptCompressor(device_map="cpu")
    
    # Mixed language text
    mixed_context = [
        "自然言語処理（Natural Language Processing）は、",
        "人間の言語をコンピュータで処理する技術です。",
        "Machine learning and deep learning are used.",
        "音声認識や機械翻訳などの応用があります。"
    ]
    
    print("📝 Mixed Language Text:")
    for text in mixed_context:
        print(f"  {text}")
    
    print("\n🔍 Testing auto-detection...")
    result = compressor.compress_prompt(
        context=mixed_context,
        rate=0.5,
        lang="auto"
    )
    
    print(f"📊 Result: {result['compressed_tokens']} tokens (from {result['origin_tokens']})")
    print(f"📄 Compressed: {result['compressed_prompt'][:150]}...")


def demo_performance_comparison():
    """Compare performance with and without Japanese processing."""
    
    print("\n⚡ Performance Comparison")
    print("=" * 50)
    
    compressor = PromptCompressor(device_map="cpu")
    
    # English text
    english_context = [
        "Natural Language Processing (NLP) is a field of artificial intelligence.",
        "It focuses on the interaction between computers and human language.",
        "Machine learning and deep learning techniques are widely used.",
        "Applications include speech recognition, machine translation, and text summarization."
    ]
    
    # Japanese text
    japanese_context = [
        "自然言語処理は人工知能の一分野です。",
        "コンピュータと人間の言語の相互作用に焦点を当てています。",
        "機械学習と深層学習の技術が広く使用されています。",
        "応用分野には音声認識、機械翻訳、テキスト要約などがあります。"
    ]
    
    print("🔤 English Text Processing:")
    start_time = time.time()
    en_result = compressor.compress_prompt(context=english_context, rate=0.5)
    en_time = time.time() - start_time
    
    print(f"  Time: {en_time:.2f}s")
    print(f"  Tokens: {en_result['compressed_tokens']}/{en_result['origin_tokens']}")
    
    print("\n🇯🇵 Japanese Text Processing:")
    start_time = time.time()
    jp_result = compressor.compress_prompt(context=japanese_context, rate=0.5, lang="ja")
    jp_time = time.time() - start_time
    
    print(f"  Time: {jp_time:.2f}s")
    print(f"  Tokens: {jp_result['compressed_tokens']}/{jp_result['origin_tokens']}")
    
    print(f"\n📈 Performance difference: {jp_time - en_time:.2f}s")


if __name__ == "__main__":
    try:
        demo_japanese_compression()
        demo_auto_detection()
        demo_performance_comparison()
        
        print("\n✅ Demo completed successfully!")
        print("\n💡 Tips:")
        print("  - Use lang='auto' for automatic language detection")
        print("  - Use lang='ja' for explicit Japanese processing")
        print("  - Adjust rate parameter to control compression level")
        print("  - Japanese tokenization preserves sentence structure")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("Make sure you have installed the required dependencies:")
        print("  pip install fugashi unidic-lite") 