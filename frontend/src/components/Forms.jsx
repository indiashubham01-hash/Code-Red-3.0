import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, Thermometer, User, Cigarette, Scale, Heart } from 'lucide-react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8004';

// --- Reusable UI Elements ---
// --- Reusable UI Elements ---
export const InputGroup = ({ label, icon: Icon, ...props }) => (
    <div className="space-y-2">
        <label className="text-sm font-medium text-slate-700 flex items-center gap-2">
            {Icon && <Icon size={16} className="text-brand-500" />}
            {label}
        </label>
        <input {...props} className="input-field" />
    </div>
);

export const SelectGroup = ({ label, icon: Icon, options, ...props }) => (
    <div className="space-y-2">
        <label className="text-sm font-medium text-slate-700 flex items-center gap-2">
            {Icon && <Icon size={16} className="text-brand-500" />}
            {label}
        </label>
        <select {...props} className="input-field cursor-pointer">
            {options.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
        </select>
    </div>
);

// --- Cardio Form ---
export const CardioForm = ({ setResult }) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        age: 50, gender: 1, height: 170, weight: 70, ap_hi: 120, ap_lo: 80,
        cholesterol: 1, gluc: 1, smoke: 0, alco: 0, active: 1
    });

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: Number(e.target.value) });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const payload = { ...formData, age: formData.age * 365 }; // Convert years to days

            // 1. Get Prediction Result
            const res1 = await axios.post(`${API_URL}/predict/cardiovascular/result`, payload);
            let resultData = res1.data;

            // 2. Get Explanation (Optional)
            try {
                const res2 = await axios.post(`${API_URL}/predict/cardiovascular/explanation`, payload);
                if (res2.data.explanations) {
                    resultData = { ...resultData, explanations: res2.data.explanations };
                }
            } catch (ignore) { console.warn("Explanations skipped"); }

            setResult({ type: 'cardio', data: resultData });
        } catch (err) {
            alert("Error: " + err.message);
        }
        setLoading(false);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6 animate-fade-in">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <InputGroup label="Age (Years)" name="age" type="number" value={formData.age} onChange={handleChange} icon={User} />
                <SelectGroup label="Gender" name="gender" value={formData.gender} onChange={handleChange} icon={User}
                    options={[{ value: 1, label: 'Female' }, { value: 2, label: 'Male' }]} />

                <InputGroup label="Height (cm)" name="height" type="number" value={formData.height} onChange={handleChange} icon={Scale} />
                <InputGroup label="Weight (kg)" name="weight" type="number" value={formData.weight} onChange={handleChange} icon={Scale} />

                <InputGroup label="Systolic BP" name="ap_hi" type="number" value={formData.ap_hi} onChange={handleChange} icon={Activity} />
                <InputGroup label="Diastolic BP" name="ap_lo" type="number" value={formData.ap_lo} onChange={handleChange} icon={Activity} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <SelectGroup label="Cholesterol" name="cholesterol" value={formData.cholesterol} onChange={handleChange} icon={Thermometer}
                    options={[{ value: 1, label: 'Normal' }, { value: 2, label: 'Above Normal' }, { value: 3, label: 'High' }]} />
                <SelectGroup label="Glucose" name="gluc" value={formData.gluc} onChange={handleChange} icon={Thermometer}
                    options={[{ value: 1, label: 'Normal' }, { value: 2, label: 'Above Normal' }, { value: 3, label: 'High' }]} />
                <SelectGroup label="Smoking" name="smoke" value={formData.smoke} onChange={handleChange} icon={Cigarette}
                    options={[{ value: 0, label: 'No' }, { value: 1, label: 'Yes' }]} />
            </div>

            <button type="submit" disabled={loading} className="btn-primary">
                {loading ? "Analyzing Heart Health..." : "Predict Cardiovascular Risk"}
            </button>
        </form>
    );
};

// --- IPF Form ---
export const IPFForm = ({ setResult }) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({ age: 65, gender: 'Male', smoking_history: 'Ever' });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await axios.post(`${API_URL}/predict/idiopathic`, formData);
            setResult({ type: 'ipf', data: res.data });
        } catch (err) { alert(err.message); }
        setLoading(false);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6 animate-fade-in">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <InputGroup label="Age" name="age" type="number" value={formData.age} onChange={e => setFormData({ ...formData, age: e.target.value })} icon={User} />
                <SelectGroup label="Gender" name="gender" value={formData.gender} onChange={e => setFormData({ ...formData, gender: e.target.value })} icon={User}
                    options={[{ value: 'Male', label: 'Male' }, { value: 'Female', label: 'Female' }]} />
                <SelectGroup label="Smoking History" name="smoking_history" value={formData.smoking_history} onChange={e => setFormData({ ...formData, smoking_history: e.target.value })} icon={Cigarette}
                    options={[{ value: 'Ever', label: 'Ever' }, { value: 'Never', label: 'Never' }]} />
            </div>
            <button type="submit" disabled={loading} className="btn-primary bg-indigo-600 hover:bg-indigo-500">
                {loading ? "Analyzing Lungs..." : "Assess Pulmonary Fibrosis Risk"}
            </button>
        </form>
    );
};
