"""
Tests for Japanese prompt compression functionality.
"""

import pytest

from llmlingua import PromptCompressor


class TestJapanesePromptCompression:
    """Test cases for Japanese prompt compression."""

    def test_japanese_detection_auto(self):
        """Test automatic Japanese text detection."""
        compressor = PromptCompressor(device_map="cpu")

        # Japanese text
        jp_context = [
            "自然言語処理は人工知能の一分野です。",
            "機械学習と深層学習を活用します。",
        ]
        jp_question = "自然言語処理とは何ですか？"

        result = compressor.compress_prompt(
            context=jp_context, question=jp_question, rate=0.5, lang="auto"
        )

        assert "compressed_prompt" in result
        assert "origin_tokens" in result
        assert "compressed_tokens" in result
        assert result["compressed_tokens"] <= result["origin_tokens"]

    def test_japanese_explicit_lang(self):
        """Test explicit Japanese language setting."""
        compressor = PromptCompressor(device_map="cpu")

        jp_context = ["私は学生です。", "大学で勉強しています。"]
        jp_question = "あなたは何をしていますか？"

        result = compressor.compress_prompt(
            context=jp_context, question=jp_question, rate=0.5, lang="ja"
        )

        assert "compressed_prompt" in result
        assert result["compressed_tokens"] <= result["origin_tokens"]

    def test_mixed_japanese_english(self):
        """Test mixed Japanese and English text."""
        compressor = PromptCompressor(device_map="cpu")

        mixed_context = [
            "自然言語処理（Natural Language Processing）は、",
            "人間の言語をコンピュータで処理する技術です。",
            "Machine learning and deep learning are used.",
        ]
        mixed_question = "What is NLP?"

        result = compressor.compress_prompt(
            context=mixed_context, question=mixed_question, rate=0.5, lang="auto"
        )

        assert "compressed_prompt" in result
        assert result["compressed_tokens"] <= result["origin_tokens"]

    def test_japanese_tokenization_preservation(self):
        """Test that Japanese tokenization preserves meaning."""
        compressor = PromptCompressor(device_map="cpu")

        jp_text = "美しい桜の花が咲いています。"

        result = compressor.compress_prompt(
            context=[jp_text], rate=0.8, lang="ja"  # High rate to preserve more content
        )

        compressed = result["compressed_prompt"]
        # Should contain some Japanese characters
        assert any(ord(char) > 127 for char in compressed)

    def test_japanese_compression_ratio(self):
        """Test Japanese compression ratio."""
        compressor = PromptCompressor(device_map="cpu")

        jp_context = [
            "自然言語処理は、人間が日常的に使っている自然言語を",
            "コンピュータに処理させる一連の技術であり、",
            "人工知能と言語学の一分野である。",
            "機械学習、特に深層学習の発展により、",
            "自然言語処理の性能は大幅に向上した。",
        ]

        result = compressor.compress_prompt(context=jp_context, rate=0.5, lang="ja")

        # Check compression ratio
        ratio = result["compressed_tokens"] / result["origin_tokens"]
        assert ratio <= 0.6  # Should be compressed (allow some tolerance)

    def test_japanese_with_instruction(self):
        """Test Japanese compression with instruction."""
        compressor = PromptCompressor(device_map="cpu")

        instruction = "以下の文章を要約してください："
        jp_context = ["今日は良い天気です。", "公園で散歩をしました。"]

        result = compressor.compress_prompt(
            context=jp_context, instruction=instruction, rate=0.5, lang="ja"
        )

        assert "compressed_prompt" in result
        assert result["compressed_tokens"] <= result["origin_tokens"]


@pytest.mark.integration
class TestJapaneseCompressionIntegration:
    """Integration tests for Japanese compression."""

    def test_long_japanese_text(self):
        """Test compression of longer Japanese text."""
        compressor = PromptCompressor(device_map="cpu")

        long_jp_text = [
            "自然言語処理（しぜんげんごしょり、英語: natural language processing、略称: NLP）は、",
            "人間が日常的に使っている自然言語をコンピュータに処理させる一連の技術であり、",
            "人工知能と言語学の一分野である。",
            "自然言語処理の研究は、計算言語学（computational linguistics）と密接に関連しており、",
            "両者を合わせて計算言語学と呼ばれることもある。",
            "自然言語処理は、音声認識、機械翻訳、情報抽出、質問応答システム、",
            "テキスト要約、感情分析など、様々な応用分野がある。",
        ]

        result = compressor.compress_prompt(
            context=long_jp_text, rate=0.3, lang="ja"  # More aggressive compression
        )

        assert result["compressed_tokens"] < result["origin_tokens"]
        assert result["compressed_tokens"] / result["origin_tokens"] <= 0.4

    def test_japanese_special_characters(self):
        """Test handling of Japanese special characters."""
        compressor = PromptCompressor(device_map="cpu")

        special_chars_text = [
            "「引用」や（括弧）など、様々な記号を含むテキスト。",
            "カタカナ：アイウエオ、ひらがな：あいうえお",
            "漢字：自然言語処理、数字：12345",
        ]

        result = compressor.compress_prompt(
            context=special_chars_text, rate=0.5, lang="ja"
        )

        assert "compressed_prompt" in result
        # Should preserve some special characters
        compressed = result["compressed_prompt"]
        assert len(compressed) > 0
