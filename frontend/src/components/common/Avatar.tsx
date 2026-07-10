import { cn } from '@/lib/utils'
import { avatarColor, initials } from '@/lib/avatar'

// A generated initials avatar. No image is stored or fetched — the colour and
// letters are derived from `name`. Size/border come from `className`.
export default function Avatar({
  name,
  className,
}: {
  name: string
  className?: string
}) {
  const display = name.replace(/^@/, '')
  return (
    <span
      className={cn(
        'flex items-center justify-center rounded-full font-mono font-semibold text-white',
        className,
      )}
      style={{ backgroundColor: avatarColor(name) }}
      title={display}
      aria-label={display}
    >
      {initials(name)}
    </span>
  )
}
