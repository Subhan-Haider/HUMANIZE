"""
Smart Adaptive Humanization System
Automatically analyzes text and selects optimal strategies.
"""
import re
import nltk
from collections import Counter

class SmartHumanizationOrchestrator:
    """
    Intelligent system that analyzes text and applies optimal humanization.
    """
    
    def __init__(self, neural_humanizer):
        self.humanizer = neural_humanizer
        
    def analyze_text_type(self, text):
        """
        Analyze text to determine its characteristics and optimal strategy.
        
        Returns:
            dict with analysis results
        """
        sentences = nltk.sent_tokenize(text)
        words = text.split()
        
        # Calculate metrics
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Detect AI indicators
        ai_words = [
            'furthermore', 'moreover', 'additionally', 'consequently', 
            'therefore', 'thus', 'hence', 'notably', 'importantly'
        ]
        ai_word_count = sum(1 for word in words if word.lower() in ai_words)
        ai_density = ai_word_count / len(words) if words else 0
        
        # Detect formality
        formal_indicators = ['shall', 'ought', 'whereas', 'thereby', 'wherein']
        formal_count = sum(1 for word in words if word.lower() in formal_indicators)
        
        # Detect structure
        has_bullets = '•' in text or '\n-' in text or '\n*' in text
        has_numbers = bool(re.search(r'\n\d+\.', text))
        
        # Determine text type
        if ai_density > 0.02:
            text_type = "high_ai"
        elif formal_count > 2 or avg_sentence_length > 25:
            text_type = "formal_academic"
        elif has_bullets or has_numbers:
            text_type = "structured_list"
        elif avg_sentence_length < 15:
            text_type = "casual"
        else:
            text_type = "standard"
            
        return {
            "type": text_type,
            "ai_density": ai_density,
            "avg_sentence_length": avg_sentence_length,
            "formality": formal_count,
            "is_structured": has_bullets or has_numbers
        }
    
    def select_optimal_level(self, analysis):
        """
        Automatically select the best stealth level based on text analysis.
        """
        text_type = analysis["type"]
        ai_density = analysis["ai_density"]
        
        if text_type == "high_ai":
            # Very AI-heavy text needs aggressive humanization
            return 5
        elif text_type == "formal_academic":
            # Formal text needs careful processing
            return 4
        elif text_type == "structured_list":
            # Lists need restructuring
            return 3
        elif ai_density > 0.01:
            # Moderate AI detection
            return 4
        else:
            # Casual or already natural
            return 3
    
    def smart_humanize(self, text, max_iterations=3, target_improvement=0.3, tone="Balanced", audience="General", preserve_formatting=True, use_emojis=False):
        """
        Intelligently humanize text with adaptive strategy.
        
        Args:
            text: Input text
            max_iterations: Maximum number of iterations
            target_improvement: Stop when this much improvement is made
            tone: Desired writing style
            audience: Target readership
            preserve_formatting: Keep paragraphs locked
            use_emojis: Enable human-like emojis
            
        Returns:
            Humanized text with metadata
        """
        print("\n" + "="*70)
        print("🧠 SMART HUMANIZATION SYSTEM")
        print("="*70)
        
        # Analyze input
        print("\n📊 Analyzing input text...")
        analysis = self.analyze_text_type(text)
        
        print(f"   Text Type: {analysis['type']}")
        print(f"   AI Density: {analysis['ai_density']:.2%}")
        print(f"   Avg Sentence Length: {analysis['avg_sentence_length']:.1f} words")
        print(f"   Formality Level: {analysis['formality']}")
        
        # Select optimal level
        optimal_level = self.select_optimal_level(analysis)
        print(f"\n🎯 Recommended Stealth Level: {optimal_level}")
        
        # Apply humanization with iterations
        current_text = text
        iteration = 1
        
        while iteration <= max_iterations:
            print(f"\n{'='*70}")
            print(f"🔄 ITERATION {iteration}/{max_iterations}")
            print(f"{'='*70}")
            
            # Adjust level for iterations
            if iteration == 1:
                level = optimal_level
            else:
                # Reduce aggressiveness in later iterations
                level = max(3, optimal_level - (iteration - 1))
            
            print(f"Using Level: {level}, Tone: {tone}, Audience: {audience}, Preserve: {preserve_formatting}")
            
            # Humanize
            current_text = self.humanizer.humanize(
                current_text, 
                stealth_level=level,
                use_artifacts=(level >= 4),
                tone=tone,
                audience=audience,
                preserve_formatting=preserve_formatting,
                use_emojis=use_emojis
            )
            
            # Analyze improvement
            new_analysis = self.analyze_text_type(current_text)
            improvement = analysis['ai_density'] - new_analysis['ai_density']
            
            print(f"\n📈 Improvement: {improvement:.2%} reduction in AI density")
            
            # Check if we should continue
            if improvement >= target_improvement:
                print(f"✓ Target improvement reached!")
                break
            
            if iteration == max_iterations:
                print(f"⚠ Maximum iterations reached")
                
            iteration += 1
        
        # Final analysis
        final_analysis = self.analyze_text_type(current_text)
        
        print(f"\n" + "="*70)
        print("✅ SMART HUMANIZATION COMPLETE")
        print("="*70)
        print(f"Initial AI Density: {analysis['ai_density']:.2%}")
        print(f"Final AI Density: {final_analysis['ai_density']:.2%}")
        print(f"Total Improvement: {analysis['ai_density'] - final_analysis['ai_density']:.2%}")
        print(f"Iterations Used: {iteration}")
        print("="*70 + "\n")
        
        return {
            "text": current_text,
            "iterations": iteration,
            "initial_analysis": analysis,
            "final_analysis": final_analysis,
            "improvement": analysis['ai_density'] - final_analysis['ai_density']
        }
    
    def get_manual_editing_tips(self, analysis):
        """
        Provide specific tips for manual editing based on text analysis.
        """
        tips = []
        
        if analysis["type"] == "high_ai":
            tips.append("⚠ High AI content detected. YOU MUST manually edit this.")
            tips.append("→ Add personal examples or experiences")
            tips.append("→ Change at least 30% of sentences to your own words")
            
        if analysis["avg_sentence_length"] > 20:
            tips.append("→ Some sentences are too long. Break them up.")
            
        if analysis["formality"] > 3:
            tips.append("→ Text is very formal. Make it more conversational.")
            tips.append("→ Use contractions (it's, don't, can't)")
            
        if analysis["is_structured"]:
            tips.append("→ Lists detected. Convert to paragraph form.")
            
        tips.append("→ Add filler words: 'actually', 'basically', 'honestly'")
        tips.append("→ Start some sentences with 'And' or 'But'")
        tips.append("→ Add your personal opinion or reaction")
        
        return tips
