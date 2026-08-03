import { useEffect } from 'react'
import { useLocation, useNavigationType } from 'react-router-dom'

// Per-history-entry scroll positions.
const positions = new Map<string, number>()

// Scroll behaviour across client-side navigation:
//   PUSH / REPLACE (a new page)  → jump to the top
//   POP (back / forward)         → restore the saved position
export default function ScrollManager() {
  const location = useLocation()
  const navType = useNavigationType()

  // Track the scroll position of the current history entry.
  useEffect(() => {
    const key = location.key
    const onScroll = () => positions.set(key, window.scrollY)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => {
      positions.set(key, window.scrollY)
      window.removeEventListener('scroll', onScroll)
    }
  }, [location.key])

  // Apply scroll on navigation.
  useEffect(() => {
    if (navType === 'POP') {
      window.scrollTo(0, positions.get(location.key) ?? 0)
    } else {
      window.scrollTo(0, 0)
    }
  }, [location.key, navType])

  return null
}
