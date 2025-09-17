import React from 'react';
import { Heart, Users, LogOut } from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
  title?: string;
  showHeader?: boolean;
  onLogout?: () => void;
}

const Layout: React.FC<LayoutProps> = ({ 
  children, 
  title = "פלטפורמת שידוכים", 
  showHeader = true,
  onLogout 
}) => {
  return (
    <div className="min-h-screen gradient-bg">
      {showHeader && (
        <header className="bg-white/10 backdrop-blur-md border-b border-white/20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center space-x-3 space-x-reverse">
                <div className="bg-gradient-to-r from-pink-500 to-purple-600 p-2 rounded-lg">
                  <Heart className="h-6 w-6 text-white" />
                </div>
                <h1 className="text-xl font-bold text-white">{title}</h1>
              </div>
              
              <div className="flex items-center space-x-4 space-x-reverse">
                <div className="flex items-center space-x-2 space-x-reverse text-white/80">
                  <Users className="h-5 w-5" />
                  <span className="text-sm">מחוברים יחד</span>
                </div>
                
                {onLogout && (
                  <button
                    onClick={onLogout}
                    className="flex items-center space-x-2 space-x-reverse text-white/80 hover:text-white transition-colors"
                  >
                    <LogOut className="h-5 w-5" />
                    <span className="text-sm">יציאה</span>
                  </button>
                )}
              </div>
            </div>
          </div>
        </header>
      )}
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
};

export default Layout;