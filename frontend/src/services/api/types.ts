export type AnalysisStatus = 'success' | 'failed';

export interface LongestMessage {
  Author: string;
  Message: string;
  Length: number;
}

export interface TopStreak {
  start: string;
  end: string;
  duration: number;
}

export interface ChatStatsPayload {
  status: AnalysisStatus;
  message: string;
  total_messages: number;
  participants: string[];
  total_users: number;
  n_messages_per_user: Record<string, number>;
  hot_hours: Record<string, number>;
  messages_per_day: Record<string, number>;
  messages_per_month: Record<string, number>;
  messages_per_year: Record<string, number>;
  top_messages_per_day: Record<string, number>;
  top_words: Record<string, number>;
  top_emojis: Record<string, number>;
  longest_messages: LongestMessage[];
  top_streaks: TopStreak[];
}

export interface UploadChatResponse {
  status: 'success';
  stats: ChatStatsPayload;
}

export interface HealthcheckResponse {
  message: string;
}