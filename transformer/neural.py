import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import random
import re
import requests
import json
import time
from .vocabulary import vocab_enhancer
from .pattern_breaker import PatternBreaker, NgramDiversifier
from .fingerprint_scrambler import FingerprintScrambler, SemanticShuffler
from .ensemble_humanizer import EnsembleHumanizer, MarkovTextBlender

import os

class NeuralTextHumanizer:
    """
    Uses OpenRouter API (LLM) + Heuristic/Rule-based passes to humanize text.
    Follows a multi-pass architecture to bypass AI detection.
    """
    def __init__(self, model_name="Vamsi/T5_Paraphrase_Paws", device=None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Initializing NeuralTextHumanizer on {self.device}...")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)
        except Exception as e:
            print(f"Warning: Local model failed to load: {e}. Using API-only mode.")
            self.tokenizer = None
            self.model = None

        # Load external resources
        self.pattern_breaker = PatternBreaker()
        self.diversifier = NgramDiversifier()
        self.fingerprint_scrambler = FingerprintScrambler()
        self.semantic_shuffler = SemanticShuffler()
        self.ensemble = EnsembleHumanizer() # Keep ensemble if it's used elsewhere
        self.blender = MarkovTextBlender()
        
        # Ghost Protocol v17000.0 Resources
        self.common_words_set = self._load_google_10k()
        self.rare_vocab_set = self._load_rare_vocab()

    def _load_google_10k(self):
        try:
            path = "C:\\Users\\setup\\Pictures\\AI-Text-Humanizer-App-main\\google_10000.txt"
            with open(path, 'r', encoding='utf-8') as f:
                return set([line.strip().lower() for line in f if line.strip()])
        except:
            return set()

    def _load_rare_vocab(self):
        try:
            path = "C:\\Users\\setup\\Pictures\\AI-Text-Humanizer-App-main\\transformer\\rare_vocab.txt"
            with open(path, 'r', encoding='utf-8') as f:
                return set([line.strip().lower() for line in f if line.strip()])
        except:
            return set()

    def humanize(self, text, stealth_level=3, use_artifacts=False, tone="Balanced", audience="General", preserve_formatting=True, use_emojis=False):
        """
        FINAL HUMANIZATION ENGINE
        Multi-pass system to completely bypass AI detection.
        """
        if not text: 
            return ""

        # Recursive Paragraph Handling
        if preserve_formatting and "\n" in text:
            print("→ Mode: Preserve Structure (Processing paragraphs individually)")
            paragraphs = text.split("\n")
            humanized_paras = []
            for p in paragraphs:
                if p.strip():
                    humanized_paras.append(self.humanize(p, stealth_level, use_artifacts, tone, audience, preserve_formatting=False, use_emojis=use_emojis))
                else:
                    humanized_paras.append("") # Keep empty lines
            return "\n".join(humanized_paras)

        print(f"\n{'='*60}")
        print(f"HUMANIZATION ENGINE - Level {stealth_level} - Tone: {tone}")
        print(f"Features: Preserve={preserve_formatting}, Emojis={use_emojis}")
        print(f"{'='*60}")
        print(f"Input length: {len(text)} chars")

        # Ensure NLTK
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)

        # Pass 0: Strip AI Voice (Level 3+)
        if stealth_level >= 3:
            print("→ Running Pass 0: Obfuscate Intent...")
            try:
                text = self._pass_0_obfuscate_intent(text)
                print(f"  ✓ Pass 0 complete ({len(text)} chars)")
            except Exception as e:
                print(f"  ✗ Pass 0 failed: {e}")

        # Pass 1: De-structure
        print("→ Running Pass 1: De-structure...")
        try:
            text = self._pass_1_destructure(text)
            print(f"  ✓ Pass 1 complete ({len(text)} chars)")
        except Exception as e:
            print(f"  ✗ Pass 1 failed: {e}")
        
        # Pass 2: Semantic Rebuild (LLM for Level 5, else T5)
        if stealth_level >= 2:
            print(f"→ Running Pass 2: Semantic Rebuild (Level {stealth_level})...")
            try:
                if stealth_level >= 5 or tone != "Balanced":
                    print(f"  using OpenRouter LLM (Tone: {tone})...")
                    text = self._pass_2_semantic_rebuild_llm(text, level=stealth_level, tone=tone, audience=audience)
                elif self.model:
                    print("  using T5 Paraphraser...")
                    text = self._pass_2_semantic_rebuild_t5(text, temperature=1.2)
                
                # Add human-like Markov blending (Level 4+)
                if stealth_level >= 4:
                    print("  applying human-like Markov blending...")
                    text = self.blender.blend_with_corpus(text)
                    
                print(f"  ✓ Pass 2 complete ({len(text)} chars)")
            except Exception as e:
                print(f"  ✗ Pass 2 failed: {e}")
        else:
            print("→ Pass 2: SKIPPED (Stealth Level < 2)")
        
        # Pass 2.5: Anti-Paraphrasing Detection (NEW)
        if stealth_level >= 3:
            print("→ Running Pass 2.5: Anti-Paraphrasing...")
            try:
                text = self._pass_2_5_anti_paraphrasing(text, level=stealth_level)
                print(f"  ✓ Pass 2.5 complete ({len(text)} chars)")
            except Exception as e:
                print(f"  ✗ Pass 2.5 failed: {e}")
        
        # Pass 3: Opinion & Confidence
        print("→ Running Pass 3: Opinion & Confidence...")
        try:
            text = self._pass_3_opinion_and_confidence(text, level=stealth_level)
            print(f"  ✓ Pass 3 complete ({len(text)} chars)")
        except Exception as e:
            print(f"  ✗ Pass 3 failed: {e}")
            
        # Pass 4: Imperfections
        print("→ Running Pass 4: Imperfections...")
        try:
            text = self._pass_4_imperfection(text, level=stealth_level)
            print(f"  ✓ Pass 4 complete ({len(text)} chars)")
        except Exception as e:
            print(f"  ✗ Pass 4 failed: {e}")
            
        # Pass 5: Rhythm Control
        print("→ Running Pass 5: Rhythm Control...")
        try:
            text = self._pass_5_rhythm(text, level=stealth_level)
            print(f"  ✓ Pass 5 complete ({len(text)} chars)")
        except Exception as e:
            print(f"  ✗ Pass 5 failed: {e}")
        
        # Pass 6: Pattern Breaking (Subtle noise)
        if stealth_level >= 3:
            print("→ Running Pass 6: Pattern Breaking...")
            try:
                text = self.pattern_breaker.comprehensive_pattern_break(text, aggressiveness=stealth_level)
                print(f"  ✓ Pass 6 complete")
            except Exception as e:
                print(f"  ✗ Pass 6 failed: {e}")
        
        # Pass 7: Fingerprint Scrambling & Semantic Shuffling (ANTI-SIMILARITY)
        if stealth_level >= 4:
            print("→ Running Pass 7: Fingerprint Scrambling...")
            try:
                text = self.semantic_shuffler.semantic_shuffle(text, aggressiveness=stealth_level)
                text = self.fingerprint_scrambler.scramble_fingerprint(text, level=stealth_level)
                print(f"  ✓ Pass 7 complete")
            except Exception as e:
                print(f"  ✗ Pass 7 failed: {e}")
        
        # Pass 8: EXTREME HUMANIZATION (Level 5 ONLY - Nuclear Option)
        if stealth_level >= 5:
            print("→ Running Pass 8: EXTREME HUMANIZATION (Nuclear)...")
            try:
                text = self._pass_8_extreme_humanization(text)
                print(f"  ✓ Pass 8 complete")
            except Exception as e:
                print(f"  ✗ Pass 8 failed: {e}")
        
        # Pass 9: Semantic Entropy Injection
        if stealth_level >= 4:
            print("→ Running Pass 9: Semantic Entropy...")
            try:
                text = self._pass_9_semantic_entropy(text)
                print(f"  ✓ Pass 9 complete")
            except Exception as e:
                print(f"  ✗ Pass 9 failed: {e}")

        # Pass 10: Statistical Anchor Breaking (THE NUCLEAR OPTION)
        if stealth_level >= 5:
            print("→ Running Pass 10: Anchor Breaking...")
            try:
                text = self._pass_10_anchor_breaking(text)
                print(f"  ✓ Pass 10 complete")
            except Exception as e:
                print(f"  ✗ Pass 10 failed: {e}")
        
        # Pass 11: Shadow Rewrite (LLM refinement for Level 5)
        llm_success = False
        if stealth_level >= 5:
            print("→ Running Pass 11: Shadow Rewrite (Refinement)...")
            try:
                # This pass ensures the final flow is human-like
                shadow_text = self._pass_11_shadow_rewrite(text)
                if len(shadow_text) > len(text) * 0.5:
                    text = shadow_text
                    llm_success = True
                print(f"  ✓ Pass 11 complete")
            except Exception as e:
                print(f"  ✗ Pass 11 failed: {e}")

        # Pass 18: Commonality Nullifier (Ghost Protocol v17000.0) - MOVED UP
        if stealth_level >= 5:
            print("→ Running Pass 18: Commonality Nullifier...")
            try:
                text = self._pass_18_commonality_nullifier(text)
                print(f"  ✓ Pass 18 complete")
            except Exception as e:
                print(f"  ✗ Pass 18 failed: {e}")

        # Pass 12: Human Jitter (Subtle)
        if stealth_level >= 4:
            print("→ Running Pass 12: Human Jitter...")
            try:
                text = self._pass_12_human_glitch(text, level=stealth_level)
                print(f"  ✓ Pass 12 complete")
            except Exception as e:
                print(f"  ✗ Pass 12 failed: {e}")

        # Pass 15: Linguistic Shatter (NEW - NUCLEAR)
        if stealth_level >= 5:
            print("→ Running Pass 15: Linguistic Shatter...")
            try:
                text = self._pass_15_linguistic_shatter(text)
                print(f"  ✓ Pass 15 complete")
            except Exception as e:
                print(f"  ✗ Pass 15 failed: {e}")

        # Pass 16: The Reddit Scrambler (NEW - LEVEL 5)
        if stealth_level >= 5:
            print("→ Running Pass 16: Reddit Scrambler...")
            try:
                text = self._pass_16_reddit_scrambler(text)
                print(f"  ✓ Pass 16 complete")
            except Exception as e:
                print(f"  ✗ Pass 16 failed: {e}")

        # Pass 19: Cyrillic Inversion (Ghost Protocol v17000.0)
        if stealth_level >= 5:
            print("→ Running Pass 19: Cyrillic Inversion...")
            try:
                text = self._pass_19_cyrillic_inversion(text)
                print(f"  ✓ Pass 19 complete")
            except Exception as e:
                print(f"  ✗ Pass 19 failed: {e}")

        # Pass 14: Token Shielder (AGGRESSIVE ENCODING SHIELD)
        if stealth_level >= 5:
            print("→ Running Pass 14: Token Shielder...")
            try:
                text = self._pass_14_token_shielder(text, level=stealth_level)
                print(f"  ✓ Pass 14 complete")
            except Exception as e:
                print(f"  ✗ Pass 14 failed: {e}")

        # Artifact Injection (Invisible Noise - CRITICAL FOR BYPASS)
        if use_artifacts or stealth_level >= 3:
            print(f"→ Running Artifact Injection (Level {stealth_level})...")
            try:
                text = self._inject_artifacts(text, level=stealth_level)
                print(f"  ✓ Artifacts injected")
            except Exception as e:
                print(f"  ✗ Artifact injection failed: {e}")

        # Pass 17: Emoji Dynamics (NEW)
        if use_emojis:
            print("→ Running Pass 17: Emoji Dynamics...")
            try:
                text = self._pass_17_emoji_dynamics(text, tone=tone)
                print(f"  ✓ Pass 17 complete ({len(text)} chars)")
            except Exception as e:
                print(f"  ✗ Pass 17 failed: {e}")

        # Add a hidden indicator if LLM failed
        if stealth_level >= 5 and not llm_success:
            text += "\u200B" 

        # Stability Guard
        if stealth_level >= 2:
            print("→ Running Stability Guard...")
            try:
                metrics = self._analyze_heuristics(text)
                print(f"  ✓ Stability check complete")
            except Exception as e:
                print(f"  ✗ Stability guard failed: {e}")

        print(f"\n{'='*60}")
        print(f"HUMANIZATION COMPLETE - Output: {len(text)} chars")
        print(f"{'='*60}\n")
        return text.strip()

    def _analyze_heuristics(self, text):
        """Analyze text for human signals."""
        sentences = nltk.sent_tokenize(text)
        if not sentences:
            return {"variance_score": 0, "opinion_count": 0}
            
        lengths = [len(s.split()) for s in sentences]
        if len(lengths) > 1:
            mean = sum(lengths) / len(lengths)
            variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
            std_dev = variance ** 0.5
        else:
            std_dev = 0
            
        opinion_patterns = ["I ", "me ", "my ", "mine", "we ", "our ", "us "]
        opinion_count = sum(1 for s in sentences if any(p in s.lower() for p in opinion_patterns))
                
        return {"variance_score": std_dev, "opinion_count": opinion_count}

    def _pass_0_obfuscate_intent(self, text):
        """
        Pass 0: Remove AI vocabulary and simplify complex structures.
        Also applies smart synonym replacement.
        """
        ai_words = [
            "additionally", "furthermore", "moreover", "consequently", "therefore",
            "thus", "hence", "notably", "importantly", "specifically", "typically",
            "ultimately", "fostering", "leveraging", "utilizing", "comprehensively",
            "meticulously", "seamlessly", "delve", "ensure", "crucial"
        ]
        
        for word in ai_words:
            pattern = re.compile(r'\b' + re.escape(word) + r'\b,?', re.IGNORECASE)
            text = pattern.sub("", text)
            
        # Simplify complex conjunctions
        text = re.sub(r", which ", ". This ", text)
        text = re.sub(r", while ", ". But ", text)
        text = re.sub(r", although ", ". Even though ", text)
        
        # Apply smart synonym replacement (10-15% of words)
        try:
            replacement_rate = random.uniform(0.10, 0.15)
            text = vocab_enhancer.smart_synonym_replacement(text, replacement_rate)
        except Exception as e:
            print(f"Vocabulary enhancement failed: {e}")
        
        return text

    def _pass_1_destructure(self, text):
        """Pass 1: Break AI symmetry."""
        sentences = nltk.sent_tokenize(text)
        if len(sentences) < 2: return text
        
        transitions = [
            "In conclusion", "Moreover", "Furthermore", "Therefore", "Additionally", 
            "However,", "Thus,", "Hence,", "In summary", "On the other hand",
            "Consequently", "As a result", "For instance", "For example"
        ]
        
        cleaned_sents = []
        for s in sentences:
            s_clean = s.strip()
            for t in transitions:
                if s_clean.lower().startswith(t.lower()):
                    pattern = re.compile(re.escape(t) + r",?\s*", re.IGNORECASE)
                    s_clean = pattern.sub("", s_clean, count=1).strip()
                    if s_clean and s_clean[0].islower():
                        s_clean = s_clean[0].upper() + s_clean[1:]
                    break
            cleaned_sents.append(s_clean)
            
        sentences = cleaned_sents

        # Merge/Shuffle sentences randomly
        new_sentences = []
        i = 0
        while i < len(sentences):
            if i < len(sentences) - 1 and random.random() < 0.45:
                # Randomly choose to merge or swap
                if random.random() < 0.5:
                    connector = random.choice([" and ", " but ", " so ", " - ", " ; ", " "])
                    s1 = sentences[i]
                    s2 = sentences[i+1]
                    
                    if s1 and s1[-1] in [".", ",", "!"]: s1 = s1[:-1]
                    if s2 and s2[0].isupper() and s2.split(" ")[0] not in ["I", "I've", "I'm"]:
                        s2 = s2[0].lower() + s2[1:]
                        
                    merged = s1 + connector + s2
                    new_sentences.append(merged)
                    i += 2
                else:
                    # Swap adjacent sentences (very human to be slightly out of order)
                    new_sentences.append(sentences[i+1])
                    new_sentences.append(sentences[i])
                    i += 2
            else:
                new_sentences.append(sentences[i])
                i += 1
        
        # Random paragraph reconstruction with jitter
        final_text = ""
        current_chunk_size = 0
        target_chunk_size = random.randint(1, 4)
        
        for s in new_sentences:
            final_text += s + " "
            current_chunk_size += 1
            if current_chunk_size >= target_chunk_size:
                # Add random punctuation to break patterns
                if random.random() < 0.15:
                    final_text = final_text.strip() + random.choice(["...", "..", "!"]) + " "
                final_text += "\n\n"
                current_chunk_size = 0
                target_chunk_size = random.randint(1, 4)
                
        return final_text.strip()

    def _pass_2_semantic_rebuild_llm(self, text, level=3, tone="Balanced", audience="General"):
        """Pass 2: LLM rewrite with human persona and custom tone."""
        
        # Determine persona based on level and tone
        if tone == "Professional":
            persona = f"a professional consultant writing for {audience}"
        elif tone == "Academic":
            persona = f"a scholar writing for {audience}"
        elif tone == "Casual":
            persona = f"a casual friend texting {audience}"
        elif tone == "Creative":
            persona = f"a creative writer telling a story to {audience}"
        else:
            persona = f"a human editor writing for {audience}"
            
        # Define tone-specific instructions
        tone_instr = {
            "Professional": "Use clear, authoritative, but accessible language. Keep it structured but avoid generic 'AI' buzzwords like 'synergy' or 'pioneering'.",
            "Academic": "Use precise vocabulary and logical progression. Ensure it sounds like a human researcher, not a robotic generator. Use complex sentence structures naturally.",
            "Casual": "Use very informal language, contractions, and first-person perspective. It's okay to use slang and skip some formal grammar rules.",
            "Creative": "Use descriptive language, metaphors, and varied rhythm. Focus on engagement and vividness.",
            "Balanced": "Mix clarity with a natural, conversational flow. Sound like an intelligent person explaining a concept."
        }.get(tone, "Be natural and human.")

        system_prompt = (
            f"You are {persona}. Read this text and rewrite it in YOUR OWN WORDS for {audience}.\n\n"
            f"TONE INSTRUCTIONS: {tone_instr}\n\n"
            "IMPORTANT RULES:\n"
            "- DON'T just paraphrase. Completely rethink how a human would say this.\n"
            "- Add human-like markers: occasional self-corrections, tangential thoughts, or rhetorical questions.\n"
            "- Use 'bursty' sentence lengths: mix some very short, some medium, and some very long / run-on sentences.\n"
            "- Avoid all typical AI transition words (However, Furthermore, Moreover, In conclusion, Firstly, Finally).\n"
            "- Use 'sloppy' human transitions: 'but yeah', 'also', 'anyway', 'the thing is', 'like i said'.\n"
            "- DO NOT use bullet points or numbered lists. Break all structure into natural paragraphs.\n"
            "- NEVER use the word 'delve', 'tapestry', 'testament', or 'realm'.\n"
        )
        
        if level >= 5:
            system_prompt += (
                "\n- SHATTER THE TEXT: Break logic flow intentionally. Jump between ideas like a human who is thinking while writing."
                "\n- USE BIASED LANGUAGE: Don't be balanced. Have a personal, human opinion on the matter."
                "\n- GHOST WRITING: Occasionally use 'i mean', 'you know', 'basically'. "
                "\n- INTENTIONAL IMPERFECTION: Use an occasional grammar slip (e.g., 'your' instead of 'you're') ONLY IF it feels natural for the tone."
                "\n- BURSTINESS: Mix extremely long run-on sentences with very short 2-3 word fragments."
                "\n- BIAS: Express a clear human preference or doubt about the topic."
            )
        
        # Structure Preservation Instruction
        system_prompt += "\n- CRITICAL: DO NOT MERGE OR SPLIT PARAGRAPHS. Keep the exact same number of paragraphs as the input."
        
        try:
            print(f"  → Calling OpenRouter API (model: gemini-2.0-flash-exp)...")
            result = self._call_llm(system_prompt, text)
            print(f"  ✓ LLM returned {len(result)} chars")
            return result
        except Exception as e:
            print(f"  ✗ LLM Call Failed: {str(e)}")
            print(f"  → Attempting T5 fallback...")
            if self.model:
                return self._pass_2_semantic_rebuild_t5(text)
            else:
                print(f"  ✗ No T5 model available. Returning original text.")
                return text

    def _call_llm(self, system_prompt, user_text):
        """Call OpenRouter API."""
        # Fetch key dynamically to allow for manual entry in UI fallback
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://blizflow.site",
            "X-Title": "BlizFlow AI"
        }
        
        # Try Claude first (better at human-like writing), fallback to Gemini
        models_to_try = [
            "anthropic/claude-3.5-sonnet:beta",
            "google/gemini-2.0-flash-exp:free"
        ]
        
        last_error = None
        
        for model in models_to_try:
            try:
                data = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_text}
                    ],
                    "temperature": 0.9,
                    "max_tokens": 2000
                }
                
                print(f"    Trying model: {model}")
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=45)
                
                print(f"    API Response: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        content = result['choices'][0]['message']['content'].strip()
                        print(f"    ✓ Received {len(content)} chars from {model}")
                        return content
                    else:
                        raise Exception(f"Invalid API response format")
                else:
                    error_detail = response.text[:200]
                    last_error = f"API Error {response.status_code}: {error_detail}"
                    print(f"    ✗ {model} failed: {last_error}")
                    continue  # Try next model
                    
            except Exception as e:
                last_error = str(e)
                print(f"    ✗ {model} error: {last_error}")
                continue  # Try next model
        
        # All models failed
        raise Exception(f"All models failed. Last error: {last_error}")

    def _pass_2_semantic_rebuild_t5(self, text, temperature=1.0):
        """Fallback T5."""
        if not self.model: return text
            
        paragraphs = text.split("\n\n")
        humanized_paragraphs = []
        for paragraph in paragraphs:
            if not paragraph.strip(): continue
            sentences = nltk.sent_tokenize(paragraph)
            new_sents = []
            for sentence in sentences:
                if not sentence.strip(): continue
                input_text = "paraphrase: " + sentence + " </s>"
                encoding = self.tokenizer.encode_plus(input_text, pad_to_max_length=True, return_tensors="pt")
                input_ids = encoding["input_ids"].to(self.device)
                try:
                    outputs = self.model.generate(
                        input_ids=input_ids, max_length=128, do_sample=True, top_p=0.96, temperature=temperature, early_stopping=True, num_return_sequences=1
                    )
                    line = self.tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
                    new_sents.append(line)
                except:
                    new_sents.append(sentence)
            humanized_paragraphs.append(" ".join(new_sents))
        return "\n\n".join(humanized_paragraphs)

    def _pass_2_5_anti_paraphrasing(self, text, level=3):
        """
        Pass 2.5: Anti-Paraphrasing Detection (AGGRESSIVE)
        Breaks paraphrasing patterns by adding human reasoning markers.
        """
        paragraphs = text.split("\n\n")
        final_paragraphs = []
        
        # Human reasoning patterns (EXPANDED)
        clarifiers = [
            "What I mean is, ",
            "To put it differently, ",
            "Or rather, ",
            "In other words, ",
            "Actually, ",
            "Well, ",
            "Let me rephrase that - ",
            "Here's the thing, ",
            "Look, "
        ]
        
        tangential_thoughts = [
            " - at least that's how I see it",
            " (not sure if that makes sense)",
            " - or maybe I'm overthinking it",
            " - though I could be wrong",
            " - that's just my take",
            " - if that makes any sense",
            " - you know what I mean?",
            " - I think",
            ""
        ]
        
        hedges = [
            "kind of ",
            "sort of ",
            "maybe ",
            "probably ",
            "I think ",
            "seems like ",
            "basically ",
            "essentially ",
            "generally "
        ]
        
        # Self-corrections (very human!)
        corrections = [
            "Wait, no - ",
            "Actually, scratch that - ",
            "Or maybe it's better to say ",
            "Well, not exactly, but "
        ]
        
        # Redundancy phrases
        redundancies = [
            " Again, ",
            " Like I said, ",
            " As I mentioned, ",
            " To repeat, "
        ]
        
        # Conversational fillers
        fillers = [
            "you know, ",
            "I mean, ",
            "like, ",
            "so, ",
            "anyway, "
        ]
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                final_paragraphs.append(paragraph)
                continue
                
            sentences = nltk.sent_tokenize(paragraph)
            new_sents = []
            
            for i, sent in enumerate(sentences):
                # INCREASED: Add clarifier (25% up from 15%)
                if random.random() < 0.25 and i > 0:
                    sent = random.choice(clarifiers) + sent[0].lower() + sent[1:]
                
                # INCREASED: Add tangential thought (20% up from 12%)
                if random.random() < 0.20:
                    sent = sent.rstrip('.!?') + random.choice(tangential_thoughts) + "."
                
                # INCREASED: Insert hedge words (30% up from 20%)
                if random.random() < 0.30 and len(sent.split()) > 8:
                    words = sent.split()
                    insert_pos = random.randint(2, min(4, len(words)-2))
                    words.insert(insert_pos, random.choice(hedges))
                    sent = " ".join(words)
                
                # NEW: Self-corrections (10% chance)
                if random.random() < 0.10 and i > 0 and len(sent.split()) > 10:
                    sent = random.choice(corrections) + sent[0].lower() + sent[1:]
                
                # NEW: Redundancy (8% chance, after first sentence)
                if random.random() < 0.08 and i > 1:
                    sent = random.choice(redundancies) + sent[0].lower() + sent[1:]
                
                # NEW: Conversational fillers (15% chance)
                if random.random() < 0.15 and len(sent.split()) > 6:
                    words = sent.split()
                    insert_pos = random.randint(1, min(3, len(words)-2))
                    words.insert(insert_pos, random.choice(fillers))
                    sent = " ".join(words)
                
                new_sents.append(sent)
            
            final_paragraphs.append(" ".join(new_sents))
        
        return "\n\n".join(final_paragraphs)

    def _pass_3_opinion_and_confidence(self, text, level=3):
        """Pass 3: Inject opinions and reduce confidence (BALANCED)."""
        paragraphs = text.split("\n\n")
        final_paragraphs = []
        
        openers = [
            "Personally, ", "To me, ", "Honestly, ", "I feel like ", 
            "From what I've seen, ", "I might be wrong, but ", "If you ask me, ",
            "It seems to me that ", "In my experience, "
        ]
        
        weakeners = {
            "guarantees": "helps", "proves": "suggests", "clearly": "It seems",
            "always": "often", "essential": "useful", "undeniable": "pretty strong",
            "must": "should", "certainly": "probably"
        }
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                final_paragraphs.append(paragraph)
                continue
            
            sentences = nltk.sent_tokenize(paragraph)
            new_sents = []
            
            # REDUCED: 1-2 opinions max per paragraph
            max_signals = 1
            if level >= 4: max_signals = 2
            if level >= 5: max_signals = 3
            
            signals_added = 0
            
            for i, sent in enumerate(sentences):
                for strong, weak in weakeners.items():
                    if strong in sent:
                        sent = sent.replace(strong, weak)
                        
                # Lower probability - only 15% chance
                if signals_added < max_signals and random.random() < 0.15:
                    if i == 0 or len(sent.split()) < 15:
                        opener = random.choice(openers)
                        if sent[0].isupper() and "I " not in sent[:3]:
                            sent = opener + sent[0].lower() + sent[1:]
                        else:
                            sent = opener + sent
                        signals_added += 1
                
                new_sents.append(sent)
                
            final_paragraphs.append(" ".join(new_sents))
            
        return "\n\n".join(final_paragraphs)

    def _pass_4_imperfection(self, text, level=3):
        """Pass 4: Add human errors (REDUCED)."""
        paragraphs = text.split("\n\n")
        final_paragraphs = []
        
        casual_connectors = [", you know,", ", like,", ", basically,", ", honestly,"]
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                final_paragraphs.append(paragraph)
                continue
                
            sentences = nltk.sent_tokenize(paragraph)
            if not sentences: continue
            
            # REDUCED: Only 1 flaw per paragraph at most levels
            num_flaws = 0
            if level >= 3: num_flaws = 1
            if level >= 4: num_flaws = random.randint(1, 2)
            if level >= 5: num_flaws = 2
            
            if num_flaws == 0:
                final_paragraphs.append(paragraph)
                continue
            
            # Select unique targets
            indices = list(range(len(sentences)))
            random.shuffle(indices)
            target_indices = indices[:min(len(sentences), num_flaws)]
            
            for target_idx in target_indices:
                target = sentences[target_idx]
                
                # Prefer casual over destructive changes
                options = ["casual", "fragment"]
                
                # Only add typos at level 5
                if level >= 5 and random.random() < 0.3:
                    options.append("typo")
                
                choice = random.choice(options)
                
                if choice == "fragment" and len(target.split()) > 15:
                    # Only chop very long sentences
                    words = target.split()
                    try:
                        cut = random.randint(7, len(words)-7)
                        target = " ".join(words[:cut]) + ". " + " ".join(words[cut:])
                    except ValueError:
                        pass
                
                elif choice == "typo" and level >= 5:
                    # Very rare typos
                    if len(target) > 10 and random.random() < 0.5:
                        idx = random.randint(1, len(target)-2)
                        char_list = list(target)
                        char_list[idx], char_list[idx+1] = char_list[idx+1], char_list[idx]
                        target = "".join(char_list)
                    
                elif choice == "casual":
                    # Insert casual filler (less frequently)
                    words = target.split()
                    if len(words) > 8 and random.random() < 0.5:
                        ins = random.randint(3, len(words)-3)
                        words.insert(ins, random.choice(casual_connectors).strip())
                        target = " ".join(words)
                
                sentences[target_idx] = target
            
            # No Oxford comma removal - too aggressive
            s_joined = " ".join(sentences)
            final_paragraphs.append(s_joined)
            
        return "\n\n".join(final_paragraphs)

    def _pass_5_rhythm(self, text, level=3):
        """Pass 5: Mix sentence lengths aggressively (BURSTINESS)."""
        paragraphs = text.split("\n\n")
        final_paragraphs = []
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                final_paragraphs.append(paragraph)
                continue
                
            sentences = nltk.sent_tokenize(paragraph)
            if len(sentences) < 2:
                final_paragraphs.append(paragraph)
                continue
            
            final_sents = []
            # Level 5 forces extreme burstiness
            burst_chance = 0.85 if level >= 5 else 0.40
            
            for i, s in enumerate(sentences):
                # Aggressively shorten or lengthen
                if random.random() < burst_chance and len(s.split()) > 15:
                    # Break long sentence
                    parts = s.split(', ')
                    if len(parts) > 1:
                        final_sents.append(parts[0] + ".")
                        final_sents.append("Wait, " + ", ".join(parts[1:]))
                    else:
                        final_sents.append(s)
                elif i < len(sentences) - 1 and random.random() < burst_chance and len(s.split()) < 10:
                    # Combine short sentence with 'and like'
                    final_sents.append(s.rstrip('.') + " and like " + sentences[i+1][0].lower() + sentences[i+1][1:])
                else:
                    final_sents.append(s)
            
            final_paragraphs.append(" ".join(final_sents))
            
        return "\n\n".join(final_paragraphs)
    
    def _pass_10_anchor_breaking(self, text):
        """
        Pass 10: Statistical Anchor Breaking
        Breaks AI's signature word-frequency patterns and adds human-like 'debris'.
        """
        words = text.split()
        if not words: return text
        
        # Human debirs - non-sequiturs and self-corrections
        debris = [
            " wait, ", " honestly, ", " i think, ", " like, ", " i guess, ",
            "...actually, ", " no wait, ", " literally, ", " basically, "
        ]
        
        # Common word swaps (Typos) for level 5
        swaps = {
            "their": "there", "there": "their", "too": "to", "to": "too",
            "your": "you're", "you're": "your", "its": "it's", "it's": "its"
        }
        
        new_words = []
        for i, w in enumerate(words):
            # 1. Randomly insert debris (8% chance)
            if random.random() < 0.08:
                new_words.append(random.choice(debris).strip())
            
            # 2. Randomly swap common words (5% chance)
            w_lower = w.lower().strip('.,!?')
            if w_lower in swaps and random.random() < 0.05:
                # Keep original capitalization
                swapped = swaps[w_lower]
                if w[0].isupper():
                    swapped = swapped[0].upper() + swapped[1:]
                new_words.append(swapped)
            else:
                new_words.append(w)
                
            # 3. Repeat a word occasionally (The "I i" phenomenon)
            if random.random() < 0.03:
                new_words.append(w)
                
        return " ".join(new_words)

    def _pass_11_shadow_rewrite(self, text):
        """
        Pass 11: Shadow Rewrite (GOD MODE VERSION)
        Forces the LLM to write like a highly opinionated, slightly chaotic human.
        """
        system_prompt = (
            "You are a human writing a post on a forum. You are NOT an AI. "
            "You write with clear bias, use personal anecdotes (invent them if needed), "
            "and skip all formal transitions. "
            "RULES:\n"
            "- Use 'i' instead of 'I' occasionally.\n"
            "- Use informal contractions (gonna, wanna, gotta).\n"
            "- Add human hesitation: 'uh', 'um', 'wait...', 'anyway'.\n"
            "- Deliberately make 1-2 grammatical mistakes that humans commonly make (e.g., 'there's people' instead of 'there are people').\n"
            "- BREAK ALL STRUCTURE. Do not use bullet points or lists.\n"
            "- Vary sentence length: some very long (run-on) and some very short.\n"
            "- Sound slightly annoyed or tired. Output ONLY the raw content."
        )
        
        try:
            # Shift temperature for maximum entropy
            result = self._call_llm(system_prompt, text)
            return result
        except:
            return text

    def _pass_12_human_glitch(self, text, level=5):
        """
        Pass 12: The Human Glitch (TONED DOWN)
        Introduces very subtle jitter and typos to maintain readability.
        """
        words = text.split()
        new_words = []
        
        typo_map = {
            "the": ["teh"], "and": ["nd"], "because": ["bc"],
            "with": ["w/"], "don't": ["dont"], "can't": ["cant"], "about": ["abt"]
        }
        
        for w in words:
            clean_w = w.lower().strip('.,!?')
            # REDUCED CHANCE: 3% for low levels, 8% for high
            chance = 0.03 if level < 5 else 0.08
            
            # 1. Punctuation Malfunction (REDUCED to 5%)
            if level >= 4 and random.random() < 0.05:
                if w.endswith(','): 
                    if random.random() < 0.5: w = w[:-1] 
                elif w.endswith('.') and random.random() < 0.2:
                    w = w[:-1] # Drop end period occasionally

            # 2. Key Typos
            if clean_w in typo_map and random.random() < chance:
                new_w = random.choice(typo_map[clean_w])
                if w.endswith('.') or w.endswith(',') or w.endswith('!') or w.endswith('?'):
                    new_w += w[-1]
                new_words.append(new_w)
            
            # 3. Key jitter (REDUCED to 3-5%)
            elif len(w) > 5 and random.random() < (0.02 if level < 5 else 0.05):
                chars = list(w)
                idx = random.randint(1, len(chars)-2)
                chars[idx], chars[idx+1] = chars[idx+1], chars[idx]
                new_words.append("".join(chars))
            else:
                new_words.append(w)
                
        return " ".join(new_words)

    def _pass_13_conversational_detours(self, text):
        """
        Pass 13: Conversational Detours
        Adds human 'fillers' and tangential thoughts as markers of human brain-lag.
        """
        sentences = nltk.sent_tokenize(text)
        new_sents = []
        fillers = ["um, ", "uh, ", "like, ", "i mean, ", "wait, ", "actually, "]
        detours = [
            " (if that makes sense) ", 
            " (idk just thinking out loud) ", 
            " - sorry, drifting off topic - ",
            " ...anyway, "
        ]
        
        for i, sent in enumerate(sentences):
            # 1. Start with filler (REDUCED to 8% chance)
            if random.random() < 0.08:
                sent = random.choice(fillers) + sent[0].lower() + sent[1:]
            
            # 2. Add detour in middle (REDUCED to 5% chance)
            if random.random() < 0.05 and len(sent.split()) > 12:
                words = sent.split()
                mid = len(words) // 2
                sent = " ".join(words[:mid]) + random.choice(detours) + " ".join(words[mid:])
            
            new_sents.append(sent)
            
        return " ".join(new_sents)

    def _pass_14_token_shielder(self, text, level=5):
        """
        Pass 14: Token Shielder (Encoding Sabotage - REFINED)
        Inserts invisible markers strategically to block tokenization.
        Ghost Protocol Update: Injects Word Joiners (\u2060) into 95% of word boundaries at Level 5.
        """
        if level < 3: return text
        
        words = text.split()
        shielded_words = []
        bombs = ["\u200B", "\u200C", "\u200D", "\u2060"]
        
        for i, word in enumerate(words):
            # Chance based on level
            chance = 0.95 if level >= 5 else 0.50
            
            if random.random() < chance and len(word) > 1:
                # Insert 2-3 bombs at random positions
                chars = list(word)
                num_bombs = random.randint(1, 2) if level < 5 else random.randint(2, 4)
                for _ in range(num_bombs):
                    idx = random.randint(1, len(chars)-1)
                    chars.insert(idx, random.choice(bombs))
                word = "".join(chars)
            
            # THE N-GRAM NULLIFIER: Inject WJ into word boundary
            if level >= 5 and i < len(words) - 1 and random.random() < 0.95:
                word += "\u2060"
                
            shielded_words.append(word)
                
        return " ".join(shielded_words)

    def _inject_artifacts(self, text, level=3):
        """
        GHOST STEALTH: Invisible Artifact Injection.
        Looks identical to a human, but shatters AI tokenization.
        """
        if level < 3: return text
        
        # We only use truly invisible Unicode control characters
        # \u200b: Zero Width Space
        # \u200c: Zero Width Non-Joiner
        # \u200d: Zero Width Joiner
        bombs = ['\u200B', '\u200C', '\u200D']
        
        words = text.split(' ')
        final_words = []
        
        for word in words:
            if not word or len(word) < 3:
                final_words.append(word)
                continue
            
            # Chance to inject based on level
            chance = 0.4 if level < 5 else 0.7
            
            if random.random() < chance:
                # Inject 1-3 invisible marks at random positions inside the word
                num_marks = random.randint(1, 2) if level < 5 else random.randint(2, 4)
                chars = list(word)
                for _ in range(num_marks):
                    # Avoid injecting at the very start/end for stability
                    idx = random.randint(1, len(chars)-1)
                    chars.insert(idx, random.choice(bombs))
                word = "".join(chars)
            
            final_words.append(word)
            
        return " ".join(final_words)

    def _pass_15_linguistic_shatter(self, text):
        """Pass 15: Subtle Syntactic Variety (CLEANED)."""
        # Removed aggressive mid-word caps and symbol swaps that caused 'gu10 ess'
        words = text.split()
        shattered = []
        for w in words:
            # Only apply very subtle variety to common words
            swaps = {"and": "&", "to": "to", "for": "for"} # Kept very minimal
            if w.lower() in swaps and random.random() < 0.05:
                w = swaps[w.lower()]
            shattered.append(w)
        return " ".join(shattered)

    def _pass_16_reddit_scrambler(self, text):
        """Pass 16: Ultra-conversational, biased human persona."""
        sentences = nltk.sent_tokenize(text)
        scrambled = []
        asides = [
            " - which is crazy if u think about it - ",
            " (everyone knows this anyway lmao) ",
            " - personal opinion obv - ",
            " (probably gonna get hate for this but idc) ",
            " - wait, actually - ",
            " (ngl this took me forever to write) ",
            " ...anyway fr "
        ]
        for sent in sentences:
            if random.random() < 0.15:
                sent = sent.rstrip('.') + random.choice(asides)
            scrambled.append(sent)
        return " ".join(scrambled)
    
    def _pass_8_extreme_humanization(self, text):
        """
        Pass 8: EXTREME HUMANIZATION (Nuclear Option for Level 5)
        Maximum chaos - internet slang, personal commentary, intentional mess.
        """
        sentences = nltk.sent_tokenize(text)
        new_sents = []
        
        # EXTREME casual internet language
        internet_slang = [
            "ngl", "tbh", "fr", "lol", "lmao", "lowkey", "highkey", 
            "imo", "imho", "idk", "tbf", "icl"
        ]
        
        # Personal interjections (VERY human)
        interjections = [
            "wait -", "okay so", "like", "literally", "honestly",
            "i mean", "you know", "right?", "fr fr"
        ]
        
        # Meta-commentary (self-aware)
        meta = [
            "(idk if that makes sense)",
            "(probably wrong but whatever)",
            "(just my 2 cents)",
            "(could be totally off base here)"
        ]
        
        for i, sent in enumerate(sentences):
            # Protective check: skip sentences that look like citations or URLs
            if "http" in sent or "www" in sent or "[" in sent:
                new_sents.append(sent)
                continue

            # 1. Lowercase "I" (Reduced to 15%)
            sent = re.sub(r'\bI\b', lambda m: 'i' if random.random() < 0.15 else 'I', sent)
            
            # 2. Add internet slang (Reduced to 10% - only very common ones)
            if random.random() < 0.10:
                sent = sent.rstrip('.!?') + f" {random.choice(['tbh', 'imo', 'fr'])}."
            
            # 3. Start with interjection (Reduced to 10%)
            if random.random() < 0.10 and len(sent.split()) > 8:
                sent = random.choice(["okay so", "honestly", "i mean"]) + " " + sent[0].lower() + sent[1:]
            
            # 4. Add meta-commentary (Reduced to 5%)
            if random.random() < 0.05:
                sent = sent.rstrip('.!?') + f" {random.choice(['(just my take)', '(imo)'])}"
            
            new_sents.append(sent)
        
        # 8. Add random personal story at the end (20% chance)
        if random.random() < 0.20:
            stories = [
                "anyway thats just what i think lol",
                "or maybe im totally wrong idk",
                "this is just based on my experience tho",
                "but yeah thats my take on it fr"
            ]
            new_sents.append(random.choice(stories))
        
        final_text = " ".join(new_sents)
        
        # 9. Overall lowercase informal start (30% chance)
        if random.random() < 0.30 and final_text:
            final_text = final_text[0].lower() + final_text[1:]
        
        return final_text

    def _pass_9_semantic_entropy(self, text):
        """
        Pass 9: Semantic Entropy Injection
        Injects 'Human-Only' linguistic patterns that AI detectors use to find humans.
        """
        paragraphs = text.split("\n\n")
        entropy_paragraphs = []
        
        # Words AI avoids but humans love
        human_keywords = ["literally", "basically", "actually", "kinda", "sorta", "honestly", "maybe", "pretty much"]
        
        for para in paragraphs:
            if not para.strip(): continue
            words = para.split()
            
            # 1. Vocabulary Jitter: Occasionally change common words to slightly 'looser' ones
            loosening_map = {
                "utilize": "use", "facilitate": "help", "implement": "do", 
                "commence": "start", "terminate": "stop", "regarding": "about"
            }
            for i, w in enumerate(words):
                if w.lower() in loosening_map and random.random() < 0.5:
                    words[i] = loosening_map[w.lower()]
            
            # 2. Inject Human Keywords randomly (10% chance per 10 words)
            for i in range(len(words) // 8):
                if random.random() < 0.3:
                    idx = random.randint(0, len(words)-1)
                    words.insert(idx, random.choice(human_keywords))
            
            # 3. Repeat for emphasis (Very human)
            if random.random() < 0.10:
                rep_word = random.choice(["really", "very", "so"])
                for i, w in enumerate(words):
                    if w.lower() == rep_word:
                        words.insert(i+1, rep_word)
                        break
            
            entropy_paragraphs.append(" ".join(words))
            
        return "\n\n".join(entropy_paragraphs)

    def _pass_18_commonality_nullifier(self, text):
        """
        Pass 18: Commonality Nullifier (Ghost Protocol v17000.0)
        Targets GPTZero's Commonality Engine by replacing common words with rare synonyms.
        """
        if not self.common_words_set or not self.rare_vocab_set:
            return text
            
        words = text.split()
        new_words = []
        
        for word in words:
            clean_word = word.lower().strip('.,!?')
            if clean_word in self.common_words_set and random.random() < 0.3:
                # Try to find a rare synonym
                syns = self._get_synonyms_simple(clean_word)
                rare_syns = [s for s in syns if s.lower() in self.rare_vocab_set]
                
                if rare_syns:
                    replacement = random.choice(rare_syns)
                    # Preserve case
                    if word[0].isupper():
                        replacement = replacement.capitalize()
                    new_words.append(replacement)
                else:
                    new_words.append(word)
            else:
                new_words.append(word)
                
        return " ".join(new_words)

    def _get_synonyms_simple(self, word):
        """Simple synonym lookup using WordNet."""
        from nltk.corpus import wordnet
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().replace('_', ' '))
        return list(synonyms)

    def _pass_19_cyrillic_inversion(self, text):
        """
        Pass 19: Cyrillic Inversion (Ghost Protocol v17000.0)
        Replaces 20% of 'a', 'e', and 'o' with their Cyrillic homoglyphs.
        """
        char_map = {
            'a': 'а', # U+0430
            'e': 'е', # U+0435
            'o': 'о', # U+043E
            'A': 'А', # U+0410
            'E': 'Е', # U+0415
            'O': 'О'  # U+041E
        }
        
        result = []
        for char in text:
            if char in char_map and random.random() < 0.20:
                result.append(char_map[char])
            else:
                result.append(char)
                
        return "".join(result)
    def _pass_17_emoji_dynamics(self, text, tone="Balanced"):
        """Pass 17: Inject human-like emojis based on sentiment/tone."""
        sentences = nltk.sent_tokenize(text)
        new_sents = []
        
        # Emoji groups
        positive = ["✨", "🚀", "🙌", "🔥", "✅", "💡", "🌟"]
        thinking = ["🤔", "💭", "🧐", "🧠"]
        casual = ["😂", "lol", "🙏", "💯", "🤷‍♂️", "😅"]
        creative = ["🌈", "🎨", "✍️", "🎭", "🪄"]
        
        for sent in sentences:
            if random.random() < 0.15: # 15% chance per sentence
                if tone == "Creative":
                    emoji = random.choice(creative + positive)
                elif tone == "Casual":
                    emoji = random.choice(casual + positive)
                elif tone == "Professional":
                    emoji = random.choice(["📈", "🎯", "🤝", "💡"])
                else:
                    emoji = random.choice(positive + thinking)
                
                # Append emoji naturally
                sent = sent.rstrip('.!?') + " " + emoji + random.choice([".", "!", ""])
            new_sents.append(sent)
            
        return " ".join(new_sents)
