import React, { useEffect, useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, useLocation } from 'react-router-dom';
import { ArrowLeft, User, Activity, Calendar } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area, CartesianGrid } from 'recharts';

const Profile = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const member = location.state?.member || { id: 0, name: 'Guest User' }; // Fallback

    // Generate deterministic random data based on member ID
    const data = useMemo(() => {
        const seed = member.id * 100;
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'];
        return months.map((month, index) => {
            // Simple pseudo-random generator
            const r1 = Math.sin(seed + index) * 10000;
            const r2 = Math.cos(seed + index) * 10000;
            const random1 = r1 - Math.floor(r1);
            const random2 = r2 - Math.floor(r2);

            return {
                name: month,
                risk: Math.floor(20 + random1 * 60), // Risk between 20-80
                glucose: Math.floor(80 + random2 * 80) // Glucose between 80-160
            };
        });
    }, [member.id]);

    const avgGlucose = Math.round(data.reduce((acc, curr) => acc + curr.glucose, 0) / data.length);

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100 p-8">
            <div className="max-w-6xl mx-auto">
                <button onClick={() => navigate('/dashboard')} className="flex items-center text-slate-400 hover:text-white mb-8 transition-colors">
                    <ArrowLeft className="mr-2" /> Back to Dashboard
                </button>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
                    {/* Profile Card */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}
                        className="glass-card p-8 flex flex-col items-center text-center"
                    >
                        <div className="w-32 h-32 rounded-full bg-gradient-to-br from-brand-400 to-accent-purple p-1 mb-4 shadow-lg shadow-brand-500/20">
                            <div className="w-full h-full rounded-full bg-slate-900 flex items-center justify-center">
                                <User size={48} className="text-slate-400" />
                            </div>
                        </div>
                        <h2 className="text-2xl font-bold">{member.name}</h2>
                        <p className="text-slate-400 mb-6">Patient ID: #{8492 + member.id}-A</p>

                        <div className="w-full grid grid-cols-2 gap-4">
                            <div className="p-3 bg-slate-900/50 rounded-xl">
                                <div className="text-xs text-slate-500">Age</div>
                                <div className="text-lg font-mono">{40 + (member.id * 3) % 20}</div>
                            </div>
                            <div className="p-3 bg-slate-900/50 rounded-xl">
                                <div className="text-xs text-slate-500">Blood Type</div>
                                <div className="text-lg font-mono">{['O+', 'A+', 'B-', 'AB+'][member.id % 4]}</div>
                            </div>
                        </div>
                    </motion.div>

                    {/* Stats */}
                    <div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-6">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
                            className="glass-card p-6 flex flex-col justify-between relative overflow-hidden group"
                        >
                            <div className="z-10">
                                <div className="text-slate-400 mb-2">Avg Glucose Level</div>
                                <div className="text-4xl font-bold text-white">{avgGlucose} <span className="text-sm font-normal text-slate-500">mg/dL</span></div>
                            </div>
                            <div className="absolute right-[-20px] bottom-[-20px] text-brand-500/10 group-hover:text-brand-500/20 transition-colors">
                                <Activity size={120} />
                            </div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
                            className="glass-card p-6 flex flex-col justify-between"
                        >
                            <div>
                                <div className="text-slate-400 mb-2">Last Checkup</div>
                                <div className="text-4xl font-bold text-white">2 <span className="text-sm font-normal text-slate-500">days ago</span></div>
                            </div>
                            <div className="flex items-center gap-2 text-emerald-400 text-sm mt-4">
                                <Calendar size={16} /> Scheduled for next week
                            </div>
                        </motion.div>
                    </div>
                </div>

                {/* Charts */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
                    className="glass-card p-6 md:p-8"
                >
                    <div className="flex items-center justify-between mb-8">
                        <h3 className="text-xl font-bold">Health Trends for {member.name}</h3>
                        <div className="flex gap-2">
                            <span className="flex items-center text-xs text-slate-400"><span className="w-3 h-3 rounded-full bg-brand-500 mr-2"></span>Risk Score</span>
                            <span className="flex items-center text-xs text-slate-400"><span className="w-3 h-3 rounded-full bg-accent-purple mr-2"></span>Glucose</span>
                        </div>
                    </div>

                    <div className="h-[400px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                                    </linearGradient>
                                    <linearGradient id="colorGlu" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <XAxis dataKey="name" stroke="#475569" />
                                <YAxis stroke="#475569" />
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b' }}
                                    itemStyle={{ color: '#e2e8f0' }}
                                />
                                <Area type="monotone" dataKey="risk" stroke="#0ea5e9" fillOpacity={1} fill="url(#colorRisk)" strokeWidth={3} />
                                <Area type="monotone" dataKey="glucose" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorGlu)" strokeWidth={3} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>

            </div>
        </div>
    );
};
export default Profile;
