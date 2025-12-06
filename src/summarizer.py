"""
Summarizer Module - Gemini-based bilingual summarization
总结模块 - 基于Gemini的双语总结
"""

import os
import json
import logging
import re
import google.generativeai as genai
from typing_extensions import TypedDict
from typing import Optional

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SCIENTISTS

logger = logging.getLogger(__name__)


class InterviewSummary(TypedDict):
    """Structured output schema for Gemini"""
    scientist_name: str
    scientist_org: str
    summary_en: str
    summary_cn: str
    key_points: list
    source_type: str


def configure_gemini():
    """Configure Gemini API"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False


def clean_json_response(text: str) -> str:
    """Clean markdown wrapping from JSON response"""
    text = text.strip()
    
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n", "", text)
        if text.endswith("```"):
            text = text[:-3].strip()
    
    return text


def summarize_content(item: dict) -> Optional[dict]:
    """
    Use Gemini to generate bilingual summary for content.
    使用Gemini生成双语总结
    """
    if not configure_gemini():
        logger.error("GEMINI_API_KEY not set")
        return None
    
    content = item.get('content', '')
    if not content:
        content = item.get('description', '')
    
    if not content or len(content) < 100:
        logger.warning(f"Insufficient content for: {item.get('title', 'Unknown')}")
        return None
    
    # Get scientist info
    matched_scientists = item.get('matched_scientists', [])
    scientist_name = matched_scientists[0] if matched_scientists else "Unknown"
    scientist_info = SCIENTISTS.get(scientist_name, {})
    
    # Truncate content if too long
    truncated_content = content[:80000]
    
    prompt = f"""You are an AI research analyst. Analyze the following content about AI expert "{scientist_name}" ({scientist_info.get('org', 'Unknown org')}).

Content Title: {item.get('title', 'Unknown')}
Content Source: {item.get('source_name', 'Unknown')}
Content Type: {item.get('source_type', 'Unknown')}

Content:
{truncated_content}

Generate a structured JSON summary with:
1. scientist_name: The main scientist discussed (use "{scientist_name}")
2. scientist_org: Their organization (use "{scientist_info.get('org', 'Unknown')}")
3. summary_en: Comprehensive English summary (300-500 words). Include key quotes if available.
4. summary_cn: Professional Chinese summary (300-500 字). Keep technical terms like "Transformer", "LLM", "Scaling Laws" in English.
5. key_points: List of 3-5 key takeaways in English
6. source_type: One of ["interview", "article", "podcast", "talk", "paper", "news"]

Focus on:
- What the scientist said or discussed
- Key insights, predictions, or announcements
- Technical details mentioned
- Industry implications
"""

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=InterviewSummary,
                temperature=0.3,
            )
        )
        
        raw_text = clean_json_response(response.text)
        result = json.loads(raw_text)
        
        # Merge with original item
        item.update(result)
        item['summarized'] = True
        
        logger.info(f"Successfully summarized: {item.get('title', 'Unknown')}")
        return item
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        if 'raw_text' in locals():
            logger.error(f"Raw text: {raw_text[:500]}")
    except Exception as e:
        logger.error(f"Summarization error for {item.get('title', 'Unknown')}: {e}")
    
    return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test with sample content
    test_item = {
        "title": "Test Interview with AI Expert",
        "content": "This is a test content about artificial intelligence and machine learning. The expert discussed various topics.",
        "source_name": "Test Source",
        "source_type": "interview",
        "matched_scientists": ["Demis Hassabis"],
    }
    
    result = summarize_content(test_item)
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))

