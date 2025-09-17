import React, { useState, useEffect } from 'react';
import { Heart, X, MapPin, Calendar, User } from 'lucide-react';
import { matchesAPI } from '../services/api';
import { WaitingMatch, FeedbackData } from '../types';

interface MatchesViewProps {
  userId: string;
}

const MatchesView: React.FC<MatchesViewProps> = ({ userId }) => {
  const [matches, setMatches] = useState<WaitingMatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);

  const loadMatches = React.useCallback(async () => {
    try {
      setLoading(true);
      const response = await matchesAPI.getWaitingMatches(userId);
      setMatches(response.waiting || []);
    } catch {
      setError('שגיאה בטעינת ההתאמות');
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    loadMatches();
  }, [loadMatches]);

  const handleFeedback = async (status: 'likes' | 'dislikes') => {
    if (currentIndex >= matches.length) return;

    const currentMatch = matches[currentIndex];
    const feedback: FeedbackData = {
      actor_id: userId,
      target_id: currentMatch.id,
      status
    };

    try {
      await matchesAPI.sendFeedback(feedback);
      
      // Remove current match and move to next
      const newMatches = matches.filter((_, index) => index !== currentIndex);
      setMatches(newMatches);
      
      // Adjust current index if needed
      if (currentIndex >= newMatches.length && newMatches.length > 0) {
        setCurrentIndex(newMatches.length - 1);
      }
    } catch {
      setError('שגיאה בשליחת המשוב');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg text-center">
        {error}
      </div>
    );
  }

  if (matches.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4 rounded-full w-20 h-20 mx-auto mb-6">
          <Heart className="h-12 w-12 text-white mx-auto" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">אין התאמות חדשות</h3>
        <p className="text-gray-600">נחזור אליך כשיהיו התאמות חדשות!</p>
      </div>
    );
  }

  const currentMatch = matches[currentIndex];

  return (
    <div className="max-w-md mx-auto">
      <div className="mb-6 text-center">
        <h2 className="text-2xl font-bold text-white mb-2">התאמות ממתינות</h2>
        <p className="text-white/80">
          {currentIndex + 1} מתוך {matches.length}
        </p>
      </div>

      <div className="profile-card">
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 h-32 flex items-center justify-center">
          <User className="h-16 w-16 text-white" />
        </div>
        
        <div className="p-6">
          <div className="text-center mb-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-1">
              {currentMatch.first_name} {currentMatch.last_name}
            </h3>
            <div className="flex items-center justify-center space-x-4 space-x-reverse text-gray-600">
              <div className="flex items-center space-x-1 space-x-reverse">
                <Calendar className="h-4 w-4" />
                <span>{currentMatch.age}</span>
              </div>
              <div className="flex items-center space-x-1 space-x-reverse">
                <MapPin className="h-4 w-4" />
                <span>{currentMatch.location}</span>
              </div>
            </div>
          </div>

          <div className="flex space-x-4 space-x-reverse">
            <button
              onClick={() => handleFeedback('dislikes')}
              className="flex-1 bg-red-500 hover:bg-red-600 text-white font-medium py-4 px-6 rounded-xl transition-all duration-200 transform hover:scale-105 shadow-lg flex items-center justify-center space-x-2 space-x-reverse"
            >
              <X className="h-6 w-6" />
              <span>לא מתאים</span>
            </button>
            
            <button
              onClick={() => handleFeedback('likes')}
              className="flex-1 bg-green-500 hover:bg-green-600 text-white font-medium py-4 px-6 rounded-xl transition-all duration-200 transform hover:scale-105 shadow-lg flex items-center justify-center space-x-2 space-x-reverse"
            >
              <Heart className="h-6 w-6" />
              <span>מעוניין/ת</span>
            </button>
          </div>
        </div>
      </div>

      {matches.length > 1 && (
        <div className="mt-6 flex justify-center space-x-2 space-x-reverse">
          {matches.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentIndex(index)}
              className={`w-3 h-3 rounded-full transition-colors ${
                index === currentIndex ? 'bg-white' : 'bg-white/30'
              }`}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default MatchesView;