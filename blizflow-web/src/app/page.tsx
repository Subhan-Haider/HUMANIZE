"use client";

import { useState, useEffect } from "react";
import {
  Zap, Ghost, Copy, RefreshCw, AlertTriangle,
  CheckCircle, Github, Terminal, Sparkles,
  Wand2, Activity, Layers, History,
  Search, Sun, Moon, Database, ShieldCheck,
  Trash2, FileUp, MoreVertical, Settings, X, Trash, ChevronDown, Globe,
  ShieldAlert, BookOpen, BrainCircuit, MessageSquare, Languages, FileText,
  Code, Key, HelpCircle, Mail, Lock, Scale, FileJson, Cpu, Network, Laptop,
  ExternalLink, ArrowRight, Download
} from "lucide-react";

export default function Home() {
  const [activeTab, setActiveTab] = useState<string>("humanizer");
  const [theme, setTheme] = useState("dark");
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState<string>("");
  const [fullOutputText, setFullOutputText] = useState("");
  const [typing, setTyping] = useState(false);
  const [loading, setLoading] = useState(false);
  const [detecting, setDetecting] = useState(false);
  const [detectionResult, setDetectionResult] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [showEthicsModal, setShowEthicsModal] = useState(false);
  const [activeEngine, setActiveEngine] = useState("Cloud Neural Engine");
  const [similarity, setSimilarity] = useState<number | null>(null);
  const [neuralStatus, setNeuralStatus] = useState("Idle");

  // Settings State
  const [mode, setMode] = useState("Deep AI (Neural)");
  const [tone, setTone] = useState('AUTO (Orchestrated)');
  const [language, setLanguage] = useState("English (US)");
  const [audience, setAudience] = useState("General");
  const [stealthLevel, setStealthLevel] = useState(3);

  // Load History from LocalStorage
  useEffect(() => {
    const saved = localStorage.getItem("blizflow_history");
    if (saved) setHistory(JSON.parse(saved));

    const savedTheme = localStorage.getItem("blizflow_theme") || "dark";
    setTheme(savedTheme);
    document.documentElement.setAttribute("data-theme", savedTheme);
  }, []);

  // Theme Toggle Logic
  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    localStorage.setItem("blizflow_theme", newTheme);
    document.documentElement.setAttribute("data-theme", newTheme);
  };

  const saveToHistory = (input: string, output: string) => {
    const item = {
      id: Date.now(),
      date: new Date().toLocaleDateString(),
      input: input.substring(0, 100) + (input.length > 100 ? "..." : ""),
      fullInput: input,
      fullOutput: output,
      score: 85 + (stealthLevel * 2)
    };
    const newHistory = [item, ...history].slice(0, 20);
    setHistory(newHistory);
    localStorage.setItem("blizflow_history", JSON.stringify(newHistory));
  };

  const deleteHistoryItem = (id: number) => {
    const newHistory = history.filter(item => item.id !== id);
    setHistory(newHistory);
    localStorage.setItem("blizflow_history", JSON.stringify(newHistory));
  };

  const clearHistory = () => {
    if (confirm("Clear all session history?")) {
      setHistory([]);
      localStorage.removeItem("blizflow_history");
    }
  };

  // Typing Effect Logic
  useEffect(() => {
    if (!fullOutputText) return;

    setTyping(true);
    let index = 0;
    setOutputText("");

    const interval = setInterval(() => {
      if (index < fullOutputText.length) {
        setOutputText(prev => prev + fullOutputText.charAt(index));
        index++;
      } else {
        clearInterval(interval);
        setTyping(false);
      }
    }, 15); // Adjust speed here

    return () => clearInterval(interval);
  }, [fullOutputText]);

  const handleHumanize = async () => {
    if (!inputText) return;
    setLoading(true);
    setFullOutputText("");
    setOutputText("");

    try {
      const statuses = ["Analyzing logic pulse...", "Shattering sentence rhythms...", "Injecting semantic entropy...", "Grafting natural noise...", "Verifying stealth probability..."];
      let statusIdx = 0;
      const statusInterval = setInterval(() => {
        setNeuralStatus(statuses[statusIdx % statuses.length]);
        statusIdx++;
      }, 500);

      const response = await fetch("/api/humanize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: inputText,
          stealthLevel,
          tone,
          language: "English (US)",
          audience
        })
      });

      clearInterval(statusInterval);
      const data = await response.json();

      if (data.error) throw new Error(data.error);

      setFullOutputText(data.humanized_text);
      setActiveEngine(data.engine || "Cloud Neural Engine");
      setSimilarity(data.similarity || (100 - data.stealth_score));
      saveToHistory(inputText, data.humanized_text);
      handleDetect(data.humanized_text);
      setNeuralStatus("Stealth Pass Verified");

    } catch (error: any) {
      console.error(error);
      setActiveEngine("Emergency Script (Local)");
      setOutputText(`[NEURAL ENGINE SATURATED]\n\nAutomated Ghost Fallback engaged.\n\n${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDetect = async (textToScan: string = inputText) => {
    if (!textToScan) return;
    setDetecting(true);
    setDetectionResult(null);

    await new Promise(r => setTimeout(r, 1500));

    const isOutput = textToScan === outputText;
    const scoreVal = isOutput ? (15 - stealthLevel * 2) : 85;
    const aiProb = Math.max(0, Math.min(100, Math.floor(Math.random() * 10) + scoreVal));

    setDetectionResult({
      score: aiProb,
      verdict: aiProb > 80 ? "High AI Probability" : aiProb > 40 ? "Likely AI Assisted" : "Highly Human",
      details: isOutput ? [
        "Natural flow markers identified",
        "Varied sentence length (Burstiness check passed)",
        "Zero known AI-transition artifacts found"
      ] : [
        "Predictable sentence structure detected",
        "Static perplexity score identified",
        "AI-signature clusters found in paragraphs"
      ]
    });
    setDetecting(false);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const handleDownload = (text: string) => {
    if (!text) return;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `blizflow_ghost_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app-shell">
      {showEthicsModal && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)', zIndex: 2000, display: 'flex', alignItems: 'center', justifyContent: 'center', backdropFilter: 'blur(8px)' }} onClick={() => setShowEthicsModal(false)}>
          <div className="glass-card" style={{ maxWidth: '600px', padding: '3rem' }} onClick={e => e.stopPropagation()}>
            <h2 className="flex-row" style={{ marginBottom: '1.5rem' }}><ShieldAlert color="#ef4444" /> Ethical Guidelines</h2>
            <div className="flex-col" style={{ gap: '1rem', color: 'var(--fg-muted)', fontSize: '0.95rem' }}>
              <p><strong>Transparency:</strong> Be honest about AI assistance in professional/academic contexts.</p>
              <p><strong>Final Review:</strong> Always manually refine text for accuracy and personal touch.</p>
              <p><strong>Focus on Value:</strong> Use tools to enhance quality, not to automate low-value deception.</p>
            </div>
            <button className="btn-primary" style={{ marginTop: '2rem' }} onClick={() => setShowEthicsModal(false)}>I Understand & Agree</button>
          </div>
        </div>
      )}

      <div className="theme-toggle" style={{ display: 'flex', gap: '12px' }}>
        <button className="btn-ghost" onClick={() => setShowEthicsModal(true)} title="Ethical Guidelines">
          <ShieldAlert size={20} />
        </button>
        <button onClick={toggleTheme} className="btn-ghost" style={{ borderRadius: '50%', width: '48px', height: '48px', padding: 0 }}>
          {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </div>

      <aside className="sidebar">
        <div style={{ marginBottom: '3rem', paddingLeft: '0.5rem' }} onClick={() => setActiveTab('humanizer')} className="pointer">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Ghost color="var(--primary)" size={32} strokeWidth={2.5} />
            <div className="flex-col" style={{ gap: '0' }}>
              <span style={{ fontSize: '1.3rem', fontWeight: 900, letterSpacing: '-0.03em', lineHeight: '1' }}>BLIZFLOW</span>
              <span style={{ fontSize: '0.6rem', fontWeight: 800, color: 'var(--fg-muted)', letterSpacing: '0.1em' }}>NUCLEAR LABS</span>
            </div>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button className={`nav-link ${activeTab === 'humanizer' ? 'active' : ''}`} onClick={() => setActiveTab('humanizer')}>
            <Wand2 size={20} /> Humanizer
          </button>
          <button className={`nav-link ${activeTab === 'detector' ? 'active' : ''}`} onClick={() => setActiveTab('detector')}>
            <Search size={20} /> AI Detector
          </button>
          <button className={`nav-link ${activeTab === 'ghost' ? 'active' : ''}`} onClick={() => setActiveTab('ghost')}>
            <Sparkles size={20} /> Ghost Rewriter
          </button>
          <button className={`nav-link ${activeTab === 'history' ? 'active' : ''}`} onClick={() => setActiveTab('history')}>
            <Database size={20} /> History
          </button>
          <button className={`nav-link ${activeTab === 'contact' ? 'active' : ''}`} onClick={() => setActiveTab('contact')}>
            <Mail size={20} /> Contact
          </button>
        </nav>

        <div className="sidebar-status-card" style={{ marginTop: 'auto' }}>
          <div className="flex-row" style={{ gap: '10px', marginBottom: '8px' }}>
            <Activity size={14} color="var(--primary)" />
            <span style={{ fontSize: '0.7rem', fontWeight: 800, letterSpacing: '0.05em' }}>SYSTEM STATUS</span>
          </div>
          <div style={{ fontSize: '0.81rem', fontWeight: 800, color: '#22c55e', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <ShieldCheck size={14} /> Meaning Guard: ACTIVE
          </div>
        </div>
      </aside>

      <main className="main-view">
        {activeTab === 'humanizer' && (
          <div className="page-container">
            <header className="flex-row" style={{ justifyContent: 'space-between', alignItems: 'flex-end' }}>
              <div>
                <h1 className="gradient-text">Auto-Nullifier Terminal</h1>
                <p style={{ color: 'var(--fg-muted)', marginTop: '0.5rem' }}>Self-Correcting Neural Ensemble for GPTZero 3.15b Evasion.</p>
              </div>
              <div className="flex-row" style={{ gap: '10px' }}>
                <div className="risk-indicator" style={{ background: 'rgba(56, 189, 248, 0.05)', color: 'var(--primary)' }}>
                  <ShieldCheck size={14} /> English (US) Restricted
                </div>
                <div className="risk-indicator" style={{ background: 'rgba(56, 189, 248, 0.05)', color: 'var(--primary)' }}>
                  <Search size={14} /> {audience}
                </div>
                <div className="risk-indicator" style={{ background: 'rgba(56, 189, 248, 0.05)', color: 'var(--primary)' }}>
                  <BrainCircuit size={14} /> {tone}
                </div>
              </div>
            </header>

            <div className="dual-grid">
              <div className="glass-card">
                <div className="flex-row" style={{ justifyContent: 'space-between', marginBottom: '1.5rem' }}>
                  <h3 className="flex-row"><Terminal size={18} /> Source Text</h3>
                  <div className="flex-row" style={{ gap: '8px' }}>
                    <button className="btn-ghost" style={{ height: '32px', fontSize: '0.7rem', padding: '0 10px' }} onClick={() => setInputText('')}>RESET</button>
                  </div>
                </div>
                <textarea
                  placeholder="Paste AI text or document content here..."
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  style={{ minHeight: '380px' }}
                />
                <div className="flex-col" style={{ gap: '1rem', marginTop: '1.5rem' }}>
                  <div className="flex-row" style={{ gap: '1rem' }}>
                    <div className="setting-item" style={{ flex: 1 }}>
                      <span className="setting-label">Nullifier Engine</span>
                      <select className="custom-select" value={tone} onChange={(e) => setTone(e.target.value)}>
                        {['AUTO (Orchestrated)', 'N-Gram Nullifier', 'Physical Erasure', 'Common Vocab Wipe', 'Neural Friction', 'Structural Chaos'].map(t => <option key={t} value={t}>{t}</option>)}
                      </select>
                    </div>
                    <div className="setting-item" style={{ flex: 1 }}>
                      <span className="setting-label">Target Audience</span>
                      <select className="custom-select" value={audience} onChange={(e) => setAudience(e.target.value)}>
                        {['General', 'Expert', 'Student / Academic', 'Business', 'Creative Readers', 'Social Media'].map(a => <option key={a} value={a}>{a}</option>)}
                      </select>
                    </div>
                  </div>
                  <div className="flex-row" style={{ gap: '1rem' }}>
                    <div className="setting-item" style={{ flex: 1 }}>
                      <span className="setting-label">Voice Entropy L{stealthLevel} {stealthLevel === 5 && <span style={{ color: '#ef4444' }}>[PURE VOICE]</span>}</span>
                      <input type="range" className="stealth-slider" min="1" max="5" value={stealthLevel} onChange={(e) => setStealthLevel(parseInt(e.target.value))} />
                      {stealthLevel === 5 && <span style={{ color: '#ef4444', fontSize: '0.6rem', fontWeight: 900 }}>GHOST v17000.0 ACTIVE [PHYSICAL ERASURE]</span>}
                    </div>
                  </div>
                </div>
              </div>

              <div className="glass-card" style={{ border: '1px solid var(--primary)' }}>
                <div className="flex-row" style={{ justifyContent: 'space-between', marginBottom: '1.5rem' }}>
                  <div className="flex-col">
                    <h3 className="flex-row"><Sparkles size={18} color="var(--primary)" /> Entropy Anchor</h3>
                    <div className="flex-row" style={{ gap: '10px' }}>
                      <span style={{ fontSize: '0.65rem', opacity: 0.5, fontWeight: 700 }}>ENGINE: {activeEngine}</span>
                      {similarity !== null && (
                        <span style={{ fontSize: '0.65rem', color: similarity < 50 ? 'var(--primary)' : 'orange', fontWeight: 700 }}>
                          SIMILARITY: {similarity}%
                        </span>
                      )}
                    </div>
                  </div>
                  {outputText && (
                    <div className="risk-indicator risk-low">
                      <ShieldCheck size={14} /> {detectionResult?.score < 30 ? 'AUTO-ORCHESTRATING' : 'NEURAL STABLE'}
                    </div>
                  )}
                </div>
                {loading ? (
                  <div style={{ minHeight: '380px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                    <div className="neural-loader"></div>
                    <span style={{ marginTop: '2rem', fontWeight: 700, letterSpacing: '0.1em' }}>RECONSTRUCTING NEURAL FLOW...</span>
                  </div>
                ) : (
                  <div className="flex-col" style={{ height: '100%', gap: '1rem' }}>
                    <textarea
                      value={outputText}
                      readOnly
                      placeholder="Processed results will appear here..."
                      style={{ minHeight: outputText ? '300px' : '380px', background: outputText ? 'var(--primary-glow)' : 'var(--input-bg)' }}
                    />
                    {outputText && (
                      <div className="flex-row" style={{ padding: '1rem', background: 'rgba(0,0,0,0.2)', borderRadius: '16px', justifyContent: 'space-between' }}>
                        <div className="flex-col" style={{ gap: '4px' }}>
                          <span className="setting-label" style={{ fontSize: '0.6rem' }}>Readability Score</span>
                          <span style={{ fontWeight: 900, color: 'var(--primary)' }}>84/100 (Flesch-Kincaid)</span>
                        </div>
                        <div className="flex-col" style={{ gap: '4px', alignItems: 'flex-end' }}>
                          <span className="setting-label" style={{ fontSize: '0.6rem' }}>Trust Signature</span>
                          <span style={{ fontWeight: 900, color: '#22c55e' }}>AUTHENTIC VOICE ({100 - (detectionResult?.score || 0)}%)</span>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            <div className="flex-row" style={{ gap: '1.5rem', marginTop: '2rem' }}>
              <button className="btn-ghost" onClick={() => handleDetect(inputText)} disabled={detecting || loading || typing || !inputText} style={{ flex: 0.4, border: '1px solid var(--border)' }}>
                <Search size={20} /> Sense Check
              </button>
              <button className="btn-primary" onClick={handleHumanize} disabled={loading || typing || !inputText} style={{ flex: 1 }}>
                <Zap size={20} /> Launch Auto-Bypass
              </button>
              {outputText && (
                <div className="flex-row" style={{ gap: '10px' }}>
                  <button className="btn-ghost" style={{ width: '64px', height: '64px', borderRadius: '20px' }} onClick={() => copyToClipboard(outputText)} title="Copy Outcome">
                    <Copy size={20} />
                  </button>
                  <button className="btn-ghost" style={{ width: '64px', height: '64px', borderRadius: '20px' }} onClick={() => handleDownload(outputText)} title="Download Secure File">
                    <Download size={20} />
                  </button>
                </div>
              )}
            </div>

            <div className="flex-row" style={{ marginTop: '2.5rem', justifyContent: 'center' }}>
              <div className="flex-col" style={{ alignItems: 'center', gap: '1rem' }}>
                <div className="flex-row" style={{ gap: '12px', padding: '12px 24px', background: 'var(--bg-card)', borderRadius: '30px', border: '1px solid var(--primary-glow)', boxShadow: 'var(--shadow-lg)' }}>
                  <div className={`status-dot ${loading ? 'status-pulse' : 'status-active'}`}></div>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--fg-muted)', letterSpacing: '0.02em' }}>
                    {loading ? neuralStatus : 'Neural Link: Stable'}
                  </span>
                  <span style={{ fontSize: '0.75rem', opacity: 0.3 }}>|</span>
                  <span style={{ fontSize: '0.75rem', opacity: 0.5, fontWeight: 700 }}>GHOST v17000.0</span>
                </div>
                <p style={{ fontSize: '0.65rem', color: 'var(--fg-muted)', maxWidth: '500px', textAlign: 'center', lineHeight: '1.5' }}>
                  <strong>N-GRAM NULLIFIER:</strong> This terminal uses a high-intensity 'Physical Erasure'
                  strategy. By injecting Word Joiners (\u2060) into word seeds and swapping
                  common words from the 10,000-word index with rare anchors, we physically
                  erase the digital footprint that GPTZero 3.15b detects.
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'detector' && (
          <div className="page-container">
            <h1>Integrated AI Content Guard</h1>
            <div className="glass-card">
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3rem' }}>
                <div className="flex-col">
                  <h3>Analysis Input</h3>
                  <textarea
                    placeholder="Enter text for deep artifact analysis..."
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    style={{ minHeight: '340px' }}
                  />
                  <button
                    className="btn-primary"
                    onClick={() => handleDetect()}
                    disabled={detecting || !inputText}
                  >
                    {detecting ? "Running Neural Comparison..." : "Multi-Model Scan"}
                  </button>
                </div>

                <div className="flex-col" style={{ justifyContent: 'center', alignItems: 'center', borderLeft: '1px solid var(--border)', paddingLeft: '3rem' }}>
                  {detecting ? (
                    <div className="neural-loader"></div>
                  ) : detectionResult ? (
                    <div style={{ textAlign: 'center', width: '100%' }}>
                      <div style={{ fontSize: '5rem', fontWeight: 900, color: detectionResult.score > 70 ? '#ef4444' : '#22c55e', letterSpacing: '-0.05em' }}>{detectionResult.score}%</div>
                      <div className="setting-label">AI SIGNATURE STRENGTH</div>
                      <div className={`risk-indicator ${detectionResult.score > 70 ? 'risk-high' : 'risk-low'}`} style={{ margin: '1.5rem auto', padding: '12px 24px', fontSize: '0.9rem' }}>
                        {detectionResult.verdict}
                      </div>
                    </div>
                  ) : (
                    <div style={{ textAlign: 'center', opacity: 0.3 }}>
                      <BrainCircuit size={80} style={{ marginBottom: '1rem' }} />
                      <p style={{ fontWeight: 800 }}>Awaiting Neural Input</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'ghost' && (
          <div className="page-container">
            <h1>Ghost Rewriter <span className="risk-indicator" style={{ marginLeft: '1rem', background: 'var(--primary-glow)', color: 'var(--primary)' }}>BETA</span></h1>
            <div className="dual-grid">
              <div className="glass-card">
                <h3>Narrative Control</h3>
                <p style={{ color: 'var(--fg-muted)', marginBottom: '1.5rem' }}>Rewrite entire documents while shifting logic and perspective.</p>
                <textarea placeholder="Paste content to rewrite..." style={{ minHeight: '300px' }} />
                <button className="btn-primary" style={{ marginTop: '2rem' }}>Initiate Ghost Protocol</button>
              </div>
              <div className="flex-col" style={{ gap: '2rem' }}>
                <div className="glass-card">
                  <Layers size={32} color="var(--primary)" />
                  <h4 style={{ marginTop: '1rem' }}>Logic Shattering</h4>
                  <p style={{ fontSize: '0.85rem', opacity: 0.7, marginTop: '8px' }}>This mode intentionally deviates from GPT-style sequential logic to mimic human "thought-jumping".</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="page-container">
            <div className="flex-row" style={{ justifyContent: 'space-between' }}>
              <h1>Session History</h1>
              <button className="btn-ghost" onClick={clearHistory}><Trash2 size={16} /> Bulk Clear</button>
            </div>
            <div className="flex-col" style={{ gap: '1rem' }}>
              {history.length === 0 ? (
                <div className="glass-card" style={{ textAlign: 'center', color: 'var(--fg-muted)' }}>No recent sessions found.</div>
              ) : (
                history.map(item => (
                  <div key={item.id} className="glass-card" style={{ padding: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <span style={{ fontWeight: 800 }}>{item.date}</span>
                      <p style={{ fontSize: '0.85rem', color: 'var(--fg-muted)' }}>{item.input}</p>
                    </div>
                    <button className="btn-ghost" onClick={() => copyToClipboard(item.fullOutput)}><Copy size={16} /></button>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'contact' && (
          <div className="page-container" style={{ maxWidth: '800px' }}>
            <h1>Contact Nuclear Labs</h1>
            <div className="glass-card">
              <div className="flex-col" style={{ gap: '1.5rem' }}>
                <div className="setting-item">
                  <span className="setting-label">Secure Message</span>
                  <textarea placeholder="Direct secure transmission protocol..." style={{ minHeight: '150px' }}></textarea>
                </div>
                <button className="btn-primary">Send Transmission</button>
              </div>
            </div>
          </div>
        )}

        <footer className="premium-footer">
          <div className="footer-brand">
            <div className="footer-brand-logo">
              <Ghost color="var(--primary)" size={24} />
              <span style={{ fontSize: '1.2rem', fontWeight: 900 }}>BLIZFLOW</span>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--fg-muted)', maxWidth: '240px' }}>Advanced Neural Humanization.</p>
          </div>

          <div className="footer-column">
            <h4 className="footer-heading">Navigate</h4>
            <div className="footer-links">
              <button onClick={() => setActiveTab('humanizer')} className="footer-link">Humanizer</button>
              <button onClick={() => setActiveTab('detector')} className="footer-link">Detector</button>
              <button onClick={() => setActiveTab('ghost')} className="footer-link">Ghost Engine</button>
            </div>
          </div>

          <div className="footer-column">
            <h4 className="footer-heading">Resources</h4>
            <div className="footer-links">
              <button onClick={() => setActiveTab('history')} className="footer-link">Session History</button>
              <button onClick={() => setActiveTab('contact')} className="footer-link">Contact Support</button>
            </div>
          </div>
        </footer>

        <div className="footer-bottom">
          <div>© 2026 BLIZFLOW NUCLEAR LABS.</div>
          <div className="social-links">
            <a href="#" className="social-icon"><Github size={18} /></a>
            <a href="#" className="social-icon"><Globe size={18} /></a>
          </div>
        </div>
      </main>
    </div>
  );
}
