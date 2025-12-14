import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Activity, Heart, Shield, ArrowRight } from 'lucide-react';

const Onboarding = () => {
    const navigate = useNavigate();

    // Floating Animation Variant
    const float = (delay) => ({
        y: [0, -15, 0],
        transition: {
            duration: 4,
            ease: "easeInOut",
            repeat: Infinity,
            delay: delay
        }
    });

    return (
        <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center relative overflow-hidden">
            {/* Background Gradients */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-brand-600/20 rounded-full blur-[100px]" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-accent-purple/20 rounded-full blur-[100px]" />
            </div>

            {/* Floating Elements (Anti-Gravity) */}
            <motion.div animate={float(0)} className="absolute top-20 left-20 text-brand-400 opacity-20">
                <Heart size={64} />
            </motion.div>
            <motion.div animate={float(2)} className="absolute bottom-40 right-20 text-accent-purple opacity-20">
                <Activity size={80} />
            </motion.div>
            <motion.div animate={float(1)} className="absolute top-40 right-40 text-accent-cyan opacity-20">
                <Shield size={48} />
            </motion.div>

            {/* Main Content */}
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="z-10 text-center px-6 max-w-2xl"
            >
                <motion.div
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="mb-6 inline-flex items-center gap-2 px-4 py-2 rounded-full glass-panel text-brand-300 text-sm font-medium"
                >
                    <span className="w-2 h-2 rounded-full bg-brand-400 animate-pulse" />
                    FedHealth AI v2.0
                </motion.div>

                <h1 className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-brand-100 to-brand-300 tracking-tight leading-tight mb-6">
                    A Privacy-First, <br /> Cross-Institutional Diagnostic Framework
                </h1>

                <p className="text-slate-400 text-lg md:text-xl mb-10 leading-relaxed">
                    Experience the future of medical diagnostics.
                    Real-time AI analysis with a fluid, tactile interface designed for precision.
                </p>

                <motion.button
                    whileHover={{ scale: 1.05, boxShadow: "0 0 30px rgba(14, 165, 233, 0.4)" }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => navigate('/dashboard')}
                    className="group relative inline-flex items-center gap-3 px-8 py-4 bg-brand-600 hover:bg-brand-500 text-white rounded-full text-lg font-semibold transition-all shadow-xl shadow-brand-900/50 overflow-hidden"
                >
                    <span className="relative z-10">Enter FedHealth AI</span>
                    <ArrowRight className="relative z-10 w-5 h-5 group-hover:translate-x-1 transition-transform" />

                    {/* Button background flow effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
                </motion.button>
            </motion.div>

            {/* Micro Interaction Footer */}
            <div className="absolute bottom-10 text-slate-600 text-sm flex gap-8">
                <span className="hover:text-brand-400 transition-colors cursor-pointer">Privacy Secure</span>
                <span className="hover:text-brand-400 transition-colors cursor-pointer">HIPAA Compliant</span>
            </div>
        </div>
    );
};

export default Onboarding;
