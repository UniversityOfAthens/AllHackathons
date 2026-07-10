import { cn } from '@/lib/utils'

// A single "live" dot that breathes — shrinks + fades, then expands + returns
// (see the `live-pulse` keyframe in index.css). Colour comes from `className`
// (e.g. bg-green-500). Respects reduced-motion.
export default function LiveDot({ className = 'bg-green-500' }: { className?: string }) {
  return (
    <span
      className={cn(
        'inline-block size-2.5 shrink-0 rounded-full animate-live-pulse motion-reduce:animate-none',
        className,
      )}
    />
  )
}
