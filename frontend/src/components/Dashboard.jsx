import React, { useState, useEffect } from 'react';
import { motion, useMotionValue, useTransform, animate, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Activity, Heart, Wind, Microscope, User, LogOut, Menu, FileText, X, Sparkles } from 'lucide-react';
import axios from 'axios';
import { CardioForm, IPFForm } from './Forms'; // Assuming these exist, might need to wrap them
import { DiabetesForm, ChatInterface, CBCForm } from './Forms2';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'; // Simple charts

// --- G-Force Dial Component ---
const GForceDial = ({ value = 0 }) => {
    // Value is 0 to 100 (Risk Probability)
    const displayValue = useMotionValue(0);
    const rotation = useTransform(displayValue, [0, 100], [-120, 120]);
    const textRef = React.useRef(null);

    useEffect(() => {
        const controls = animate(displayValue, value * 100, { duration: 1.5, ease: "backOut" });
        return controls.stop;
    }, [value]);

    useEffect(() => {
        const unsubscribe = displayValue.on("change", (latest) => {
            if (textRef.current) {
                textRef.current.textContent = Math.round(latest);
            }
        });
        return unsubscribe;
    }, [displayValue]);

    return (
        <div className="relative w-64 h-64 flex items-center justify-center">
            {/* Dial Background */}
            <svg className="w-full h-full text-slate-800" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="200" strokeDashoffset="50" transform="rotate(135 50 50)" />
            </svg>

            {/* Active Arc (Gradient) */}
            <svg className="absolute top-0 left-0 w-full h-full text-brand-500 overflow-visible" viewBox="0 0 100 100">
                {/* Simplified representation - normally would use strokeDasharray calcs */}
                <motion.circle
                    cx="50" cy="50" r="45"
                    stroke="url(#gradient)" strokeWidth="4" fill="none"
                    strokeDasharray="200" strokeDashoffset={useTransform(displayValue, [0, 100], [280, 50])}
                    strokeLinecap="round"
                    transform="rotate(135 50 50)"
                    initial={{ strokeDashoffset: 280 }}
                />
                <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#0ea5e9" />
                        <stop offset="100%" stopColor="#f43f5e" />
                    </linearGradient>
                </defs>
            </svg>

            {/* Needle / Indicator */}
            <motion.div
                style={{ rotate: rotation }}
                className="absolute w-full h-full flex justify-center pt-4"
            >
                <div className="w-1 h-4 bg-white rounded-full shadow-[0_0_10px_white]" />
            </motion.div>

            {/* Center Label */}
            <div className="absolute flex flex-col items-center">
                <span ref={textRef} className="text-4xl font-mono font-bold text-white">
                    0
                </span>
                <span className="text-xs text-slate-400 uppercase tracking-widest">Risk IDX</span>
            </div>
        </div>
    );
};

const Dashboard = () => {
    const navigate = useNavigate();
    const [activeModule, setActiveModule] = useState('cardio');
    const [result, setResult] = useState(null);

    // Report State
    const [showReport, setShowReport] = useState(false);
    const [reportContent, setReportContent] = useState('');
    const [reportLoading, setReportLoading] = useState(false);

    const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:6969';

    const generateReport = async () => {
        if (!result) return;
        setReportLoading(true);
        setShowReport(true);
        try {
            // Prepare payload
            // We use the result data as the prediction context
            const prediction = {
                ...result.data,
                module: activeModule
            };

            // Infer symptoms/context from available data keys if possible, otherwise generic
            const symptoms = ["Analyzed via " + activeModule + " module", "Clinical data provided"];

            const res = await axios.post(`${API_URL}/generate_report`, {
                prediction: prediction,
                symptoms: symptoms
            });

            setReportContent(res.data.report);
        } catch (err) {
            setReportContent("Failed to generate report. Please try again.\nError: " + err.message);
        }
        setReportLoading(false);
    };

    // Member State
    const [members, setMembers] = useState([
        { id: 1, name: 'John Doe' },
        { id: 2, name: 'Jane Smith' }
    ]);
    const [activeMember, setActiveMember] = useState(members[0]);
    const [showAddMember, setShowAddMember] = useState(false);
    const [newMemberName, setNewMemberName] = useState('');

    const addMember = () => {
        if (newMemberName.trim()) {
            const newId = members.length + 1;
            const newMember = { id: newId, name: newMemberName };
            setMembers([...members, newMember]);
            setActiveMember(newMember);
            setNewMemberName('');
            setShowAddMember(false);
        }
    };

    // Navigation Items
    const navItems = [
        { id: 'cardio', label: 'Cardio', icon: Heart },
        { id: 'diabetes', label: 'Diabetes', icon: Activity },
        { id: 'ipf', label: 'Pulmonary', icon: Wind },
        { id: 'cbc', label: 'Blood', icon: Microscope },
    ];

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100 font-sans flex overflow-hidden">
            {/* Sidebar Navigation */}
            <motion.aside
                initial={{ x: -100 }} animate={{ x: 0 }}
                className="w-20 lg:w-64 bg-slate-900 border-r border-slate-800 flex flex-col z-20"
            >
                <div className="h-20 flex items-center justify-center lg:justify-start lg:px-6 border-b border-slate-800">
                    <Activity className="text-brand-500 w-8 h-8" />
                    <span className="hidden lg:block ml-3 font-bold text-xl tracking-tight">FedHealth</span>
                </div>

                <nav className="flex-1 py-8 px-2 space-y-2 overflow-y-auto scrollbar-thin">
                    {/* Module Nav */}
                    {navItems.map(item => (
                        <button
                            key={item.id}
                            onClick={() => { setActiveModule(item.id); setResult(null); }}
                            className={`w-full flex items-center p-3 rounded-xl transition-all group ${activeModule === item.id ? 'bg-brand-600/20 text-brand-400' : 'hover:bg-slate-800 text-slate-400'}`}
                        >
                            <item.icon size={24} className="min-w-[24px]" />
                            <span className="hidden lg:block ml-3 font-medium">{item.label}</span>
                            {activeModule === item.id && (
                                <motion.div layoutId="active-pill" className="absolute left-0 w-1 h-8 bg-brand-500 rounded-r-full" />
                            )}
                        </button>
                    ))}

                    <div className="pt-8 mt-8 border-t border-slate-800 px-2">
                        <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-4 px-2 hidden lg:block">Members</div>
                        <div className="space-y-1">
                            {members.map(member => (
                                <button
                                    key={member.id}
                                    onClick={() => setActiveMember(member)}
                                    className={`w-full flex items-center p-2 rounded-lg text-sm transition-colors ${activeMember.id === member.id ? 'bg-slate-800 text-white' : 'text-slate-400 hover:text-slate-300'}`}
                                >
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 ${activeMember.id === member.id ? 'bg-brand-500 text-white' : 'bg-slate-700'}`}>
                                        <User size={14} />
                                    </div>
                                    <span className="hidden lg:block truncate">{member.name}</span>
                                </button>
                            ))}
                        </div>

                        {/* Add Member UI */}
                        {showAddMember ? (
                            <div className="mt-4 p-2 bg-slate-800 rounded-lg animate-fade-in">
                                <input
                                    className="w-full bg-slate-900 border border-slate-700 rounded p-1 text-xs text-white mb-2"
                                    placeholder="Name..."
                                    value={newMemberName}
                                    onChange={e => setNewMemberName(e.target.value)}
                                    autoFocus
                                />
                                <div className="flex gap-2">
                                    <button onClick={addMember} className="flex-1 bg-brand-600 text-xs py-1 rounded text-white">Add</button>
                                    <button onClick={() => setShowAddMember(false)} className="flex-1 bg-slate-700 text-xs py-1 rounded text-slate-300">Cancel</button>
                                </div>
                            </div>
                        ) : (
                            <button onClick={() => setShowAddMember(true)} className="w-full mt-4 flex items-center justify-center py-2 border border-dashed border-slate-700 rounded-lg text-slate-500 hover:text-brand-400 hover:border-brand-500/50 transition-all text-sm">
                                + Add Member
                            </button>
                        )}
                    </div>

                    <div className="pt-8 mt-8 border-t border-slate-800">
                        <button
                            onClick={() => navigate('/profile', { state: { member: activeMember } })}
                            className="w-full flex items-center p-3 text-slate-400 hover:text-white transition-colors"
                        >
                            <User size={24} />
                            <span className="hidden lg:block ml-3">Profile & Logs</span>
                            <span className="hidden lg:inline-flex ml-auto bg-slate-800 text-xs py-0.5 px-2 rounded-full text-slate-400">{activeMember.name.split(' ')[0]}</span>
                        </button>
                    </div>
                </nav>

                <div className="p-4 border-t border-slate-800">
                    <button className="w-full flex items-center justify-center lg:justify-start text-rose-400 hover:bg-rose-500/10 p-3 rounded-xl transition-all">
                        <LogOut size={20} />
                        <span className="hidden lg:block ml-2 text-sm">Logout</span>
                    </button>
                </div>
            </motion.aside>

            {/* Main Content Area */}
            <main className="flex-1 relative overflow-y-auto">
                {/* Top Header */}
                <header className="h-20 border-b border-slate-800/50 flex items-center justify-between px-8 bg-slate-950/80 backdrop-blur sticky top-0 z-10">
                    <div>
                        <h2 className="text-2xl font-semibold">
                            {navItems.find(i => i.id === activeModule)?.label} Diagnostics
                        </h2>
                        <div className="text-sm text-slate-400 flex items-center gap-2">
                            Assessing: <span className="text-brand-400 font-medium">{activeMember.name}</span>
                        </div>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="flex flex-col items-end mr-4">
                            <span className="text-xs text-slate-400">System Status</span>
                            <div className="flex items-center gap-2">
                                <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                                <span className="text-emerald-500 text-sm font-mono">ONLINE</span>
                            </div>
                        </div>
                    </div>
                </header>

                <div className="p-8 grid grid-cols-1 xl:grid-cols-3 gap-8 max-w-7xl mx-auto">

                    {/* Center Control / Result Display */}
                    <div className="xl:col-span-1 order-1 xl:order-2 flex flex-col gap-6">
                        {/* THE G-FORCE DIAL Container */}
                        <div className="glass-card p-6 flex flex-col items-center justify-center relative min-h-[300px]">
                            <h3 className="absolute top-6 left-6 text-sm text-slate-400 uppercase tracking-wider">Risk Analysis</h3>

                            <GForceDial value={result?.data?.risk_probability || 0} />

                            <div className="mt-8 text-center space-y-2">
                                <div className="text-sm text-slate-500">Classification</div>
                                <div className={`text-2xl font-bold ${result ? 'text-white' : 'text-slate-600'}`}>
                                    {result?.data?.risk_category || "No Data"}
                                </div>
                                {result && (
                                    <motion.button
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        onClick={generateReport}
                                        className="mt-4 flex items-center gap-2 mx-auto px-4 py-2 bg-brand-600/20 hover:bg-brand-600/30 text-brand-400 rounded-full text-sm font-medium transition-all border border-brand-500/20"
                                    >
                                        <Sparkles size={16} />
                                        <span>Generate AI Report</span>
                                    </motion.button>
                                )}
                            </div>

                            {/* Anti-gravity decorative ring */}
                            <motion.div
                                animate={{ rotate: 360 }}
                                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                                className="absolute w-[280px] h-[280px] border border-dashed border-slate-700/50 rounded-full pointer-events-none"
                            />
                        </div>

                        {/* Quick Stats or Chat */}
                        <div className="glass-card p-0 overflow-hidden flex-1 min-h-[300px]">
                            <ChatInterface />
                        </div>
                    </div>

                    {/* Forms Input Area */}
                    <div className="xl:col-span-2 order-2 xl:order-1 space-y-6">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="glass-card p-8"
                        >
                            {activeModule === 'cardio' && <CardioForm setResult={setResult} />}
                            {activeModule === 'diabetes' && <DiabetesForm setResult={setResult} />}
                            {activeModule === 'ipf' && <IPFForm setResult={setResult} />}
                            {activeModule === 'cbc' && <CBCForm setResult={setResult} />}
                        </motion.div>
                    </div>

                </div>
            </main>

            {/* Report Modal */}
            <AnimatePresence>
                {showReport && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[85vh] overflow-hidden flex flex-col shadow-2xl"
                        >
                            <div className="p-6 border-b border-slate-800 flex items-center justify-between bg-slate-800/50">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-brand-500/20 rounded-lg text-brand-400">
                                        <FileText size={24} />
                                    </div>
                                    <div>
                                        <h3 className="text-lg font-semibold text-white">Medical Analysis Report</h3>
                                        <p className="text-xs text-slate-400">Generated by FedHealth AI • Gemini Pro</p>
                                    </div>
                                </div>
                                <button onClick={() => setShowReport(false)} className="p-2 hover:bg-slate-700 rounded-full text-slate-400 hover:text-white transition-colors">
                                    <X size={20} />
                                </button>
                            </div>

                            <div className="p-6 overflow-y-auto custom-scrollbar">
                                {reportLoading ? (
                                    <div className="flex flex-col items-center justify-center py-12 space-y-4">
                                        <div className="w-12 h-12 border-4 border-brand-500/30 border-t-brand-500 rounded-full animate-spin" />
                                        <p className="text-slate-400 animate-pulse">Analyzing clinical markers...</p>
                                    </div>
                                ) : (
                                    <div className="prose prose-invert prose-sm max-w-none">
                                        <div className="whitespace-pre-wrap font-sans text-slate-300 leading-relaxed">
                                            {reportContent}
                                        </div>
                                    </div>
                                )}
                            </div>

                            <div className="p-4 border-t border-slate-800 bg-slate-900/50 flex justify-end">
                                <button
                                    onClick={() => setShowReport(false)}
                                    className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-sm font-medium transition-colors"
                                >
                                    Close Report
                                </button>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default Dashboard;
