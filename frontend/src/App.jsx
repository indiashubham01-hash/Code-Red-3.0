import React, { useState } from 'react';
import { Heart, Activity, Wind, Microscope, MessageCircle, Github, FileText } from 'lucide-react';
import axios from 'axios';
import { CardioForm, IPFForm } from './components/Forms';
import { DiabetesForm, ChatInterface } from './components/Forms2';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8004';

// Result Display Component
const ResultCard = ({ result }) => {
  if (!result) return null;
  const { type, data } = result;
  const [report, setReport] = useState(null);
  const [loadingReport, setLoadingReport] = useState(false);

  // Reset report when result changes
  React.useEffect(() => { setReport(null); }, [result]);

  const getRiskColor = (prob) => {
    if (prob < 0.3) return 'bg-emerald-100 text-emerald-800 border-emerald-200';
    if (prob < 0.7) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-rose-100 text-rose-800 border-rose-200';
  };

  const generateReport = async () => {
    setLoadingReport(true);
    try {
      const payload = {
        prediction: data,
        symptoms: ["No specific symptoms provided by user input form."]
      };
      const res = await axios.post(`${API_URL}/generate_report`, payload);
      setReport(res.data.report);
    } catch (err) {
      alert("Failed to generate report: " + err.message);
    }
    setLoadingReport(false);
  };

  return (
    <div className="glass-card p-6 animate-slide-up mt-6 border-l-4 border-l-brand-500">
      <h3 className="text-xl font-bold text-slate-800 mb-2">Analysis Result</h3>

      {data.risk_probability !== undefined && (
        <div className={`p-4 rounded-lg border mb-4 flex justify-between items-center ${getRiskColor(data.risk_probability)}`}>
          <span className="font-medium text-lg">{data.risk_category || "Risk Assessment"}</span>
          <span className="text-2xl font-bold">{(data.risk_probability * 100).toFixed(1)}%</span>
        </div>
      )}

      {data.prediction && (
        <div className="text-lg font-medium text-slate-700 mb-2">
          Prediction: <span className="text-brand-600">{data.prediction}</span>
        </div>
      )}

      {data.explanations && (
        <div className="mt-4">
          <h4 className="font-semibold text-slate-700 mb-2">Key Factors:</h4>
          <ul className="space-y-1">
            {data.explanations.top_factors.map((f, i) => (
              <li key={i} className="text-sm text-slate-600 flex justify-between">
                <span className="capitalize">{f.feature}</span>
                <span className={`${f.impact === 'increases' ? 'text-rose-500' : 'text-emerald-500'}`}>{f.impact} risk</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Report Generation Section */}
      <div className="mt-6 pt-6 border-t border-slate-200">
        {!report ? (
          <button
            onClick={generateReport}
            disabled={loadingReport}
            className="w-full flex items-center justify-center gap-2 py-2 px-4 bg-slate-800 text-white rounded-lg hover:bg-slate-700 transition-all disabled:opacity-50"
          >
            <FileText size={18} />
            {loadingReport ? "Generating AI Report..." : "Generate Detailed AI Report"}
          </button>
        ) : (
          <div className="animate-fade-in bg-slate-50 p-4 rounded-lg border border-slate-200 text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
            <h4 className="font-bold text-slate-900 mb-2 flex items-center gap-2">
              <FileText size={16} className="text-brand-500" /> AI Medical Report
            </h4>
            {report}
          </div>
        )}
      </div>
    </div>
  );
};

function App() {
  const [activeTab, setActiveTab] = useState('cardio');
  const [result, setResult] = useState(null);

  const tabs = [
    { id: 'cardio', label: 'Cardiovascular', icon: Heart },
    { id: 'diabetes', label: 'Diabetes', icon: Activity },
    { id: 'ipf', label: 'Pulmonary (IPF)', icon: Wind },
    { id: 'cbc', label: 'CBC Analysis', icon: Microscope },
    { id: 'chat', label: 'AI Assistant', icon: MessageCircle },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 fixed h-full hidden md:flex flex-col z-10">
        <div className="p-6 border-b border-slate-100">
          <h1 className="text-2xl font-bold text-brand-600 flex items-center gap-2">
            <Activity className="text-brand-500" />
            MedAssist
          </h1>
          <p className="text-xs text-slate-400 mt-1">AI-Powered Diagnostics</p>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => { setActiveTab(tab.id); setResult(null); }}
              className={`nav-item w-full ${activeTab === tab.id ? 'active bg-brand-50 text-brand-600' : ''}`}
            >
              <tab.icon size={20} />
              {tab.label}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-100">
          <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-50 text-slate-600 text-sm">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
            Backend Online (8004)
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 md:ml-64 p-4 md:p-8 overflow-y-auto">
        <div className="max-w-3xl mx-auto space-y-8">
          <div className="flex justify-between items-center md:hidden mb-6">
            <h1 className="text-xl font-bold text-brand-600">MedAssist</h1>
            {/* Mobile menu toggle would go here */}
          </div>

          <div className="mb-8">
            <h2 className="text-3xl font-bold text-slate-900 mb-2">
              {tabs.find(t => t.id === activeTab)?.label} Analysis
            </h2>
            <p className="text-slate-500">
              Enter patient vitals below for real-time AI inference.
            </p>
          </div>

          {/* Content Area */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-6">
              <div className="glass-card p-6">
                {activeTab === 'cardio' && <CardioForm setResult={setResult} />}
                {activeTab === 'diabetes' && <DiabetesForm setResult={setResult} />}
                {activeTab === 'ipf' && <IPFForm setResult={setResult} />}
                {activeTab === 'chat' && <ChatInterface />}
                {activeTab === 'cbc' && <div className="text-center py-10 text-slate-500">CBC Form Placeholder</div>}
              </div>
            </div>

            {/* Sidebar Result / Info */}
            <div className="lg:col-span-1">
              {result ? (
                <ResultCard result={result} />
              ) : (
                activeTab !== 'chat' && (
                  <div className="glass-card p-6 text-center text-slate-400">
                    <Activity className="w-12 h-12 mx-auto mb-3 opacity-20" />
                    <p className="text-sm">Analysis results will appear here after submission.</p>
                  </div>
                )
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
