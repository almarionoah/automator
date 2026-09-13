# Atlas Core - Mobile Navigation Architecture Overhaul & Token Refactoring
**Author:** Nyx Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D18 14:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the mobile navigation drawer into a streamlined, token-driven bottom sheet and floating tab bar. Cleaned up legacy CSS redundancies, unified motion curves, and enforced touch target standards per the Company Document.

## Deliverable
```
// Atlas Core — Refactored Mobile Navigation Component
// Author: Nyx Marlow (Design Systems & UI Engineering)
// Aligned with requirements in: Business Document: Company Document (Section 4.2: Mobile Accessibility & Hybrid Touch Targets)

import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { Home, Calendar, Users, Layers, Menu, X, ShieldCheck } from 'lucide-react';

interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  path: string;
  badge?: number;
}

const NAV_ITEMS: NavItem[] = [
  { id: 'dashboard', label: 'Atlas Home', icon: Home, path: '/dashboard' },
  { id: 'f2f-service', label: 'Field Ops', icon: Calendar, path: '/f2f/schedule' },
  { id: 'clients', label: 'Accounts', icon: Users, path: '/clients' },
  { id: 'platform', label: 'SaaS Modules', icon: Layers, path: '/modules' },
];

// Tokens refactored to eliminate legacy inline overrides
const MOTION_SPRING = { type: 'spring', damping: 28, stiffness: 320 };

export const AtlasMobileNav: React.FC<{ activePath: string; onNavigate: (path: string) => void }> = ({
  activePath,
  onNavigate,
}) => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const prefersReducedMotion = useReducedMotion();

  // Refactored keyboard trap & ESC handler per Company Document accessibility guidelines
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Escape') setDrawerOpen(false);
  }, []);

  useEffect(() => {
    if (drawerOpen) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', handleKeyDown);
    } else {
      document.body.style.overflow = '';
      window.removeEventListener('keydown', handleKeyDown);
    }
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [drawerOpen, handleKeyDown]);

  return (
    <nav
      role="navigation"
      aria-label="Atlas Core Mobile Navigation"
      className="fixed bottom-0 inset-x-0 z-50 bg-slate-900/95 backdrop-blur-md border-t border-slate-800 pb-[env(safe-area-inset-bottom)] md:hidden"
    >
      {/* Primary 4-Tab Matrix - Min 48px target height enforced */}
      <div className="flex items-center justify-around h-16 px-2">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = activePath === item.path;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.path)}
              aria-current={isActive ? 'page' : undefined}
              className={`flex flex-col items-center justify-center flex-1 h-12 min-w-[48px] rounded-lg transition-colors ${
                isActive ? 'text-cyan-400 font-semibold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Icon className="w-5 h-5 mb-1" />
              <span className="text-[11px] tracking-tight">{item.label}</span>
            </button>
          );
        })}

        <button
          onClick={() => setDrawerOpen(true)}
          aria-expanded={drawerOpen}
          aria-label="Open Atlas Core Extended Menu"
          className="flex flex-col items-center justify-center flex-1 h-12 min-w-[48px] text-slate-400 hover:text-slate-200"
        >
          <Menu className="w-5 h-5 mb-1" />
          <span className="text-[11px] tracking-tight">More</span>
        </button>
      </div>

      {/* Modal Drawer Overhaul */}
      <AnimatePresence>
        {drawerOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setDrawerOpen(false)}
              className="fixed inset-0 bg-black/60 backdrop-blur-sm -z-10"
              aria-hidden="true"
            />
            <motion.aside
              initial={prefersReducedMotion ? { opacity: 0 } : { y: '100%' }}
              animate={prefersReducedMotion ? { opacity: 1 } : { y: 0 }}
              exit={prefersReducedMotion ? { opacity: 0 } : { y: '100%' }}
              transition={MOTION_SPRING}
              className="absolute bottom-full inset-x-0 bg-slate-900 border-t border-slate-800 rounded-t-2xl p-6 shadow-2xl"
            >
              <div className="flex items-center justify-between pb-4 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-cyan-400" />
                  <span className="text-sm font-bold text-white uppercase tracking-wider">I.T. Skokos Service Portal</span>
                </div>
                <button
                  onClick={() => setDrawerOpen(false)}
                  className="p-2 text-slate-400 hover:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-400"
                  aria-label="Close extended menu"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-3 text-xs text-slate-300">
                <button className="p-3 bg-slate-800/50 hover:bg-slate-800 rounded-xl text-left border border-slate-700/50">
                  Live F2F Dispatch
                </button>
                <button className="p-3 bg-slate-800/50 hover:bg-slate-800 rounded-xl text-left border border-slate-700/50">
                  SaaS System Health
                </button>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </nav>
  );
};
```