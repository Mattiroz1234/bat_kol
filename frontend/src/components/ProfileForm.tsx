import React, { useState } from 'react';
import { User, Upload, Save } from 'lucide-react';
import { profileAPI } from '../services/api';
import { User as UserType } from '../types';

interface ProfileFormProps {
  onProfileCreated: (personId: string) => void;
}

const ProfileForm: React.FC<ProfileFormProps> = ({ onProfileCreated }) => {
  const [formData, setFormData] = useState<UserType>({
    email: '',
    first_name: '',
    last_name: '',
    age: 18,
    location: '',
    gender: 'Male',
    marital_status: 'Single',
    origin: 'אשכנזי',
    sector: 'ליטאי',
    free_text_self: '',
    free_text_for_search: '',
    occupation: '',
    favorites: [],
    height: undefined
  });
  
  const [photo, setPhoto] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'age' || name === 'height' ? parseInt(value) || undefined : value
    }));
  };

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setPhoto(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await profileAPI.addPerson(formData, photo || undefined);
      if (response.person_id) {
        onProfileCreated(response.person_id);
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'שגיאה ביצירת הפרופיל');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-2xl card-shadow p-8">
        <div className="text-center mb-8">
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded-full w-16 h-16 mx-auto mb-4">
            <User className="h-10 w-10 text-white mx-auto" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">יצירת פרופיל</h2>
          <p className="text-gray-600">מלא את הפרטים שלך כדי להתחיל למצוא התאמות</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">שם פרטי</label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">שם משפחה</label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">גיל</label>
              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleInputChange}
                min="18"
                max="120"
                className="input-field"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">מגדר</label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleInputChange}
                className="input-field"
                required
              >
                <option value="Male">זכר</option>
                <option value="Female">נקבה</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">גובה (ס"מ)</label>
              <input
                type="number"
                name="height"
                value={formData.height || ''}
                onChange={handleInputChange}
                className="input-field"
                placeholder="אופציונלי"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">מצב משפחתי</label>
              <select
                name="marital_status"
                value={formData.marital_status}
                onChange={handleInputChange}
                className="input-field"
                required
              >
                <option value="Single">רווק/ה</option>
                <option value="Divorced">גרוש/ה</option>
                <option value="Widower">אלמן/ה</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">מוצא</label>
              <select
                name="origin"
                value={formData.origin}
                onChange={handleInputChange}
                className="input-field"
                required
              >
                <option value="אשכנזי">אשכנזי</option>
                <option value="ספרדי">ספרדי</option>
                <option value="תימני">תימני</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">מגזר</label>
              <select
                name="sector"
                value={formData.sector}
                onChange={handleInputChange}
                className="input-field"
                required
              >
                <option value="ליטאי">ליטאי</option>
                <option value="חסידי">חסידי</option>
                <option value="ספרדי">ספרדי</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">מקום מגורים</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">אימייל</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className="input-field"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">מקצוע (אופציונלי)</label>
            <input
              type="text"
              name="occupation"
              value={formData.occupation || ''}
              onChange={handleInputChange}
              className="input-field"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">תיאור עצמי</label>
            <textarea
              name="free_text_self"
              value={formData.free_text_self}
              onChange={handleInputChange}
              rows={4}
              className="input-field resize-none"
              placeholder="ספר/י על עצמך..."
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">מה אני מחפש/ת</label>
            <textarea
              name="free_text_for_search"
              value={formData.free_text_for_search}
              onChange={handleInputChange}
              rows={4}
              className="input-field resize-none"
              placeholder="תאר/י את מי שאת/ה מחפש/ת..."
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">תמונה (אופציונלי)</label>
            <div className="flex items-center space-x-4 space-x-reverse">
              <label className="cursor-pointer bg-gray-50 hover:bg-gray-100 border-2 border-dashed border-gray-300 rounded-lg p-4 flex items-center space-x-2 space-x-reverse transition-colors">
                <Upload className="h-5 w-5 text-gray-400" />
                <span className="text-gray-600">בחר תמונה</span>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handlePhotoChange}
                  className="hidden"
                />
              </label>
              {photo && (
                <span className="text-sm text-green-600">נבחרה תמונה: {photo.name}</span>
              )}
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
                <Save className="h-5 w-5" />
                <span>צור פרופיל</span>
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ProfileForm;