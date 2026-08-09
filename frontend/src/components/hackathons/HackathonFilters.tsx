import { cn } from '@/lib/utils'
import { Globe } from 'lucide-react'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

export type ModeFilter = 'all' | 'in-person' | 'online'

const PILLS: { key: ModeFilter; label: string }[] = [
  { key: 'all', label: 'Όλα' },
  { key: 'in-person', label: 'In person' },
  { key: 'online', label: 'Online' },
]

const REGIONS = [
  { value: 'all', label: 'Όλη η Ελλάδα' },
  { value: 'athens', label: 'Αθήνα' },
  { value: 'thessaloniki', label: 'Θεσσαλονίκη' },
  { value: 'patras', label: 'Πάτρα' },
  { value: 'heraklion', label: 'Ηράκλειο' },
]

// Design-pass filter row (issue #3). The full upcoming/past/tag/search logic and
// server-side query params are owned by #14 — this is the visual control + a basic
// client-side mode filter.
export default function HackathonFilters({
  mode,
  onModeChange,
}: {
  mode: ModeFilter
  onModeChange: (m: ModeFilter) => void
}) {
  return (
    <div className="flex flex-wrap items-center gap-3">
      {/* Region — visual control for now; region filtering is a later enhancement. */}
      <Select defaultValue="all" items={REGIONS}>
        <SelectTrigger className="cursor-pointer rounded-full border-input bg-card px-5 py-2.5 data-[size=default]:h-auto">
          <Globe className="size-4 text-muted-foreground" aria-hidden />
          <SelectValue />
        </SelectTrigger>
        <SelectContent sideOffset={4} alignOffset={0} alignItemWithTrigger={false} className="p-2">
          {REGIONS.map((region) => (
            <SelectItem key={region.value} value={region.value} className="cursor-pointer py-2 pl-2.5 pr-8">
              {region.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <div className="hidden h-5 w-px bg-border sm:block" />
      <div className="flex items-center gap-2">
        {PILLS.map((p) => (
          <button
            key={p.key}
            onClick={() => onModeChange(p.key)}
            className={cn(
              'cursor-pointer rounded-full px-4 py-2 text-sm font-medium transition-colors',
              mode === p.key
                ? 'bg-primary text-primary-foreground'
                : 'border border-input text-foreground hover:bg-accent',
            )}
          >
            {p.label}
          </button>
        ))}
      </div>
    </div>
  )
}
