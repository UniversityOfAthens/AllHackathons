import { useState, useEffect } from 'react';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { Label } from '../components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import type { FeedbackEntry } from '@/types/feedback';

const STORAGE_KEY = 'allhackathons_feedback';

function loadFeedback(): FeedbackEntry[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveFeedback(entries: FeedbackEntry[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
}

export default function Feedback() {
  const [entries, setEntries] = useState<FeedbackEntry[]>(loadFeedback);
  const [isBug, setIsBug] = useState(false);
  const [isFeature, setIsFeature] = useState(false);
  const [isOther, setIsOther] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    saveFeedback(entries);
  }, [entries]);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!message.trim()) return;
    if (!isBug && !isFeature && !isOther) return;

    const type = isBug ? 'bug' : isFeature ? 'feature' : 'other';
    setEntries((prev) => [{ id: crypto.randomUUID(), type, message: message.trim() }, ...prev]);
    setMessage('');
    setIsBug(false);
    setIsFeature(false);
    setIsOther(false);
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Feedback</h1>
          <p className="text-muted-foreground mt-1">Found a bug or have an idea? Let us know.</p>
        </div>

        <div className="flex justify-center mb-10">
          <Card className="w-full max-w-lg">
            <CardHeader>
              <CardTitle className="text-lg">Submit Feedback</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <fieldset className="space-y-2">
                  <Label>Type</Label>
                  <div className="flex gap-4">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={isBug}
                        onChange={(e) => {
                          setIsBug(e.target.checked);
                          if (e.target.checked) {
                            setIsFeature(false);
                            setIsOther(false);
                          }
                        }}
                        className="size-4 rounded border-border accent-foreground"
                      />
                      <span className="text-sm">Bug Report</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={isFeature}
                        onChange={(e) => {
                          setIsFeature(e.target.checked);
                          if (e.target.checked) {
                            setIsBug(false);
                            setIsOther(false);
                          }
                        }}
                        className="size-4 rounded border-border accent-foreground"
                      />
                      <span className="text-sm">Feature Request</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={isOther}
                        onChange={(e) => {
                          setIsOther(e.target.checked);
                          if (e.target.checked) {
                            setIsBug(false);
                            setIsFeature(false);
                          }
                        }}
                        className="size-4 rounded border-border accent-foreground"
                      />
                      <span className="text-sm">Other</span>
                    </label>
                  </div>
                </fieldset>
                <div className="space-y-2">
                  <Label htmlFor="message">Message</Label>
                  <Textarea
                    id="message"
                    placeholder="Describe the bug or feature..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    className="min-h-[120px]"
                    required
                  />
                </div>
                <Button
                  type="submit"
                  className="cursor-pointer"
                  disabled={!isBug && !isFeature && !isOther}
                >
                  Submit
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>

        {entries.length > 0 && (
          <section>
            <h2 className="text-xl font-semibold mb-4">Previous Submissions</h2>
            <div className="space-y-3">
              {entries.map((entry) => (
                <div key={entry.id} className="rounded-lg border p-4">
                  <div className="flex items-center gap-2 mb-1.5">
                    <span
                      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                        entry.type === 'bug'
                          ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                          : entry.type === 'feature'
                            ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                            : 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400'
                      }`}
                    >
                      {entry.type === 'bug' ? (
                        <svg
                          className="mr-1 size-3"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          strokeWidth={2}
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                          />
                        </svg>
                      ) : entry.type === 'feature' ? (
                        <svg
                          className="mr-1 size-3"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          strokeWidth={2}
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                          />
                        </svg>
                      ) : (
                        <svg
                          className="mr-1 size-3"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          strokeWidth={2}
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                          />
                        </svg>
                      )}
                      {entry.type === 'bug'
                        ? 'Bug'
                        : entry.type === 'feature'
                          ? 'Feature'
                          : 'Other'}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
                    {entry.message}
                  </p>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
      <Footer />
    </div>
  );
}
