import Link from "next/link";
import { Shield, Sparkles, Database, FileText, Lock, ArrowRight } from "lucide-react";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 md:p-24 relative overflow-hidden">
      {/* Background ambient lighting */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-blue-500/10 blur-[120px] rounded-full pointer-events-none" />

      <div className="z-10 max-w-5xl w-full flex flex-col items-center text-center space-y-8">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-blue-500/30 bg-blue-500/10 text-blue-400 text-xs font-semibold uppercase tracking-wider backdrop-blur-sm">
          <Sparkles className="w-3.5 h-3.5" />
          Enterprise Claims & Policy Intelligence
        </div>

        {/* Title */}
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white max-w-4xl">
          Hybrid SQL + Vector Intelligence for{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-teal-300">
            Insurance Operations
          </span>
        </h1>

        {/* Subtitle */}
        <p className="text-lg md:text-xl text-slate-400 max-w-2xl">
          Accurate policy interpretations, verified claim queries, and comprehensive coverage reasoning powered by LangGraph, pgvector, and deterministic tools.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row gap-4 pt-4">
          <Link
            href="/login"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium shadow-lg shadow-blue-500/25 transition-all duration-200"
          >
            Access Portal
            <ArrowRight className="w-4 h-4" />
          </Link>
          <a
            href="http://localhost:8005/docs"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-slate-200 font-medium transition-all duration-200"
          >
            Backend API Docs
          </a>
        </div>

        {/* Pillars Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-12 w-full text-left">
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-sm hover:border-slate-700 transition">
            <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400 mb-4">
              <Database className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Deterministic SQL</h3>
            <p className="text-sm text-slate-400">
              Zero-hallucination queries over claims, customers, policies, and hospital networks using parameterized tools.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-sm hover:border-slate-700 transition">
            <div className="w-10 h-10 rounded-lg bg-teal-500/10 flex items-center justify-center text-teal-400 mb-4">
              <FileText className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Policy RAG</h3>
            <p className="text-sm text-slate-400">
              Hybrid vector & full-text search across complex insurance policy terms, exclusions, and waiting periods.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-sm hover:border-slate-700 transition">
            <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4">
              <Shield className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Guardrails & Security</h3>
            <p className="text-sm text-slate-400">
              Multi-stage guardrail engine, JWT invalidation, Fernet encrypted secrets, and comprehensive evaluation runner.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
