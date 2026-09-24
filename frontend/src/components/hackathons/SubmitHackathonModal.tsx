import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '../ui/dialog';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Label } from '../ui/label';
import { Switch } from '../ui/switch';
import { submitHackathon } from '@/lib/api';
import { addMySubmission } from '@/lib/store';

interface Props {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCreated?: () => void;
}

export default function SubmitHackathonModal({ open, onOpenChange, onCreated }: Props) {
  const [name, setName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [hasPrize, setHasPrize] = useState(false);
  const [prizeDetails, setPrizeDetails] = useState('');
  const [location, setLocation] = useState('');
  const [url, setUrl] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successStatus, setSuccessStatus] = useState<string | null>(null);

  function resetAndClose(created?: { status: string }) {
    setName('');
    setStartDate('');
    setHasPrize(false);
    setPrizeDetails('');
    setLocation('');
    setUrl('');
    setError(null);
    if (created) addMySubmission(created as never);
    onOpenChange(false);
    setTimeout(() => setSuccessStatus(null), 300);
    onCreated?.();
  }

  function handleOpenChange(next: boolean) {
    onOpenChange(next);
    if (!next) {
      setError(null);
      setSuccessStatus(null);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const nameTrimmed = name.trim();
    const urlTrimmed = url.trim();
    if (!nameTrimmed && !urlTrimmed) {
      setError('Provide at least name or link');
      return;
    }
    setSubmitting(true);
    setError(null);
    setSuccessStatus(null);
    try {
      const created = await submitHackathon({
        ...(nameTrimmed ? { name: nameTrimmed } : {}),
        ...(urlTrimmed ? { url: urlTrimmed } : {}),
        startDate: startDate.trim() || undefined,
        hasPrize: hasPrize || undefined,
        prizeDetails: hasPrize ? prizeDetails.trim() || undefined : undefined,
        location: location.trim() || undefined,
      });
      setSuccessStatus(created.status);
      // brief success feedback before closing so user sees published vs pending
      setTimeout(() => resetAndClose(created), 900);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Submit failed');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Submit a Hackathon</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              placeholder="e.g. ETHGlobal Bangkok"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="startDate">Start Date</Label>
            <Input
              id="startDate"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div className="flex items-center justify-between">
            <Label htmlFor="hasPrize">Prize</Label>
            <Switch id="hasPrize" checked={hasPrize} onCheckedChange={setHasPrize} />
          </div>
          {hasPrize && (
            <div className="space-y-2">
              <Label htmlFor="prizeDetails">Prize Details</Label>
              <Textarea
                id="prizeDetails"
                placeholder="e.g. $10,000 USD + free travel"
                value={prizeDetails}
                onChange={(e) => setPrizeDetails(e.target.value)}
              />
            </div>
          )}
          <div className="space-y-2">
            <Label htmlFor="location">Location</Label>
            <Input
              id="location"
              placeholder="e.g. Bangkok, Thailand"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="url">Link</Label>
            <Input
              id="url"
              placeholder="e.g. https://ethglobal.com"
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
          </div>
          {error && <p className="text-xs text-destructive">{error}</p>}
          {successStatus && (
            <p className="text-xs text-accent-green">
              {successStatus === 'published'
                ? '✓ Published — live on the list'
                : `Status: ${successStatus} — pending review`}
            </p>
          )}
          <p className="text-xs text-muted-foreground">
            Name or Link is required. Fill in as much as you know.
          </p>
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              className="cursor-pointer"
              onClick={() => handleOpenChange(false)}
              disabled={submitting}
            >
              Cancel
            </Button>
            <Button type="submit" className="cursor-pointer" disabled={submitting}>
              {submitting ? 'Submitting…' : 'Submit'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
