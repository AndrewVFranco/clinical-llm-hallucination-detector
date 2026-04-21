import React, { useLayoutEffect, useState } from 'react';
import { Sun, Moon, Menu, X } from 'lucide-react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [query, setQuery] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingPhase, setLoadingPhase] = useState(null);
  const [result, setResult] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('theme');
    return saved ? saved === 'dark' : true;
  });

  useLayoutEffect(() => {
    document.body.classList.toggle('dark-mode', darkMode);
  }, [darkMode]);

  const toggleTheme = () => {
    setDarkMode(prevMode => {
      const newMode = !prevMode;
      localStorage.setItem('theme', newMode ? 'dark' : 'light');
      return newMode;
    });
  };

  const closeSidebar = () => setIsSidebarOpen(false);

  const handleSubmit = async (fhirData = {}) => {
    if ((!query.trim() && !fhirData.has_fhir) || loading) return;

    closeSidebar();

    const userMessage = {
        role: 'user',
        text: query || `FHIR ${fhirData.fhir_resource_type}/${fhirData.fhir_resource_id}`
      };

    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setLoading(true);
    setLoadingPhase(null);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage.text, api_key: apiKey, ...fhirData }),
      });

      if (!response.ok) throw new Error('Query failed');

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        const parts = buffer.split('\n\n');

        buffer = parts.pop();

        for (const part of parts) {
          const line = part.trim();
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.substring(6));

              if (data.status) {
                setLoadingPhase(data.status);
              }

              if (data.final_response) {
                setResult(data.final_response);
                setMessages(prev => [...prev, { role: 'assistant', data: data.final_response }]);
              }
            } catch (parseError) {
               console.error("JSON Parse Error on complete chunk:", line, parseError);
            }
          }
        }
      }
    } catch (err) {
        let errorText = 'Failed to connect to the analysis server. Ensure the backend is running.';

        if (err.message === 'Query failed') {
          errorText = 'The server returned an error. Check your API key or try a different query.';
        } else if (err.message.includes('fetch')) {
          errorText = 'Cannot reach the backend server. Ensure it is running on port 8000.';
        } else if (err.message.includes('quota') || err.message.includes('429')) {
          errorText = 'API quota exhausted. Please provide your own Gemini API key.';
        }

        setMessages(prev => [...prev, {
          role: 'error',
          text: errorText
        }]);
    } finally {
      setLoading(false);
      setLoadingPhase(null);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button
            className="mobile-menu-toggle"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            style={{ background: 'none', border: 'none', color: 'inherit', cursor: 'pointer' }}
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>

          <div className="logo">
            Sentinel<span>MD</span>
          </div>
        </div>

        <div>
          <button onClick={toggleTheme} style={{ background: 'none', border: 'none', outline: 'none', color: 'inherit' }}>
            {darkMode ? <Sun /> : <Moon />}
          </button>
        </div>
      </header>

      <div className="layout">
        <div className={`sidebar-container ${isSidebarOpen ? 'open' : ''}`}>
          <Sidebar apiKey={apiKey} onApiKeyChange={setApiKey} result={result}/>
        </div>

        {isSidebarOpen && (
           <div className="mobile-overlay" onClick={closeSidebar}></div>
        )}

        <ChatWindow
          messages={messages}
          query={query}
          onQueryChange={setQuery}
          onSubmit={handleSubmit}
          loading={loading}
          loadingPhase={loadingPhase}
        />
      </div>
    </div>
  );
}

export default App;