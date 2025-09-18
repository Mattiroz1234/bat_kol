// Re-saving file to fix potential corruption.
export interface User {
  email: string;
  first_name: string;
  last_name: string;
  age: number;
  location: string;
  gender: 'Male' | 'Female';
  marital_status: 'Single' | 'Divorced' | 'Widower';
  origin: 'ספרדי' | 'אשכנזי' | 'תימני';
  sector: 'חסידי' | 'ליטאי' | 'ספרדי';
  free_text_self: string;
  free_text_for_search: string;
  occupation?: string;
  favorites?: string[];
  height?: number;
  photo?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface WaitingMatch {
  id: string;
  first_name: string;
  last_name: string;
  age: number;
  gender: string;
  location: string;
}

export interface FeedbackData {
  actor_id: string;
  target_id: string;
  status: 'likes' | 'dislikes' | 'waiting';
}