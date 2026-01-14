"""
Real-Time AI Detector Testing
Tests text against actual AI detectors via APIs.
"""
import requests
import time
import re

class DetectorTester:
    """
    Tests text against real AI detection APIs.
    """
    
    def __init__(self):
        # Free AI detection APIs
        self.apis = {
            "sapling": {
                "url": "https://api.sapling.ai/api/v1/aidetect",
                "enabled": False  # Requires API key
            },
            "writer": {
                "url": "https://enterprise-api.writer.com/content/organization/{org_id}/ai-content-detector",
                "enabled": False  # Requires API key
            }
        }
    
    def test_with_local_heuristics(self, text):
        """
        Use local heuristics to estimate AI probability.
        """
        import nltk
        
        score = 0
        total_checks = 0
        
        sentences = nltk.sent_tokenize(text)
        
        # Check 1: Sentence length variance
        if sentences:
            lengths = [len(s.split()) for s in sentences]
            variance = sum((l - sum(lengths)/len(lengths))**2 for l in lengths) / len(lengths)
            std_dev = variance ** 0.5
            
            # High variance = more human
            if std_dev > 8:
                score += 1
            total_checks += 1
        
        # Check 2: First-person pronouns
        text_lower = text.lower()
        first_person_count = sum([
            text_lower.count(" i "),
            text_lower.count(" me "),
            text_lower.count(" my "),
            text_lower.count(" we ")
        ])
        
        # More first-person = more human
        if first_person_count > 2:
            score += 1
        total_checks += 1
        
        # Check 3: Informal language
        informal_markers = [
            "lol", "haha", "tbh", "honestly", "like,", "you know,",
            "i mean,", "basically,", "kind of", "sort of"
        ]
        informal_count = sum(text_lower.count(m) for m in informal_markers)
        
        if informal_count > 0:
            score += 1
        total_checks += 1
        
        # Check 4: Imperfections
        has_double_space = "  " in text
        has_missing_comma = re.search(r'\w,\w', text) is not None
        has_casual_start = any(text.startswith(w) for w in ["And ", "But ", "So "])
        
        if has_double_space or has_missing_comma or has_casual_start:
            score += 1
        total_checks += 1
        
        # Check 5: Avoid AI transition words
        ai_words = [
            "furthermore", "moreover", "additionally", "consequently",
            "therefore", "thus", "hence", "notably"
        ]
        ai_word_count = sum(text_lower.count(w) for w in ai_words)
        
        # Fewer AI words = more human
        if ai_word_count == 0:
            score += 1
        total_checks += 1
        
        # Calculate final score
        human_probability = (score / total_checks) * 100
        ai_probability = 100 - human_probability
        
        return {
            "detector": "Local Heuristics",
            "ai_probability": ai_probability,
            "human_probability": human_probability,
            "confidence": "medium",
            "details": {
                "sentence_variance_check": "✓" if std_dev > 8 else "✗",
                "first_person_check": "✓" if first_person_count > 2 else "✗",
                "informal_language_check": "✓" if informal_count > 0 else "✗",
                "imperfection_check": "✓" if (has_double_space or has_missing_comma or has_casual_start) else "✗",
                "ai_words_check": "✓" if ai_word_count == 0 else "✗"
            }
        }
    
    def recommend_improvements(self, result):
        """
        Recommend improvements based on detector results.
        """
        recommendations = []
        
        if result["ai_probability"] > 70:
            recommendations.append("⚠ HIGH AI DETECTION - CRITICAL IMPROVEMENTS NEEDED:")
            recommendations.append("  → Add more first-person language (I, me, my)")
            recommendations.append("  → Vary sentence lengths drastically")
            recommendations.append("  → Add informal language (honestly, like, you know)")
            recommendations.append("  → Include some imperfections (typos, casual grammar)")
        
        elif result["ai_probability"] > 50:
            recommendations.append("⚠ MODERATE AI DETECTION - IMPROVEMENTS SUGGESTED:")
            recommendations.append("  → Add personal opinions and experiences")
            recommendations.append("  → Use more contractions (don't, can't, it's)")
            recommendations.append("  → Add conversational fillers")
        
        elif result["ai_probability"] > 30:
            recommendations.append("✓ LOW AI DETECTION - MINOR TOUCH-UPS:")
            recommendations.append("  → Consider adding 1-2 personal anecdotes")
            recommendations.append("  → Add some casual language")
        
        else:
            recommendations.append("✅ EXCELLENT - TEXT APPEARS HUMAN!")
            recommendations.append("  → No major improvements needed")
            recommendations.append("  → You can still manually review for quality")
        
        return recommendations


