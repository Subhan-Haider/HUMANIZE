# BlizFlow AI (Web Edition)

This is a standalone, modern **Next.js** web application for BlizFlow AI. 
It is designed to be "Serverless" and "Static-First", meaning it can run entirely in the browser by connecting directly to the **OpenRouter API**, without needing the local Python backend.

## 🚀 Features
- **Pure Web Stack**: Built with Next.js 15, React, and Vanilla CSS (Premium Design System).
- **Serverless Humanization**: Connects directly to LLMs via OpenRouter.
- **Responsive Design**: Fully optimized for Desktop, Tablet, and Mobile.
- **Stealth Mode**: Implements client-side prompt engineering to mimic the Python backend's logic.

## 🛠️ Getting Started

### 1. Prerequisites
- Node.js (v18 or higher)
- An API Key from [OpenRouter](https://openrouter.ai)

### 2. Installation
```bash
npm install
```

### 3. Configuration (Optional)
Create a `.env.local` file to auto-load your API Key:
```env
NEXT_PUBLIC_OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### 4. Run Locally
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000)

## 🔌 Architecture
This web app operates in two modes:

1.  **Standalone (Default):** Uses the browser to fetch data from OpenRouter. No Python required.
2.  **Hybrid (Optional):** If you run the global `api.py` in the parent directory (`python ../api.py`), this web app will detect it and offload processing to the Python engine for advanced features (like NLTK pattern breaking).

## 📦 Deployment
This app is ready for Vercel, Netlify, or any static hosting.
```bash
npm run build
```
