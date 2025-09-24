import React from 'react';
import { Button } from './ui/button';
import { Brain, BarChart3 } from 'lucide-react';

interface NavigationProps {
  currentPage: 'landing' | 'dashboard';
  setCurrentPage: (page: 'landing' | 'dashboard') => void;
}

export function Navigation({ currentPage, setCurrentPage }: NavigationProps) {
  return (
    <nav className="bg-white/80 backdrop-blur-sm border-b border-purple-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-purple-600" />
            <span className="text-xl font-bold text-gray-900">Pulso Emocional</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <Button
              variant={currentPage === 'landing' ? 'default' : 'ghost'}
              onClick={() => setCurrentPage('landing')}
              className="text-sm"
            >
              Início
            </Button>
            <Button
              variant={currentPage === 'dashboard' ? 'default' : 'ghost'}
              onClick={() => setCurrentPage('dashboard')}
              className="text-sm"
            >
              <BarChart3 className="h-4 w-4 mr-2" />
              Dashboard
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}