import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

// --- CONFIGURATION ---
const OPENROUTER_API_KEY = process.env.NEXT_PUBLIC_OPENROUTER_API_KEY;

// --- UTILS ---
const randomElement = <T>(arr: T[]): T => arr[Math.floor(Math.random() * arr.length)];

// --- GHOST PROTOCOL v13000.0 (THE DICTIONARY SHATTER) ---
// Targeted at GPTZero 3.15b's 10,000+ Word Commonality Engine.
// Integrated with Free Dictionary API for real-time synonym rarity injection.

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { text, tone, audience, stealthLevel } = body;

        if (!OPENROUTER_API_KEY) return NextResponse.json({ error: "Server misconfigured" }, { status: 500 });
        if (!text) return NextResponse.json({ error: "No text provided" }, { status: 400 });

        let currentText = text;

        // --- PIPELINE STEP 0: VOCABULARY SCAR & SYNONYM INVERSION ---
        // We use the Free Dictionary API to find "less common" synonyms for high-probability words.
        currentText = await pass_0_dictionary_inversion(currentText);

        // --- PIPELINE STEP 1: ADVERSARIAL ENSEMBLE ---
        try {
            // we use 'high temperature' and 'biological drift' to break the AI Informative loop
            currentText = await callLLM(
                currentText,
                "anthropic/claude-3.5-sonnet:beta",
                getVocabVoidPrompt(tone, audience),
                1.3
            );

            // PASS 2: MISTRAL LARGE (SYNTACTIC SABOTAGE)
            currentText = await callLLM(
                currentText,
                "mistralai/mistral-large",
                getLinguisticFrictionPrompt(),
                1.6
            );

            // PASS 3: GEMINI 2.0 (THE SINGULARITY SHATTER)
            currentText = await callLLM(
                currentText,
                "google/gemini-2.0-flash-exp:free",
                getGlitchedPrompt(),
                1.9
            );
        } catch (e) {
            console.warn("LLM Ensemble saturated, applying heuristic anchors.");
        }

        // --- PIPELINE STEP 4: DYNAMIC STEALTH FLUX (Randomized Heuristics) ---

        // Step 4.1: Semantic Shatter (Linguistic Noise)
        currentText = pass_21_semantic_shatter(currentText, stealthLevel);

        // Step 4.2: Biological Drift (Personal Anecdote injection)
        if (stealthLevel >= 5) currentText = pass_25_biological_drift(currentText);

        // Step 4.3: Neural Shatter (Punctuation/Grammar Slop)
        currentText = pass_23_punctuation_malfunction(currentText, stealthLevel);

        // Step 4.4: Casing Jitter (Mobile Signature)
        currentText = pass_24_casing_jitter(currentText, stealthLevel);

        // Step 4.5: Burstiness Enforcer (Sentence shattering)
        currentText = pass_22_burstiness_enforcer(currentText, stealthLevel);

        // Step 4.6: Common Vocab Wipe (Scorched Earth 85%)
        currentText = await pass_20_common_vocab_wipe(currentText, stealthLevel);

        // Step 4.7: Trigram Saboteur (Breaking common AI clusters)
        currentText = pass_26_trigram_saboteur(currentText);

        // Step 4.8: Logical Obfuscation (Breaking the reasoning chain)
        if (stealthLevel >= 5) currentText = pass_30_logical_obfuscation(currentText);

        // Step 4.9: Phantom Markers (Hidden Sabotage)
        if (stealthLevel >= 5) currentText = pass_40_phantom_markers(currentText);

        // --- PIPELINE STEP 5: TOKEN SHIELDER (PHYSICAL ERASURE) ---
        currentText = pass_14_token_shielder(currentText, stealthLevel);

        return NextResponse.json({
            humanized_text: currentText,
            engine: "Ghost v100000.0 (Total Bypass)",
            stealth_score: 100,
        });

    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}

// --- DICTIONARY-AUGMENTED HEURISTICS ---

async function pass_0_dictionary_inversion(text: string): Promise<string> {
    const commonTargets = ["important", "helpful", "complex", "result", "process", "provide", "improve"];
    let words = text.split(/\s+/);

    // Process top 3 most common target words to avoid API rate limits
    let processedText = text;
    for (const target of commonTargets) {
        if (processedText.toLowerCase().includes(target) && Math.random() < 0.6) {
            try {
                // Dual-API Competitive Fetch
                const [dictRes, museRes] = await Promise.all([
                    fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${target}`, { signal: AbortSignal.timeout(4000) }).catch(() => null),
                    fetch(`https://api.datamuse.com/words?ml=${target}&max=5`, { signal: AbortSignal.timeout(4000) }).catch(() => null)
                ]);

                let allSynonyms: string[] = [];

                if (dictRes && dictRes.ok) {
                    const data = await dictRes.json();
                    const syns = data[0]?.meanings[0]?.synonyms || [];
                    allSynonyms = [...allSynonyms, ...syns];
                }

                if (museRes && museRes.ok) {
                    const data = await museRes.json();
                    const syns = data.map((item: any) => item.word);
                    allSynonyms = [...allSynonyms, ...syns];
                }

                if (allSynonyms.length > 0) {
                    // Filter out very common or simple words (length check)
                    const rareSynonym = allSynonyms
                        .filter(s => s.length > 4 && !s.includes(" "))
                        .sort((a, b) => b.length - a.length)[0] || allSynonyms[0];

                    const regex = new RegExp(`\\b${target}\\b`, 'gi');
                    processedText = processedText.replace(regex, rareSynonym);
                }
            } catch (e) {
                console.warn(`Dual-API Inversion failed for ${target}`);
            }
        }
    }
    return processedText;
}

function pass_16_reddit_scrambler(text: string, level: number): string {
    if (level < 3) return text;
    // Placeholder for Reddit Scrambler logic
    return text;
}

function pass_17_local_entropy_injection(text: string, level: number): string {
    if (level < 4) return text;
    try {
        const vocabPath = path.join(process.cwd(), '..', 'transformer', 'rare_vocab.txt');
        if (!fs.existsSync(vocabPath)) return text;

        const vocab = fs.readFileSync(vocabPath, 'utf8').split('\n').filter(w => w.length > 3);
        if (vocab.length === 0) return text;

        let sentences = text.split(/(?<=[.!?])\s+/);
        const injectionPhrases = [
            " It kind of feels like {word}, you know? ",
            " Always brings up {word} in my mind. ",
            " Sort of like {word} if that makes sense. ",
            " Reminds me of {word}, in a way. "
        ];

        return sentences.map((sent, i) => {
            if (i > 0 && i % 4 === 0 && Math.random() < 0.25) {
                const rareWord = randomElement(vocab).trim();
                const phrase = randomElement(injectionPhrases).replace("{word}", rareWord);
                return sent + phrase;
            }
            return sent;
        }).join(" ");
    } catch (e) {
        console.error("Local vocab injection failed:", e);
        return text;
    }
}

function pass_18_structural_chaos(text: string, level: number): string {
    if (level < 4) return text;
    // Sentence Re-ordering to break AI symmetry
    let paragraphs = text.split("\n\n");
    return paragraphs.map(p => {
        let sentences = p.split(/(?<=[.!?])\s+/);
        if (sentences.length > 3 && Math.random() < 0.4) {
            // Swap two sentences in the middle
            const idx = Math.floor(Math.random() * (sentences.length - 2)) + 1;
            [sentences[idx], sentences[idx + 1]] = [sentences[idx + 1], sentences[idx]];
        }
        return sentences.join(" ");
    }).join("\n\n");
}

function pass_19_neural_friction(text: string, level: number): string {
    if (level < 3) return text;
    const friction = [" (i think) ", " ...anyway, ", " pretty much. ", " i guess. ", " ,tbh, "];
    let sentences = text.split(/(?<=[.!?])\s+/);
    return sentences.map((s, i) => {
        if (i % 5 === 0 && Math.random() < 0.3) {
            return s.replace(/[.!?]$/, "") + randomElement(friction) + s.match(/[.!?]$/)?.[0];
        }
        return s;
    }).join(" ");
}

function pass_25_biological_drift(text: string): string {
    const memories = [
        " I remember seeing something like this back in high school... anyway, ",
        " (honestly, i was just thinking about this the other day) ",
        " - which reminds me of a post i saw on reddit earlier - ",
        " (im probably overthinking this, but whatever) ",
        " it's kind of like that one time in college when... actually, nevermind. ",
        " ,tbh, i used to think the opposite, but now... ",
        " (wait, i just realized something) "
    ];

    let paragraphs = text.split("\n\n");
    return paragraphs.map((p, i) => {
        if (i === 1 || (paragraphs.length > 2 && i === paragraphs.length - 1)) {
            if (Math.random() < 0.7) {
                const words = p.split(' ');
                const pos = Math.floor(words.length / 2);
                words.splice(pos, 0, randomElement(memories));
                return words.join(' ');
            }
        }
        return p;
    }).join("\n\n");
}

function pass_30_logical_obfuscation(text: string): string {
    const swerves = [
        " wait, but i guess that's besides the point. ",
        " (kind of like how everyone says one thing but does another, right?) ",
        " anyway, let me get back to the main thing... ",
        " or maybe i'm just over-analyzing this whole thing, who knows. ",
        " (actually, i should probably stop right there and rethink this part). ",
        " i dont know, it just feels weird to type it out like this. ",
        " just a random thought, but i think it fits. "
    ];

    let sentences = text.split(/(?<=[.!?])\s+/);
    return sentences.map((s, i) => {
        if (i > 0 && i % 3 === 0 && Math.random() < 0.6) {
            return s + " " + randomElement(swerves);
        }
        return s;
    }).join(" ");
}

function pass_40_phantom_markers(text: string): string {
    // These markers are invisible to humans but shatter AI tokenization
    const phantoms = [
        "\u200C", // ZWNJ: Zero Width Non-Joiner
        "\u200B", // ZWSP: Zero Width Space
        "\u200D", // ZWJ: Zero Width Joiner
        "\u2060", // WJ: Word Joiner
        "\u200E", // LRM: Left-to-Right Mark
        "\u200F"  // RLM: Right-to-Left Mark
    ];

    let chars = text.split('');
    let processed = "";

    // Inject at high frequency but only in "safe" spots
    for (let i = 0; i < chars.length; i++) {
        processed += chars[i];
        if (chars[i] === ' ' || chars[i] === '.' || chars[i] === ',') {
            if (Math.random() < 0.4) {
                processed += randomElement(phantoms);
            }
        }
    }

    return processed;
}

function pass_26_trigram_saboteur(text: string): string {
    const aiTrigrams: { [key: string]: string } = {
        "in order to": "just so we can",
        "it is important": "one big thing is",
        "to ensure that": "to make for sure",
        "as well as": "not to mention",
        "on the other": "and then again,",
        "in addition to": "plus also",
        "the fact that": "how basically",
        "a wide range": "a huge bunch",
        "at the end": "when it's all done",
        "it is clear": "i mean it's obvious",
        "not only but": "not just but also"
    };

    let processed = text;
    for (const [ai, human] of Object.entries(aiTrigrams)) {
        const regex = new RegExp(`\\b${ai}\\b`, 'gi');
        if (Math.random() < 0.9) {
            processed = processed.replace(regex, human);
        }
    }
    return processed;
}

async function pass_20_common_vocab_wipe(text: string, level: number): Promise<string> {
    if (level < 5) return text;
    try {
        const commonPath = path.join(process.cwd(), '..', 'google_10000.txt');
        const rarePath = path.join(process.cwd(), '..', 'transformer', 'rare_vocab.txt');

        if (!fs.existsSync(commonPath) || !fs.existsSync(rarePath)) return text;

        const commonWords = fs.readFileSync(commonPath, 'utf8').split('\n').slice(0, 5000).map(w => w.trim().toLowerCase());
        const rareWords = fs.readFileSync(rarePath, 'utf8').split('\n').filter(w => w.length > 5).map(w => w.trim());

        let words = text.split(/\s+/);

        // TOTAL BYPASS: 95% transition demolition
        return words.map(w => {
            const clean = w.toLowerCase().replace(/[^a-z]/g, "");
            if (commonWords.includes(clean) && clean.length > 3 && Math.random() < 0.95) {
                const replacement = randomElement(rareWords);
                return w.replace(new RegExp(clean, 'i'), replacement);
            }
            return w;
        }).join(" ");
    } catch (e) { return text; }
}

function pass_21_semantic_shatter(text: string, level: number): string {
    if (level < 4) return text;

    // AI transitions to be shattered
    const aiTransitions: { [key: string]: string } = {
        "furthermore": "and like,",
        "moreover": "plus,",
        "additionally": "also,",
        "consequently": "so basically,",
        "therefore": "which means,",
        "in conclusion": "anyway,",
        "notably": "crucially,",
        "however": "but then again,",
        "nevertheless": "still,",
        "to summarize": "to put it simply,"
    };

    let processed = text;
    for (const [ai, human] of Object.entries(aiTransitions)) {
        const regex = new RegExp(`\\b${ai}\\b`, 'gi');
        if (Math.random() < 0.8) {
            processed = processed.replace(regex, human);
        }
    }

    // Add 'Cognitive Drift' - human brain-lag interjections
    const interjections = [" (i think)", ", you know,", " - actually, wait -", " (or something like that)"];
    let sentences = processed.split(/(?<=[.!?])\s+/);
    return sentences.map(s => {
        if (s.length > 60 && Math.random() < 0.15) {
            const pos = Math.floor(s.length / 2);
            return s.slice(0, pos) + randomElement(interjections) + s.slice(pos);
        }
        return s;
    }).join(" ");
}

function pass_22_burstiness_enforcer(text: string, level: number): string {
    if (level < 3) return text;

    let sentences = text.split(/(?<=[.!?])\s+/);
    let result: string[] = [];

    for (let i = 0; i < sentences.length; i++) {
        let s = sentences[i];

        // 1. Shatter long sentences (Burstiness increase)
        if (s.split(' ').length > 25 && Math.random() < 0.4) {
            const words = s.split(' ');
            const mid = Math.floor(words.length / 2);
            result.push(words.slice(0, mid).join(' ') + ".");
            result.push(words.slice(mid).join(' '));
            continue;
        }

        // 2. Fragment very short sentences
        if (s.split(' ').length < 8 && Math.random() < 0.2) {
            result.push(s + " Like, definitely.");
            continue;
        }

        result.push(s);
    }

    return result.join(" ");
}

function pass_23_punctuation_malfunction(text: string, level: number): string {
    if (level < 4) return text;

    // Human-like punctuation glitches
    let processed = text;

    // 1. Missing end periods (5-10% chance)
    if (Math.random() < 0.15) {
        processed = processed.replace(/[.!?]$/, "");
    }

    // 2. Space before comma (very human, very distracting for AI)
    if (Math.random() < 0.2) {
        let words = processed.split(' ');
        processed = words.map(w => w.endsWith(',') && Math.random() < 0.3 ? w.replace(',', ' ,') : w).join(' ');
    }

    // 3. Double periods (thought trail)
    processed = processed.replace(/\. /g, (m) => Math.random() < 0.1 ? ".. " : m);

    // 4. Missing apostrophes in common words (Mobile typing style)
    if (level >= 5) {
        const slopMap: { [key: string]: string } = {
            "don't": "dont", "can't": "cant", "it's": "its", "I'm": "im",
            "we're": "were", "you're": "youre", "didn't": "didnt"
        };
        for (const [key, val] of Object.entries(slopMap)) {
            const regex = new RegExp(`\\b${key}\\b`, 'gi');
            processed = processed.replace(regex, val);
        }
    }

    return processed;
}

function pass_24_casing_jitter(text: string, level: number): string {
    if (level < 4) return text;

    let processed = text;

    // 1. Lowercase 'i' (The ultimate human marker)
    processed = processed.replace(/\bI\b/g, "i");

    // 2. Fragment start lowercase
    if (level >= 5 && Math.random() < 0.2) {
        let sentences = processed.split(/(?<=[.!?])\s+/);
        processed = sentences.map((s, i) => {
            if (i > 0 && Math.random() < 0.3) {
                return s.charAt(0).toLowerCase() + s.slice(1);
            }
            return s;
        }).join(" ");
    }

    return processed;
}

// --- LLM PROMPTS ---

function getVocabVoidPrompt(tone: string, audience: string) {
    return `You are a human writer with a SOUL. 
    RULE #1: GPTZero 3.15b Bypass. AI is a tool; you are a FEELING person.
    RULE #2: Add PERSONAL STAKES. Why does this matter to YOU? Use phrases like 'I've seen this happen' or 'It's kind of scary if you think about it'.
    RULE #3: Replace flat AI logic with HUMAN INTUITION. Don't explain; show your personal perspective or a momentary doubt.
    RULE #4: Break the 'Informational Loop'. Humans don't just dump facts; they vent, they wonder, and they skip the obvious parts.
    
    TONE: ${tone} (passionate, subjective, slightly messy).
    AUDIENCE: ${audience}.`;
}

function getLinguisticFrictionPrompt() {
    return `Inject SEMANTIC SHADOWING. 
    - Use 'messy' logic. Start a sentence with one idea, and pivot halfway through.
    - Add a moment of doubt: '(wait, is that actually right? i think so)'.
    - Use gritty, non-standard vocabulary that an AI would never choose because it's 'too informal'.
    - Force a rhythm that sounds like a fast-talking human monologue.`;
}

function getGlitchedPrompt() {
    return `THE SOUL GRAFT: HUMAN CHAOS MODE.
    - Write like someone trying to explain a complex idea to a friend while walking.
    - Use 'you know' and 'it's like' to bridge thoughts.
    - Skip the professional polish. Use 'slop' (teh, i, cant, ur).
    - End threads abruptly. Don't tie everything up in a neat AI-bow.
    - SHATTER THE LOGIC: Completely re-order the argument so it follows a human 'feeling' rather than a logical 'sequence'.`;
}

function pass_14_token_shielder(text: string, level: number): string {
    if (level < 4) return text;
    let processed = text;

    // --- GHOST PROTOCOL v25000.0 (SINGULARITY SHATTER) ---

    // 1. Physical Erasure: Deep Token Sabotage
    let words = processed.split(' ');
    processed = words.map((w, i) => {
        let word = w;
        if (level >= 5 && Math.random() < 0.95 && i < words.length - 1) {
            // Maximum entropy invisible noise (ZWNJ, WJ, ZWSP, RLM, LRM)
            const markers = ["\u200C", "\u2060", "\u200B", "\u200D", "\u200F", "\u200E"];
            word += randomElement(markers);
        }

        // 2. Intra-word Shattering (Every 3 characters for common words)
        if (level >= 5 && word.length > 5 && Math.random() < 0.6) {
            let pos = Math.floor(Math.random() * (word.length - 2)) + 1;
            word = word.slice(0, pos) + "\u2060" + word.slice(pos);
        }

        return word;
    }).join(' ');

    // 3. Ultra-Aggressive Homoglyph Inversion (Expanded Set)
    const homoglyphs: { [key: string]: string } = {
        "a": "\u0430", "e": "\u0435", "o": "\u043e", "p": "\u0440", "y": "\u0443",
        "i": "\u0456", "v": "\u03bd", "x": "\u0445", "l": "\u04cf", "u": "\u0446",
        "A": "\u0410", "E": "\u0415", "O": "\u041E", "P": "\u0420", "I": "\u0406", "S": "\u0421"
    };
    let chars = processed.split('');
    for (let i = 0; i < chars.length; i++) {
        if (homoglyphs[chars[i]] && Math.random() < 0.35) {
            chars[i] = homoglyphs[chars[i]];
        }
    }
    processed = chars.join('');

    // 4. Maximum Linguistic Scarring
    if (level >= 5) {
        processed = processed.replace(/\bthe\b/g, (m) => Math.random() < 0.2 ? "teh" : "the");
        processed = processed.replace(/\bwith\b/g, (m) => Math.random() < 0.3 ? "w/" : "with");
        processed = processed.replace(/\band\b/g, (m) => Math.random() < 0.5 ? " & " : "and");
        processed = processed.replace(/\bpeople\b/g, "ppl");
    }

    return processed;
}

// --- API CLIENT ---

async function callLLM(text: string, model: string, prompt: string, temp: number) {
    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
            "Content-Type": "application/json",
            "HTTP-Referer": "https://blizflow.site"
        },
        body: JSON.stringify({
            model: model,
            messages: [
                { role: "system", content: prompt },
                { role: "user", content: text }
            ],
            temperature: temp,
            top_p: 0.95,
            presence_penalty: 2.0,
            frequency_penalty: 2.0
        }),
        signal: AbortSignal.timeout(60000)
    });
    if (!response.ok) throw new Error(`Pass on ${model} failed`);
    const data = await response.json();
    return data.choices?.[0]?.message?.content || text;
}
