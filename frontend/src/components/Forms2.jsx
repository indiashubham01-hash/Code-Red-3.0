import React, { useState } from 'react';
import { Activity, MessageSquare, FileText, Send } from 'lucide-react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:6969';

import { InputGroup, SelectGroup } from './Forms';
import { User, Cigarette, Heart, Scale, Thermometer, Microscope } from 'lucide-react';

// --- Diabetes Form ---
export const DiabetesForm = ({ setResult }) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        age: 45, gender: 'Male', hypertension: 0, heart_disease: 0, smoking_history: 'never',
        bmi: 25.0, HbA1c_level: 5.5, blood_glucose_level: 100
    });

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.type === 'number' ? Number(e.target.value) : e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await axios.post(`${API_URL}/predict/diabetes`, formData);
            setResult({ type: 'diabetes', data: res.data });
        } catch (err) {
            console.error("Diabetes Error:", err);
            const msg = err.response?.data?.detail || err.response?.data?.message || err.message;
            alert("Error: " + (typeof msg === 'object' ? JSON.stringify(msg) : msg));
        }
        setLoading(false);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6 animate-fade-in">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <InputGroup label="Age" name="age" type="number" value={formData.age} onChange={handleChange} icon={User} />
                <SelectGroup label="Gender" name="gender" value={formData.gender} onChange={handleChange} icon={User}
                    options={[{ value: 'Male', label: 'Male' }, { value: 'Female', label: 'Female' }]} />

                <SelectGroup label="Hypertension" name="hypertension" value={formData.hypertension} onChange={handleChange} icon={Activity}
                    options={[{ value: 0, label: 'No' }, { value: 1, label: 'Yes' }]} />
                <SelectGroup label="Heart Disease" name="heart_disease" value={formData.heart_disease} onChange={handleChange} icon={Heart}
                    options={[{ value: 0, label: 'No' }, { value: 1, label: 'Yes' }]} />

                <SelectGroup label="Smoking History" name="smoking_history" value={formData.smoking_history} onChange={handleChange} icon={Cigarette}
                    options={[
                        { value: 'never', label: 'Never' }, { value: 'current', label: 'Current' },
                        { value: 'former', label: 'Former' }, { value: 'No Info', label: 'No Info' }
                    ]} />
                <InputGroup label="BMI" name="bmi" type="number" step="0.1" value={formData.bmi} onChange={handleChange} icon={Scale} />

                <InputGroup label="HbA1c Level" name="HbA1c_level" type="number" step="0.1" value={formData.HbA1c_level} onChange={handleChange} icon={Thermometer} />
                <InputGroup label="Blood Glucose" name="blood_glucose_level" type="number" value={formData.blood_glucose_level} onChange={handleChange} icon={Thermometer} />
            </div>
            <button type="submit" disabled={loading} className="btn-primary bg-emerald-600 hover:bg-emerald-500">
                {loading ? "Analyzing..." : "Check Diabetes Risk"}
            </button>
        </form>
    );
};

// --- CBC Form ---
export const CBCForm = ({ setResult }) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        sex: 'male', wbc: 8.5, rbc: 4.8, hemoglobin: 14.2, hematocrit: 42, platelets: 280,
        mcv: 88, mch: 30, mchc: 34, rdw: 12.5
    });

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.type === 'number' ? Number(e.target.value) : e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await axios.post(`${API_URL}/analyze_cbc`, formData);
            setResult({ type: 'cbc', data: res.data });
        } catch (err) {
            console.error("CBC Error:", err);
            const msg = err.response?.data?.detail || err.response?.data?.message || err.message;
            alert("Error: " + (typeof msg === 'object' ? JSON.stringify(msg) : msg));
        }
        setLoading(false);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6 animate-fade-in">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <SelectGroup label="Sex" name="sex" value={formData.sex} onChange={handleChange} icon={User}
                    options={[{ value: 'male', label: 'Male' }, { value: 'female', label: 'Female' }]} />
                <InputGroup label="WBC (x10^9/L)" name="wbc" type="number" step="0.1" value={formData.wbc} onChange={handleChange} icon={Microscope} />
                <InputGroup label="RBC (x10^12/L)" name="rbc" type="number" step="0.1" value={formData.rbc} onChange={handleChange} icon={Microscope} />

                <InputGroup label="Hemoglobin (g/dL)" name="hemoglobin" type="number" step="0.1" value={formData.hemoglobin} onChange={handleChange} icon={Activity} />
                <InputGroup label="Hematocrit (%)" name="hematocrit" type="number" step="0.1" value={formData.hematocrit} onChange={handleChange} icon={Activity} />
                <InputGroup label="Platelets (x10^9/L)" name="platelets" type="number" value={formData.platelets} onChange={handleChange} icon={Activity} />

                <InputGroup label="MCV (fL)" name="mcv" type="number" step="0.1" value={formData.mcv} onChange={handleChange} />
                <InputGroup label="MCH (pg)" name="mch" type="number" step="0.1" value={formData.mch} onChange={handleChange} />
                <InputGroup label="MCHC (g/dL)" name="mchc" type="number" step="0.1" value={formData.mchc} onChange={handleChange} />
                <InputGroup label="RDW (%)" name="rdw" type="number" step="0.1" value={formData.rdw} onChange={handleChange} />
            </div>
            <button type="submit" disabled={loading} className="btn-primary bg-blue-600 hover:bg-blue-500">
                {loading ? "Analyzing Blood..." : "Analyze CBC Report"}
            </button>
        </form>
    );
};

// --- Chat Interface ---
export const ChatInterface = () => {
    const [msgs, setMsgs] = useState([{ role: 'ai', content: 'Hello! I am FedHealth AI. Ask me any medical question.' }]);
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
        <div className="flex flex-col h-[500px] border border-slate-700/50 rounded-2xl bg-slate-900/50 overflow-hidden shadow-inner">
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-transparent scrollbar-thin">
                {msgs.map((m, i) => (
                    <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] p-3 rounded-2xl ${m.role === 'user' ? 'bg-brand-600 text-white rounded-tr-none' : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-tl-none shadow-sm'}`}>
                            {m.content}
                        </div>
                    </div>
                ))}
                {loading && <div className="text-slate-400 text-sm ml-4 flex items-center gap-2"><div className="w-2 h-2 bg-brand-500 rounded-full animate-bounce" /> Thinking...</div>}
            </div>
            <div className="p-4 bg-slate-800/50 border-t border-slate-700 flex gap-2">
                <input className="flex-1 bg-slate-900 border border-slate-700 text-white rounded-xl px-4 focus:ring-1 focus:ring-brand-500 outline-none" value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} placeholder="Type a message..." />
                <button onClick={send} className="p-3 bg-brand-600 text-white rounded-xl hover:bg-brand-500 shadow-lg shadow-brand-500/20"><Send size={20} /></button>
            </div>
        </div>
    );
};
