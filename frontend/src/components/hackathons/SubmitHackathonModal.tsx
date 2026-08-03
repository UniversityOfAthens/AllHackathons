import { useState } from 'react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../ui/dialog'
import { Button } from '../ui/button'
import { Input } from '../ui/input'
import { Textarea } from '../ui/textarea'
import { Label } from '../ui/label'
import { Switch } from '../ui/switch'
import type { Hackathon } from '@/types/hackathon'

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (hackathon: Hackathon) => void
}

export default function SubmitHackathonModal({ open, onOpenChange, onSubmit }: Props) {
  const [name, setName] = useState('')
  const [startDate, setStartDate] = useState('')
  const [hasPrize, setHasPrize] = useState(false)
  const [prizeDetails, setPrizeDetails] = useState('')
  const [location, setLocation] = useState('')
  const [url, setUrl] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const nameTrimmed = name.trim()
    const urlTrimmed = url.trim()
    if (!nameTrimmed && !urlTrimmed) return
    const loc = location.trim()
    onSubmit({
      id: crypto.randomUUID(),
      name: nameTrimmed || urlTrimmed || 'Untitled Hackathon',
      startDate: startDate.trim() || undefined,
      hasPrize: hasPrize || undefined,
      prizeDetails: hasPrize ? prizeDetails.trim() : undefined,
      location: loc || undefined,
      url: urlTrimmed || undefined,
      status: 'published',
    })
    setName('')
    setStartDate('')
    setHasPrize(false)
    setPrizeDetails('')
    setLocation('')
    setUrl('')
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
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
          <p className="text-xs text-muted-foreground">Name or Link is required. Fill in as much as you know.</p>
          <DialogFooter>
            <Button type="button" variant="outline" className="cursor-pointer" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" className="cursor-pointer">Submit</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
