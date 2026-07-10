import { useState } from 'react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../ui/dialog'
import { Button } from '../ui/button'
import { Textarea } from '../ui/textarea'

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  hackathonName: string
}

// Free-text "suggest an edit" (issue #9). The backend endpoint
// (POST /api/hackathons/:id/change-request) is owned by #5/#9 and doesn't exist yet,
// so for now this just confirms receipt.
export default function RequestChangeModal({ open, onOpenChange, hackathonName }: Props) {
  const [text, setText] = useState('')
  const [sent, setSent] = useState(false)

  function change(next: boolean) {
    onOpenChange(next)
    if (!next) {
      setSent(false)
      setText('')
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!text.trim()) return
    setSent(true)
  }

  return (
    <Dialog open={open} onOpenChange={change}>
      <DialogContent className="sm:max-w-lg">
        {sent ? (
          <div className="py-4 text-center">
            <p className="font-serif text-2xl font-semibold text-foreground">Ευχαριστούμε!</p>
            <p className="mx-auto mt-2 max-w-sm text-muted-foreground">
              Η πρότασή σου στάλθηκε για έλεγχο. Η ομάδα θα τη διασταυρώσει και θα
              ενημερώσει την καταχώρηση.
            </p>
            <Button className="mt-6 cursor-pointer" onClick={() => change(false)}>
              Κλείσιμο
            </Button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">
            <DialogHeader className="space-y-2">
              <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-accent-terracotta">
                Πρότεινε διόρθωση
              </p>
              <DialogTitle className="font-serif text-2xl">Τι πρέπει να αλλάξει;</DialogTitle>
            </DialogHeader>

            <div className="flex flex-wrap items-center gap-2 text-sm">
              <span className="text-muted-foreground">Σχετικά με:</span>
              <span className="rounded-full bg-secondary px-3 py-1 text-xs font-medium text-secondary-foreground">
                {hackathonName}
              </span>
            </div>

            <div className="space-y-2.5">
              <Textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                rows={7}
                autoFocus
                className="min-h-44"
                placeholder={
                  'π.χ. «Η προθεσμία αιτήσεων άλλαξε, τώρα είναι 20 Αυγ, όχι 15.» ή «Το έπαθλο είναι €6.000, όχι €5.000.»'
                }
              />
              <p className="text-xs text-muted-foreground">
                Δεν χρειάζεται φόρμα, γράψε με δικά σου λόγια. Η ομάδα διασταυρώνει και
                ενημερώνει την καταχώρηση.
              </p>
            </div>

            <DialogFooter className="gap-2 pt-1">
              <Button
                type="button"
                variant="ghost"
                className="cursor-pointer"
                onClick={() => change(false)}
              >
                Άκυρο
              </Button>
              <Button type="submit" disabled={!text.trim()} className="cursor-pointer">
                Στείλ&apos; το
              </Button>
            </DialogFooter>
          </form>
        )}
      </DialogContent>
    </Dialog>
  )
}
