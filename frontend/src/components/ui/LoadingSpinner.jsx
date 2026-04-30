import { X, AlertTriangle, Loader2 } from 'lucide-react'
import clsx from 'clsx'

// ─── LoadingSpinner ───────────────────────────────────────────────────────────
export default function LoadingSpinner({ fullScreen, size = 'md', className }) {
  const sizes = { sm: 'w-4 h-4', md: 'w-6 h-6', lg: 'w-10 h-10' }
  const spinner = (
    <Loader2 className={clsx('animate-spin text-primary-600', sizes[size], className)} />
  )
  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-white">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-10 h-10 animate-spin text-primary-600" />
          <p className="text-sm text-gray-500">Loading…</p>
        </div>
      </div>
    )
  }
  return spinner
}
