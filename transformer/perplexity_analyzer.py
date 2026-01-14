"""
Perplexity-Based Quality Analyzer
Measures how "AI-like" text is and iterates until it's human-like.
"""
import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import numpy as np

class PerplexityAnalyzer:
    """
    Analyzes text perplexity to detect AI patterns.
    Lower perplexity = More AI-like (too predictable)
    Higher perplexity = More human-like (less predictable)
    """
    
    def __init__(self):
        print("Loading GPT-2 for perplexity analysis...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = GPT2LMHeadModel.from_pretrained('gpt2').to(self.device)
        self.tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
        self.model.eval()
        print("✓ Perplexity analyzer ready")
        
    def calculate_perplexity(self, text):
        """
        Calculate perplexity of text.
        
        Returns:
            float: Perplexity score (higher = more human-like)
        """
        encodings = self.tokenizer(text, return_tensors='pt')
        
        max_length = self.model.config.n_positions
        stride = 512
        
        lls = []
        for i in range(0, encodings.input_ids.size(1), stride):
            begin_loc = max(i + stride - max_length, 0)
            end_loc = min(i + stride, encodings.input_ids.size(1))
            trg_len = end_loc - i
            
            input_ids = encodings.input_ids[:, begin_loc:end_loc].to(self.device)
            target_ids = input_ids.clone()
            target_ids[:, :-trg_len] = -100
            
            with torch.no_grad():
                outputs = self.model(input_ids, labels=target_ids)
                log_likelihood = outputs.loss * trg_len
                
            lls.append(log_likelihood)
            
        ppl = torch.exp(torch.stack(lls).sum() / end_loc)
        return ppl.item()
    
    def analyze_text_quality(self, text):
        """
        Comprehensive text quality analysis.
        
        Returns:
            dict with quality metrics
        """
        perplexity = self.calculate_perplexity(text)
        
        # Interpret perplexity
        if perplexity < 30:
            quality = "Very AI-like (too predictable)"
            human_score = 0.1
        elif perplexity < 50:
            quality = "AI-like"
            human_score = 0.3
        elif perplexity < 80:
            quality = "Mixed"
            human_score = 0.5
        elif perplexity < 120:
            quality = "Human-like"
            human_score = 0.7
        else:
            quality = "Very human-like"
            human_score = 0.9
            
        return {
            "perplexity": perplexity,
            "quality": quality,
            "human_score": human_score,
            "recommendation": self._get_recommendation(perplexity)
        }
    
    def _get_recommendation(self, perplexity):
        """Get recommendation based on perplexity."""
        if perplexity < 50:
            return "Text is too predictable. Add more variation and imperfections."
        elif perplexity < 80:
            return "Good progress. Add more personal voice and casual language."
        else:
            return "Excellent! Text has human-like unpredictability."


class IterativeHumanizer:
    """
    Iteratively improves text until perplexity targets are met.
    """
    
    def __init__(self, humanizer, analyzer):
        self.humanizer = humanizer
        self.analyzer = analyzer
        
    def iterative_humanize(self, text, target_perplexity=80, max_iterations=5, tone="Balanced", audience="General", preserve_formatting=True, use_emojis=False):
        """
        Keep humanizing until perplexity target is reached.
        
        Args:
            text: Input text
            target_perplexity: Target perplexity (80 = human-like)
            max_iterations: Maximum iterations
            tone: Desired writing style
            audience: Target readership
            preserve_formatting: Keep paragraphs locked
            use_emojis: Enable human-like emojis
            
        Returns:
            dict with final text and metrics
        """
        print(f"\n{'='*70}")
        print(f"🔄 ITERATIVE HUMANIZATION (Target Perplexity: {target_perplexity})")
        print(f"Mode: {tone} | Audience: {audience} | Preserve: {preserve_formatting}")
        print(f"{'='*70}")
        
        current_text = text
        history = []
        
        for iteration in range(1, max_iterations + 1):
            print(f"\n--- Iteration {iteration}/{max_iterations} ---")
            
            # Analyze current state
            analysis = self.analyzer.analyze_text_quality(current_text)
            print(f"Perplexity: {analysis['perplexity']:.2f}")
            print(f"Quality: {analysis['quality']}")
            print(f"Human Score: {analysis['human_score']:.1%}")
            
            history.append({
                "iteration": iteration,
                "perplexity": analysis['perplexity'],
                "text_length": len(current_text)
            })
            
            # Check if target reached
            if analysis['perplexity'] >= target_perplexity:
                print(f"\n✓ Target perplexity reached!")
                break
                
            # Determine level based on current perplexity
            if analysis['perplexity'] < 40:
                level = 5  # Very aggressive
            elif analysis['perplexity'] < 60:
                level = 4
            else:
                level = 3
                
            print(f"→ Applying humanization (Level {level})...")
            
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
            
        # Final analysis
        final_analysis = self.analyzer.analyze_text_quality(current_text)
        
        print(f"\n{'='*70}")
        print(f"✅ ITERATIVE HUMANIZATION COMPLETE")
        print(f"{'='*70}")
        print(f"Initial Perplexity: {history[0]['perplexity']:.2f}")
        print(f"Final Perplexity: {final_analysis['perplexity']:.2f}")
        print(f"Improvement: +{final_analysis['perplexity'] - history[0]['perplexity']:.2f}")
        print(f"Quality: {final_analysis['quality']}")
        print(f"Iterations: {len(history)}")
        print(f"{'='*70}\n")
        
        return {
            "text": current_text,
            "initial_perplexity": history[0]['perplexity'],
            "final_perplexity": final_analysis['perplexity'],
            "improvement": final_analysis['perplexity'] - history[0]['perplexity'],
            "quality": final_analysis['quality'],
            "human_score": final_analysis['human_score'],
            "iterations": len(history),
            "history": history
        }
