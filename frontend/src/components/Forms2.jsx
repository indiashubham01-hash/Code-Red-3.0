import React, { useState } from 'react';
import { Activity, MessageSquare, FileText, Send } from 'lucide-react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8004';

// --- Diabetes Form ---
export const DiabetesForm = ({ setResult }) => {
    // Simplified for brevity, usually has more fields
    const [data, setData] = useState({ age: 45, gender: 'Male', bmi: 25.0, HbA1c_level: 5.5, blood_glucose_level: 100, smoking_history: 'never', hypertension: 0, heart_disease: 0 });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post(`${API_URL}/predict/diabetes`, data);
            setResult({ type: 'diabetes', data: res.data });
        } catch (err) { alert(err.message); }
    };
    return (
        <form onSubmit={handleSubmit} className="space-y-4 animate-fade-in">
            <div className="grid grid-cols-2 gap-4">
                <input type="number" placeholder="Glucose" className="input-field" value={data.blood_glucose_level} onChange={e => setData({ ...data, blood_glucose_level: Number(e.target.value) })} />
                <input type="number" placeholder="HbA1c" className="input-field" value={data.HbA1c_level} onChange={e => setData({ ...data, HbA1c_level: Number(e.target.value) })} />
                <input type="number" placeholder="BMI" className="input-field" value={data.bmi} onChange={e => setData({ ...data, bmi: Number(e.target.value) })} />
            </div>
            <button className="btn-primary bg-emerald-600 hover:bg-emerald-500">Check Diabetes Risk</button>
        </form>
    );
};

// --- Chat Interface ---
export const ChatInterface = () => {
    const [msgs, setMsgs] = useState([{ role: 'ai', content: 'Hello! I am Meditron. Ask me any medical question.' }]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const send = async () => {
        if (!input) return;
        const newMsgs = [...msgs, { role: 'user', content: input }];
        setMsgs(newMsgs);
        setInput('');
        setLoading(true);
        try {
            const res = await axios.post(`${API_URL}/chat/meditron`, { message: input, history: [] });
            setMsgs([...newMsgs, { role: 'ai', content: res.data.response }]);
        } catch (err) {
            setMsgs([...newMsgs, { role: 'error', content: "Chat service unavailable." }]);
        }
        setLoading(false);
    };

    return (
        <div className="flex flex-col h-[500px] border rounded-2xl bg-white overflow-hidden shadow-sm">
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
                {msgs.map((m, i) => (
                    <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] p-3 rounded-2xl ${m.role === 'user' ? 'bg-brand-600 text-white rounded-tr-none' : 'bg-white border rounded-tl-none shadow-sm'}`}>
                            {m.content}
                        </div>
                    </div>
                ))}
                {loading && <div className="text-slate-400 text-sm ml-4">Thinking...</div>}
            </div>
            <div className="p-4 bg-white border-t flex gap-2">
                <input className="input-field" value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} placeholder="Type a message..." />
                <button onClick={send} className="p-3 bg-brand-600 text-white rounded-lg hover:bg-brand-500"><Send size={20} /></button>
            </div>
        </div>
    );
};
