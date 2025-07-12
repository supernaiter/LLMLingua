"""
Integration tests for Japanese prompt compression.
"""

import pytest
from llmlingua import PromptCompressor


class TestJapaneseIntegration:
    """Integration tests for Japanese prompt compression."""
    
    @pytest.fixture
    def compressor(self):
        """Create a compressor instance for testing."""
        return PromptCompressor(device_map="cpu")
    
    def test_japanese_compression_basic(self, compressor):
        """Test basic Japanese text compression."""
        context = [
            "自然言語処理（Natural Language Processing）は、",
            "人間が日常的に使っている自然言語をコンピュータに処理させる一連の技術です。",
            "人工知能と言語学の一分野として位置づけられています。"
        ]
        
        result = compressor.compress_prompt(
            context=context,
            rate=0.5,
            lang="ja"
        )
        
        assert "compressed_prompt" in result
        assert result["compressed_tokens"] <= result["origin_tokens"]
        assert result["compressed_tokens"] > 0
        
        # Should preserve some Japanese content
        compressed = result["compressed_prompt"]
        assert any(ord(char) > 127 for char in compressed)
    
    def test_japanese_auto_detection(self, compressor):
        """Test automatic Japanese language detection."""
        jp_context = ["日本語のテキストです。", "機械学習を活用します。"]
        en_context = ["This is English text.", "Machine learning is used."]
        
        # Japanese should be detected
        jp_result = compressor.compress_prompt(
            context=jp_context,
            rate=0.5,
            lang="auto"
        )
        
        # English should not trigger Japanese processing
        en_result = compressor.compress_prompt(
            context=en_context,
            rate=0.5,
            lang="auto"
        )
        
        assert jp_result["compressed_tokens"] <= jp_result["origin_tokens"]
        assert en_result["compressed_tokens"] <= en_result["origin_tokens"]
    
    def test_japanese_with_question(self, compressor):
        """Test Japanese compression with question."""
        context = [
            "東京は日本の首都です。",
            "人口は約1400万人です。",
            "多くの企業の本社があります。"
        ]
        question = "東京について教えてください。"
        
        result = compressor.compress_prompt(
            context=context,
            question=question,
            rate=0.5,
            lang="ja"
        )
        
        assert "compressed_prompt" in result
        assert result["compressed_tokens"] <= result["origin_tokens"]
    
    def test_japanese_compression_ratio_control(self, compressor):
        """Test Japanese compression ratio control."""
        context = [
            "自然言語処理は、人間の言語をコンピュータで処理する技術です。",
            "機械学習、特に深層学習の発展により、性能が大幅に向上しました。",
            "音声認識、機械翻訳、情報抽出など、様々な応用分野があります。"
        ]
        
        # High compression rate
        high_result = compressor.compress_prompt(
            context=context,
            rate=0.3,
            lang="ja"
        )
        
        # Low compression rate
        low_result = compressor.compress_prompt(
            context=context,
            rate=0.8,
            lang="ja"
        )
        
        # High compression should result in fewer tokens
        high_ratio = high_result["compressed_tokens"] / high_result["origin_tokens"]
        low_ratio = low_result["compressed_tokens"] / low_result["origin_tokens"]
        
        assert high_ratio <= low_ratio
    
    def test_japanese_backward_compatibility(self, compressor):
        """Test that Japanese support doesn't break English functionality."""
        en_context = ["This is English text for testing.", "It should work normally."]
        
        # Should work with default settings (no lang parameter)
        result = compressor.compress_prompt(
            context=en_context,
            rate=0.5
        )
        
        assert "compressed_prompt" in result
        assert result["compressed_tokens"] <= result["origin_tokens"]
        
        # Should work with explicit English
        result_explicit = compressor.compress_prompt(
            context=en_context,
            rate=0.5,
            lang="auto"  # Should detect as English
        )
        
        assert "compressed_prompt" in result_explicit
        assert result_explicit["compressed_tokens"] <= result_explicit["origin_tokens"]


@pytest.mark.benchmark
class TestJapanesePerformance:
    """Performance tests for Japanese compression."""
    
    def test_japanese_tokenization_speed(self, benchmark):
        """Benchmark Japanese tokenization speed."""
        from llmlingua.tokenizer_jp import tokenize_jp
        
        text = "自然言語処理は人工知能の一分野であり、機械学習と深層学習を活用して人間の言語をコンピュータで処理する技術です。"
        
        result = benchmark(tokenize_jp, text)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_japanese_detection_speed(self, benchmark):
        """Benchmark Japanese text detection speed."""
        from llmlingua.tokenizer_jp import is_japanese_text
        
        text = "Hello 世界！This is a mixed text with Japanese characters."
        
        result = benchmark(is_japanese_text, text)
        assert isinstance(result, bool) 