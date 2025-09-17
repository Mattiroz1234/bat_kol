import React, { useState } from 'react';
import { Mail, Lock, UserPlus, LogIn } from 'lucide-react';
import { authAPI } from '../services/api';
import { LoginData } from '../types';

interface LoginFormProps {
  onLoginSuccess: (token: string) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onLoginSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState<LoginData>({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        const response = await authAPI.login(formData);
        onLoginSuccess(response.access_token);
      } else {
        await authAPI.register(formData);
        setIsLogin(true);
        setError('');
        alert('נרשמת בהצלחה! כעת תוכל להתחבר');
      }
    } catch (err: unknown) {
        // @ts-expect-error: err is of type unknown
        const errorMessage = err.response?.data?.detail || 'שגיאה בהתחברות';
        setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-2xl card-shadow p-8">
          <div className="text-center mb-8">
            <div className="bg-gradient-to-r from-pink-500 to-purple-600 p-3 rounded-full w-16 h-16 mx-auto mb-4">
              <UserPlus className="h-10 w-10 text-white mx-auto" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              {isLogin ? 'התחברות' : 'הרשמה'}
            </h2>
            <p className="text-gray-600">
              {isLogin ? 'התחבר לחשבון שלך' : 'צור חשבון חדש'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                כתובת אימייל
              </label>
              <div className="relative">
                <Mail className="absolute right-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="input-field pr-10"
                  placeholder="הכנס את כתובת האימייל"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                סיסמה
              </label>
              <div className="relative">
                <Lock className="absolute right-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  className="input-field pr-10"
                  placeholder="הכנס סיסמה"
                  required
                />
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary flex items-center justify-center space-x-2 space-x-reverse"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                <>
                  {isLogin ? <LogIn className="h-5 w-5" /> : <UserPlus className="h-5 w-5" />}
                  <span>{isLogin ? 'התחבר' : 'הירשם'}</span>
                </>
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-blue-600 hover:text-blue-500 font-medium"
            >
              {isLogin ? 'אין לך חשבון? הירשם כאן' : 'יש לך חשבון? התחבר כאן'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;