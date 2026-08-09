export interface FeedbackEntry {
  id: string;
  type: 'bug' | 'feature' | 'other';
  message: string;
}
