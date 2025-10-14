# URL Attack Detection System - Modern Tech Stack Implementation

## 🚀 Technology Migration: Python → Modern Web Stack

Transform your existing Python-based URL Attack Detection System into a cutting-edge web application using:

- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: Node.js + Express.js + TypeScript
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **Real-time**: Supabase Realtime
- **Deployment**: Vercel (Frontend) + Railway/Render (Backend)

---

## 🏗️ Modern Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   React App     │  │  Tailwind CSS   │  │ TypeScript   │ │
│  │   (Components)  │  │   (Styling)     │  │ (Type Safety)│ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND API LAYER                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Express.js    │  │    Node.js      │  │ TypeScript   │ │
│  │  (REST Routes)  │  │   (Runtime)     │  │(Controllers) │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │ SQL Queries
┌─────────────────────────────────────────────────────────────┐
│                    DATA & AUTH LAYER                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Supabase      │  │  PostgreSQL     │  │   Realtime   │ │
│  │   (Auth/API)    │  │   (Database)    │  │ (Live Updates)│ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
url-attack-detector-modern/
├── frontend/                          # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/                # Reusable UI Components
│   │   │   ├── Dashboard/
│   │   │   │   ├── StatsCard.tsx
│   │   │   │   ├── AttackChart.tsx
│   │   │   │   └── RecentAttacks.tsx
│   │   │   ├── Analyzer/
│   │   │   │   ├── UrlInput.tsx
│   │   │   │   ├── ResultDisplay.tsx
│   │   │   │   └── ThreatIndicator.tsx
│   │   │   ├── Layout/
│   │   │   │   ├── Navbar.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   └── Common/
│   │   │       ├── Button.tsx
│   │   │       ├── Modal.tsx
│   │   │       └── LoadingSpinner.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Analyzer.tsx
│   │   │   ├── AttackDatabase.tsx
│   │   │   └── Reports.tsx
│   │   ├── hooks/                     # Custom React Hooks
│   │   │   ├── useAttackDetection.ts
│   │   │   ├── useRealtime.ts
│   │   │   └── useStats.ts
│   │   ├── services/                  # API Communication
│   │   │   ├── api.ts
│   │   │   ├── supabase.ts
│   │   │   └── attackDetector.ts
│   │   ├── types/                     # TypeScript Definitions
│   │   │   ├── attack.types.ts
│   │   │   ├── api.types.ts
│   │   │   └── common.types.ts
│   │   ├── utils/
│   │   │   ├── constants.ts
│   │   │   ├── helpers.ts
│   │   │   └── validators.ts
│   │   └── styles/
│   │       └── globals.css            # Tailwind imports
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── backend/                           # Node.js + Express Backend
│   ├── src/
│   │   ├── controllers/               # Route Controllers
│   │   │   ├── attackController.ts
│   │   │   ├── statsController.ts
│   │   │   └── exportController.ts
│   │   ├── services/                  # Business Logic
│   │   │   ├── AttackDetectorService.ts
│   │   │   ├── DatabaseService.ts
│   │   │   └── AnalyticsService.ts
│   │   ├── models/                    # Data Models
│   │   │   ├── Attack.ts
│   │   │   └── Statistics.ts
│   │   ├── middleware/                # Express Middleware
│   │   │   ├── auth.ts
│   │   │   ├── validation.ts
│   │   │   └── rateLimit.ts
│   │   ├── routes/                    # API Routes
│   │   │   ├── attacks.ts
│   │   │   ├── analytics.ts
│   │   │   └── export.ts
│   │   ├── types/                     # Shared TypeScript Types
│   │   │   └── index.ts
│   │   ├── utils/
│   │   │   ├── logger.ts
│   │   │   ├── errorHandler.ts
│   │   │   └── patterns.ts
│   │   └── app.ts                     # Express App Setup
│   ├── package.json
│   └── tsconfig.json
│
├── shared/                            # Shared TypeScript Types
│   └── types/
│       ├── attack.types.ts
│       └── api.types.ts
│
└── docs/
    ├── API.md
    └── DEPLOYMENT.md
```

---

## 🎨 Frontend Implementation (React + TypeScript + Tailwind)

### **1. Main Dashboard Component**

```typescript
// frontend/src/pages/Dashboard.tsx
import React, { useEffect, useState } from 'react';
import { useStats } from '../hooks/useStats';
import { useRealtime } from '../hooks/useRealtime';
import StatsCard from '../components/Dashboard/StatsCard';
import AttackChart from '../components/Dashboard/AttackChart';
import RecentAttacks from '../components/Dashboard/RecentAttacks';
import { AttackStats } from '../types/attack.types';

const Dashboard: React.FC = () => {
  const { stats, loading, error } = useStats();
  const { isConnected } = useRealtime();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            🛡️ URL Attack Detection Dashboard
          </h1>
          <p className="text-gray-600 mt-2">
            Real-time monitoring and analysis of web security threats
          </p>
          {isConnected && (
            <div className="inline-flex items-center mt-4 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
              Live Updates Active
            </div>
          )}
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Statistics Cards */}
            <div className="lg:col-span-3">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatsCard
                  title="Total Attacks"
                  value={stats?.total_attacks || 0}
                  icon="⚠️"
                  trend="+12%"
                  className="bg-red-50 border-red-200"
                />
                <StatsCard
                  title="SQL Injections"
                  value={stats?.attack_by_type?.sql_injection || 0}
                  icon="💉"
                  trend="+8%"
                  className="bg-orange-50 border-orange-200"
                />
                <StatsCard
                  title="XSS Attempts"
                  value={stats?.attack_by_type?.xss || 0}
                  icon="🎭"
                  trend="+15%"
                  className="bg-yellow-50 border-yellow-200"
                />
                <StatsCard
                  title="Clean URLs"
                  value={stats?.clean_urls || 0}
                  icon="✅"
                  trend="+5%"
                  className="bg-green-50 border-green-200"
                />
              </div>
            </div>

            {/* Attack Trends Chart */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4">Attack Trends</h3>
                <AttackChart data={stats?.trends} />
              </div>
            </div>

            {/* Recent Attacks */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-4">Recent Threats</h3>
                <RecentAttacks attacks={stats?.recent_attacks} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
```

### **2. URL Analyzer Component**

```typescript
// frontend/src/pages/Analyzer.tsx
import React, { useState } from 'react';
import { useAttackDetection } from '../hooks/useAttackDetection';
import UrlInput from '../components/Analyzer/UrlInput';
import ResultDisplay from '../components/Analyzer/ResultDisplay';
import ThreatIndicator from '../components/Analyzer/ThreatIndicator';
import { AnalysisResult } from '../types/attack.types';

const Analyzer: React.FC = () => {
  const [url, setUrl] = useState<string>('');
  const { analyzeUrl, loading, result, error } = useAttackDetection();

  const handleAnalyze = async () => {
    if (!url.trim()) return;
    await analyzeUrl(url);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🔍 URL Security Analyzer
          </h1>
          <p className="text-xl text-gray-600">
            Enter a URL to check for potential security threats
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <UrlInput
            value={url}
            onChange={setUrl}
            onAnalyze={handleAnalyze}
            loading={loading}
            placeholder="https://example.com/path?param=value"
          />
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-6">
            {/* Threat Level Indicator */}
            <ThreatIndicator
              isMalicious={result.is_malicious}
              confidence={result.confidence}
              severity={result.severity}
            />

            {/* Detailed Results */}
            <ResultDisplay result={result} />
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <div className="text-red-400 mr-3">❌</div>
              <div>
                <h3 className="text-red-800 font-medium">Analysis Error</h3>
                <p className="text-red-600 text-sm mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Sample URLs for Testing */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-semibold text-blue-800 mb-3">🧪 Test URLs</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <h4 className="font-medium text-blue-700 mb-2">SQL Injection:</h4>
              <button
                onClick={() => setUrl("http://example.com/login?user=' OR '1'='1")}
                className="text-blue-600 hover:text-blue-800 block w-full text-left p-2 rounded hover:bg-blue-100"
              >
                http://example.com/login?user=' OR '1'='1
              </button>
            </div>
            <div>
              <h4 className="font-medium text-blue-700 mb-2">XSS Attack:</h4>
              <button
                onClick={() => setUrl("http://example.com/search?q=<script>alert('XSS')</script>")}
                className="text-blue-600 hover:text-blue-800 block w-full text-left p-2 rounded hover:bg-blue-100"
              >
                http://example.com/search?q=&lt;script&gt;alert('XSS')&lt;/script&gt;
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analyzer;
```

### **3. Custom Hooks for State Management**

```typescript
// frontend/src/hooks/useAttackDetection.ts
import { useState } from 'react';
import { api } from '../services/api';
import { AnalysisResult } from '../types/attack.types';

export const useAttackDetection = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const analyzeUrl = async (url: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.post<AnalysisResult>('/analyze', { url });
      setResult(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
  };

  return {
    loading,
    result,
    error,
    analyzeUrl,
    reset
  };
};
```

```typescript
// frontend/src/hooks/useRealtime.ts
import { useEffect, useState } from 'react';
import { supabase } from '../services/supabase';
import { RealtimeChannel } from '@supabase/supabase-js';

export const useRealtime = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [latestAttack, setLatestAttack] = useState(null);

  useEffect(() => {
    let channel: RealtimeChannel;

    const setupRealtime = async () => {
      channel = supabase
        .channel('attacks')
        .on(
          'postgres_changes',
          {
            event: 'INSERT',
            schema: 'public',
            table: 'attacks'
          },
          (payload) => {
            setLatestAttack(payload.new as any);
          }
        )
        .subscribe((status) => {
          setIsConnected(status === 'SUBSCRIBED');
        });
    };

    setupRealtime();

    return () => {
      if (channel) {
        supabase.removeChannel(channel);
      }
    };
  }, []);

  return {
    isConnected,
    latestAttack
  };
};
```

---

## 🚀 Backend Implementation (Node.js + Express + TypeScript)

### **1. Main Express Application**

```typescript
// backend/src/app.ts
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { createClient } from '@supabase/supabase-js';
import attackRoutes from './routes/attacks';
import analyticsRoutes from './routes/analytics';
import exportRoutes from './routes/export';
import { errorHandler } from './middleware/errorHandler';
import { logger } from './utils/logger';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});
app.use('/api/', limiter);

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Request logging
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.path} - ${req.ip}`);
  next();
});

// Routes
app.use('/api/attacks', attackRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/export', exportRoutes);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version 
  });
});

// Error handling
app.use(errorHandler);

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  logger.info(`🚀 Server running on port ${PORT}`);
  logger.info(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
});

export default app;
```

### **2. Attack Detection Service**

```typescript
// backend/src/services/AttackDetectorService.ts
import { AttackPattern, AnalysisResult, DetectedAttack } from '../types';
import { attackPatterns } from '../utils/patterns';
import { logger } from '../utils/logger';

export class AttackDetectorService {
  private patterns: AttackPattern[] = attackPatterns;

  constructor() {
    logger.info(`🛡️  Attack detector initialized with ${this.patterns.length} patterns`);
  }

  async analyzeUrl(url: string, sourceIp?: string): Promise<AnalysisResult> {
    const startTime = Date.now();
    
    try {
      // Preprocess URL
      const processedData = this.preprocessUrl(url);
      
      // Detect attacks
      const detectedAttacks = this.detectAttacks(processedData);
      
      // Calculate overall assessment
      const result: AnalysisResult = {
        url,
        is_malicious: detectedAttacks.length > 0,
        attacks_detected: detectedAttacks,
        severity: this.calculateOverallSeverity(detectedAttacks),
        confidence: this.calculateOverallConfidence(detectedAttacks),
        analysis_time_ms: Date.now() - startTime,
        processed_at: new Date().toISOString(),
        source_ip: sourceIp
      };

      logger.info(`🔍 Analyzed URL: ${url} - ${result.is_malicious ? 'THREAT' : 'CLEAN'} (${result.analysis_time_ms}ms)`);
      
      return result;
    } catch (error) {
      logger.error(`❌ Analysis failed for URL: ${url}`, error);
      throw new Error('URL analysis failed');
    }
  }

  private preprocessUrl(url: string): ProcessedUrl {
    try {
      // URL decoding (handle multiple encoding layers)
      let decoded = decodeURIComponent(url);
      let doubleDecoded = decodeURIComponent(decoded);
      
      // Parse URL components
      const urlObj = new URL(decoded);
      
      return {
        original: url,
        decoded: decoded,
        double_decoded: doubleDecoded,
        protocol: urlObj.protocol,
        hostname: urlObj.hostname,
        pathname: urlObj.pathname,
        search: urlObj.search,
        searchParams: Object.fromEntries(urlObj.searchParams.entries())
      };
    } catch (error) {
      // If URL parsing fails, work with the raw string
      return {
        original: url,
        decoded: url,
        double_decoded: url,
        protocol: '',
        hostname: '',
        pathname: '',
        search: '',
        searchParams: {}
      };
    }
  }

  private detectAttacks(urlData: ProcessedUrl): DetectedAttack[] {
    const detectedAttacks: DetectedAttack[] = [];

    for (const pattern of this.patterns) {
      const regex = new RegExp(pattern.pattern, 'gi');
      const testString = urlData.decoded;

      if (regex.test(testString)) {
        const confidence = this.calculateConfidence(pattern, urlData);
        const severity = this.determineSeverity(pattern.attack_type, confidence);

        detectedAttacks.push({
          type: pattern.attack_type,
          pattern_matched: pattern.pattern,
          confidence,
          severity,
          description: pattern.description,
          matched_text: this.extractMatchedText(testString, regex)
        });
      }
    }

    return detectedAttacks;
  }

  private calculateConfidence(pattern: AttackPattern, urlData: ProcessedUrl): number {
    let confidence = pattern.base_confidence || 70;

    // Boost for multiple suspicious indicators
    const suspiciousChars = this.countSuspiciousCharacters(urlData.decoded);
    if (suspiciousChars > 3) confidence += 15;

    // Higher confidence for known dangerous patterns
    const dangerousKeywords = ['DROP', 'UNION', 'SELECT', '<script>', 'javascript:', '../'];
    if (dangerousKeywords.some(keyword => pattern.pattern.includes(keyword))) {
      confidence += 20;
    }

    // Encoding suggests obfuscation
    if (urlData.decoded !== urlData.double_decoded) {
      confidence += 10;
    }

    // Length-based heuristics
    if (urlData.decoded.length > 1000) confidence += 5;

    return Math.min(confidence, 99);
  }

  private determineSeverity(attackType: string, confidence: number): 'low' | 'medium' | 'high' | 'critical' {
    const criticalAttacks = ['sql_injection', 'command_injection', 'rfi'];
    const highAttacks = ['xss', 'directory_traversal', 'lfi'];

    if (criticalAttacks.includes(attackType) && confidence >= 80) return 'critical';
    if (criticalAttacks.includes(attackType) || (highAttacks.includes(attackType) && confidence >= 85)) return 'high';
    if (confidence >= 70) return 'medium';
    return 'low';
  }

  private calculateOverallSeverity(attacks: DetectedAttack[]): 'low' | 'medium' | 'high' | 'critical' {
    if (attacks.length === 0) return 'low';
    
    const severities = attacks.map(a => a.severity);
    if (severities.includes('critical')) return 'critical';
    if (severities.includes('high')) return 'high';
    if (severities.includes('medium')) return 'medium';
    return 'low';
  }

  private calculateOverallConfidence(attacks: DetectedAttack[]): number {
    if (attacks.length === 0) return 0;
    return Math.max(...attacks.map(a => a.confidence));
  }

  private countSuspiciousCharacters(url: string): number {
    const suspiciousChars = /[<>'";\(\){}[\]\\|&$`]/g;
    return (url.match(suspiciousChars) || []).length;
  }

  private extractMatchedText(text: string, regex: RegExp): string {
    const match = text.match(regex);
    return match ? match[0] : '';
  }
}

// Types
interface ProcessedUrl {
  original: string;
  decoded: string;
  double_decoded: string;
  protocol: string;
  hostname: string;
  pathname: string;
  search: string;
  searchParams: Record<string, string>;
}
```

### **3. Attack Controller with Database Integration**

```typescript
// backend/src/controllers/attackController.ts
import { Request, Response } from 'express';
import { AttackDetectorService } from '../services/AttackDetectorService';
import { DatabaseService } from '../services/DatabaseService';
import { logger } from '../utils/logger';
import { validateUrl } from '../utils/validators';

const attackDetector = new AttackDetectorService();
const db = new DatabaseService();

export const analyzeUrl = async (req: Request, res: Response) => {
  try {
    const { url } = req.body;
    
    // Validation
    if (!url || typeof url !== 'string') {
      return res.status(400).json({ 
        error: 'URL is required and must be a string' 
      });
    }

    if (!validateUrl(url)) {
      return res.status(400).json({ 
        error: 'Invalid URL format' 
      });
    }

    if (url.length > 2048) {
      return res.status(400).json({ 
        error: 'URL too long (max 2048 characters)' 
      });
    }

    // Analyze the URL
    const sourceIp = req.ip || req.connection.remoteAddress || '127.0.0.1';
    const result = await attackDetector.analyzeUrl(url, sourceIp);

    // Save to database (Critical - this ensures dashboard integration!)
    const attackRecord = {
      url: result.url,
      source_ip: result.source_ip || sourceIp,
      attack_type: result.attacks_detected[0]?.type || 'legitimate',
      is_malicious: result.is_malicious,
      severity: result.severity,
      confidence: result.confidence,
      pattern_matched: result.attacks_detected[0]?.pattern_matched || '',
      user_agent: req.get('User-Agent') || '',
      additional_data: JSON.stringify({
        attacks_detected: result.attacks_detected,
        analysis_time_ms: result.analysis_time_ms
      })
    };

    await db.insertAttack(attackRecord);

    // Return analysis result
    res.json(result);

  } catch (error) {
    logger.error('Attack analysis failed:', error);
    res.status(500).json({ 
      error: 'Internal server error during analysis' 
    });
  }
};

export const getAttackHistory = async (req: Request, res: Response) => {
  try {
    const { page = 1, limit = 50, attack_type, severity } = req.query;
    
    const filters = {
      attack_type: attack_type as string,
      severity: severity as string
    };

    const attacks = await db.getAttacks({
      page: Number(page),
      limit: Number(limit),
      filters
    });

    res.json(attacks);
  } catch (error) {
    logger.error('Failed to fetch attack history:', error);
    res.status(500).json({ error: 'Failed to fetch attack history' });
  }
};

export const getAttackById = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const attack = await db.getAttackById(id);
    
    if (!attack) {
      return res.status(404).json({ error: 'Attack not found' });
    }

    res.json(attack);
  } catch (error) {
    logger.error('Failed to fetch attack:', error);
    res.status(500).json({ error: 'Failed to fetch attack' });
  }
};
```

---

## 🗄️ Supabase Database Schema

### **1. Database Tables**

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable Row Level Security
ALTER DATABASE postgres SET row_security = on;

-- Attacks table (main data storage)
CREATE TABLE attacks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    url TEXT NOT NULL,
    source_ip INET,
    attack_type TEXT NOT NULL DEFAULT 'legitimate',
    is_malicious BOOLEAN DEFAULT FALSE,
    severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')) DEFAULT 'low',
    confidence DECIMAL(5,2) CHECK (confidence >= 0 AND confidence <= 100),
    pattern_matched TEXT,
    user_agent TEXT,
    additional_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Attack patterns table (configurable patterns)
CREATE TABLE attack_patterns (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    attack_type TEXT NOT NULL,
    pattern TEXT NOT NULL,
    description TEXT,
    base_confidence INTEGER DEFAULT 70,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Statistics cache table (for dashboard performance)
CREATE TABLE attack_statistics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE,
    total_attacks INTEGER DEFAULT 0,
    total_malicious INTEGER DEFAULT 0,
    attack_type_breakdown JSONB,
    severity_breakdown JSONB,
    hourly_breakdown JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(date)
);

-- Indexes for performance
CREATE INDEX idx_attacks_created_at ON attacks(created_at DESC);
CREATE INDEX idx_attacks_attack_type ON attacks(attack_type);
CREATE INDEX idx_attacks_is_malicious ON attacks(is_malicious);
CREATE INDEX idx_attacks_severity ON attacks(severity);
CREATE INDEX idx_attacks_source_ip ON attacks(source_ip);

-- Full-text search on URLs
CREATE INDEX idx_attacks_url_fts ON attacks USING gin(to_tsvector('english', url));

-- Trigger to update statistics
CREATE OR REPLACE FUNCTION update_attack_statistics()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO attack_statistics (
        date,
        total_attacks,
        total_malicious,
        attack_type_breakdown,
        severity_breakdown
    )
    VALUES (
        CURRENT_DATE,
        1,
        CASE WHEN NEW.is_malicious THEN 1 ELSE 0 END,
        jsonb_build_object(NEW.attack_type, 1),
        jsonb_build_object(NEW.severity, 1)
    )
    ON CONFLICT (date)
    DO UPDATE SET
        total_attacks = attack_statistics.total_attacks + 1,
        total_malicious = attack_statistics.total_malicious + 
                         CASE WHEN NEW.is_malicious THEN 1 ELSE 0 END,
        attack_type_breakdown = attack_statistics.attack_type_breakdown || 
                               jsonb_build_object(
                                   NEW.attack_type,
                                   COALESCE((attack_statistics.attack_type_breakdown->>NEW.attack_type)::integer, 0) + 1
                               ),
        severity_breakdown = attack_statistics.severity_breakdown || 
                            jsonb_build_object(
                                NEW.severity,
                                COALESCE((attack_statistics.severity_breakdown->>NEW.severity)::integer, 0) + 1
                            ),
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_attack_statistics
    AFTER INSERT ON attacks
    FOR EACH ROW
    EXECUTE FUNCTION update_attack_statistics();

-- Sample attack patterns data
INSERT INTO attack_patterns (attack_type, pattern, description, base_confidence) VALUES
-- SQL Injection
('sql_injection', '(\bOR\b|\bAND\b).*[=><].*[''"]', 'Boolean-based SQL injection', 85),
('sql_injection', '[''"];.*DROP.*TABLE', 'SQL DROP statement injection', 95),
('sql_injection', '\bUNION\b.*\bSELECT\b', 'UNION-based SQL injection', 90),
('sql_injection', '\b(SELECT|INSERT|UPDATE|DELETE)\b.*\b(FROM|INTO|SET|WHERE)\b', 'SQL statement injection', 80),

-- Cross-Site Scripting (XSS)
('xss', '<script[^>]*>.*?</script>', 'Script tag injection', 95),
('xss', 'javascript:', 'JavaScript protocol injection', 85),
('xss', 'on\w+\s*=', 'HTML event handler injection', 80),
('xss', '<.*?(\bon\w+|javascript:)', 'HTML with JavaScript events', 85),

-- Directory Traversal
('directory_traversal', '\.\.\/', 'Directory traversal (Unix)', 90),
('directory_traversal', '\.\.\\', 'Directory traversal (Windows)', 90),
('directory_traversal', '(%2e%2e%2f|%2e%2e%5c)', 'URL encoded directory traversal', 95),

-- Command Injection
('command_injection', '[;&|`]', 'Command separator injection', 85),
('command_injection', '\$\(.*\)', 'Command substitution injection', 90),

-- Server-Side Request Forgery (SSRF)
('ssrf', 'https?://(localhost|127\.0\.0\.1|0\.0\.0\.0)', 'Internal network SSRF', 90),
('ssrf', 'file://', 'Local file protocol SSRF', 95),

-- Local/Remote File Inclusion
('lfi', '\.\./.*\.\./.*\.\.\/', 'Multiple directory traversal', 90),
('lfi', '/etc/passwd', 'Unix passwd file inclusion', 95),
('rfi', 'https?://.*\.(txt|php|asp)', 'Remote file inclusion', 85);
```

### **2. Database Service (Supabase Integration)**

```typescript
// backend/src/services/DatabaseService.ts
import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { AttackRecord, AttackStats, PaginatedResponse } from '../types';
import { logger } from '../utils/logger';

export class DatabaseService {
  private supabase: SupabaseClient;

  constructor() {
    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_ANON_KEY;

    if (!supabaseUrl || !supabaseKey) {
      throw new Error('Supabase credentials are required');
    }

    this.supabase = createClient(supabaseUrl, supabaseKey);
    logger.info('🗄️  Database service initialized');
  }

  async insertAttack(attackData: Omit<AttackRecord, 'id' | 'created_at' | 'updated_at'>): Promise<AttackRecord> {
    try {
      const { data, error } = await this.supabase
        .from('attacks')
        .insert(attackData)
        .select()
        .single();

      if (error) throw error;

      logger.info(`📊 Attack recorded: ${attackData.attack_type} - ${attackData.url.substring(0, 50)}...`);
      return data;
    } catch (error) {
      logger.error('Failed to insert attack:', error);
      throw new Error('Database insertion failed');
    }
  }

  async getAttacks(options: {
    page: number;
    limit: number;
    filters?: { attack_type?: string; severity?: string; is_malicious?: boolean };
  }): Promise<PaginatedResponse<AttackRecord>> {
    try {
      let query = this.supabase
        .from('attacks')
        .select('*', { count: 'exact' })
        .order('created_at', { ascending: false });

      // Apply filters
      if (options.filters?.attack_type) {
        query = query.eq('attack_type', options.filters.attack_type);
      }
      if (options.filters?.severity) {
        query = query.eq('severity', options.filters.severity);
      }
      if (options.filters?.is_malicious !== undefined) {
        query = query.eq('is_malicious', options.filters.is_malicious);
      }

      // Pagination
      const offset = (options.page - 1) * options.limit;
      query = query.range(offset, offset + options.limit - 1);

      const { data, error, count } = await query;

      if (error) throw error;

      return {
        data: data || [],
        total: count || 0,
        page: options.page,
        limit: options.limit,
        totalPages: Math.ceil((count || 0) / options.limit)
      };
    } catch (error) {
      logger.error('Failed to fetch attacks:', error);
      throw new Error('Database query failed');
    }
  }

  async getAttackStats(): Promise<AttackStats> {
    try {
      // Get current day statistics
      const { data: todayStats } = await this.supabase
        .from('attack_statistics')
        .select('*')
        .eq('date', new Date().toISOString().split('T')[0])
        .single();

      // Get overall statistics
      const { data: overallStats } = await this.supabase
        .from('attacks')
        .select('attack_type, severity, is_malicious, created_at')
        .gte('created_at', new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString()); // Last 30 days

      // Get recent attacks
      const { data: recentAttacks } = await this.supabase
        .from('attacks')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(10);

      return {
        total_attacks: todayStats?.total_attacks || 0,
        total_malicious: todayStats?.total_malicious || 0,
        attack_by_type: todayStats?.attack_type_breakdown || {},
        severity_distribution: todayStats?.severity_breakdown || {},
        recent_attacks: recentAttacks || [],
        trends: this.calculateTrends(overallStats || [])
      };
    } catch (error) {
      logger.error('Failed to fetch attack statistics:', error);
      throw new Error('Statistics query failed');
    }
  }

  private calculateTrends(attacks: any[]): any[] {
    // Group attacks by day and calculate trends
    const grouped = attacks.reduce((acc, attack) => {
      const date = attack.created_at.split('T')[0];
      if (!acc[date]) acc[date] = 0;
      acc[date]++;
      return acc;
    }, {});

    return Object.entries(grouped).map(([date, count]) => ({
      date,
      count
    }));
  }

  async exportAttacks(format: 'csv' | 'json', filters?: any): Promise<any[]> {
    try {
      let query = this.supabase.from('attacks').select('*');

      if (filters) {
        // Apply filters similar to getAttacks
        if (filters.attack_type) query = query.eq('attack_type', filters.attack_type);
        if (filters.severity) query = query.eq('severity', filters.severity);
      }

      const { data, error } = await query.order('created_at', { ascending: false });

      if (error) throw error;

      return data || [];
    } catch (error) {
      logger.error('Failed to export attacks:', error);
      throw new Error('Export failed');
    }
  }
}
```

---

## 🎨 Tailwind CSS Configuration

### **tailwind.config.js**

```javascript
// frontend/tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          900: '#1e3a8a'
        },
        danger: {
          50: '#fef2f2',
          100: '#fee2e2',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
          900: '#7f1d1d'
        },
        warning: {
          50: '#fffbeb',
          100: '#fef3c7',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309'
        },
        success: {
          50: '#ecfdf5',
          100: '#d1fae5',
          500: '#10b981',
          600: '#059669',
          700: '#047857'
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-gentle': 'bounce 2s infinite',
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        }
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'Monaco', 'Consolas', 'monospace']
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio')
  ]
}
```

---

## 🚀 Deployment Strategy

### **1. Frontend Deployment (Vercel)**

```json
// frontend/vercel.json
{
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "headers": {
        "cache-control": "s-maxage=31536000,immutable"
      }
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "REACT_APP_API_URL": "https://your-backend-url.railway.app",
    "REACT_APP_SUPABASE_URL": "@supabase-url",
    "REACT_APP_SUPABASE_ANON_KEY": "@supabase-anon-key"
  }
}
```

### **2. Backend Deployment (Railway)**

```yaml
# backend/railway.yml
version: 2
build:
  commands:
    - npm install
    - npm run build
start:
  command: npm start
env:
  NODE_ENV: production
  PORT: $PORT
  SUPABASE_URL: $SUPABASE_URL
  SUPABASE_ANON_KEY: $SUPABASE_ANON_KEY
  FRONTEND_URL: $FRONTEND_URL
```

---

## 🎯 Key Features Comparison

### **Python Version vs Modern Stack**

| Feature | Python Stack | Modern Stack |
|---------|--------------|--------------|
| **Frontend** | Flask Templates + HTML/CSS | React + TypeScript + Tailwind |
| **Backend** | Python + Flask | Node.js + Express + TypeScript |
| **Database** | SQLite | Supabase (PostgreSQL) |
| **Real-time** | None | WebSocket + Supabase Realtime |
| **Type Safety** | None | Full TypeScript coverage |
| **UI/UX** | Basic HTML forms | Modern React components |
| **Deployment** | Manual setup | Automated CI/CD |
| **Scaling** | Limited | Horizontal scaling |
| **Performance** | Good | Excellent |

### **Enhanced Capabilities**

1. **Real-time Updates**: Live dashboard updates using Supabase realtime
2. **Type Safety**: Full TypeScript implementation
3. **Modern UI**: Responsive design with Tailwind CSS
4. **Cloud Database**: Scalable PostgreSQL with Supabase
5. **API First**: RESTful API with comprehensive documentation
6. **Authentication Ready**: Supabase Auth integration
7. **Deployment Ready**: Production deployment configurations

---

## 🛠️ Quick Start Guide

### **1. Clone and Setup**

```bash
# Clone the project
git clone https://github.com/yourusername/url-attack-detector-modern
cd url-attack-detector-modern

# Backend setup
cd backend
npm install
cp .env.example .env
# Configure Supabase credentials in .env
npm run dev

# Frontend setup (in new terminal)
cd ../frontend
npm install
cp .env.example .env.local
# Configure API and Supabase URLs
npm start
```

### **2. Supabase Setup**

```bash
# Install Supabase CLI
npm install -g supabase

# Login and create project
supabase login
supabase init
supabase start

# Run database migrations
supabase db push
```

### **3. Environment Variables**

```bash
# Backend (.env)
NODE_ENV=development
PORT=5000
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
FRONTEND_URL=http://localhost:3000

# Frontend (.env.local)
REACT_APP_API_URL=http://localhost:5000
REACT_APP_SUPABASE_URL=your-supabase-url
REACT_APP_SUPABASE_ANON_KEY=your-anon-key
```

---

This modern implementation provides a **production-ready, scalable, and maintainable** URL Attack Detection System using cutting-edge web technologies. The system maintains all the core functionality while adding real-time capabilities, type safety, modern UI/UX, and cloud-native architecture! 🚀

**Live Demo**: Deploy to see the system in action with real-time updates and modern interface!