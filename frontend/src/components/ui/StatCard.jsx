import clsx from 'clsx'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

export default function StatCard({ icon: Icon, label, value, sub, trend, color = 'blue' }) {
  const colors = {
    blue:   { bg: 'bg-blue-100',   icon: 'text-blue-600'   },
    green:  { bg: 'bg-green-100',  icon: 'text-green-600'  },
    orange: { bg: 'bg-orange-100', icon: 'text-orange-600' },
    purple: { bg: 'bg-purple-100', icon: 'text-purple-600' },
    red:    { bg: 'bg-red-100',    icon: 'text-red-600'    },
    teal:   { bg: 'bg-teal-100',   icon: 'text-teal-600'   },
  }
  const c = colors[color] || colors.blue

  return (
    <div className="stat-card">
      <div className={clsx('stat-icon', c.bg)}>
        <Icon className={clsx('w-6 h-6', c.icon)} />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-medium text-gray-500 uppercase tracking-wider">{label}</p>
        <div className="flex items-baseline gap-2 mt-0.5">
          <p className="text-2xl font-bold text-gray-900">{value ?? '—'}</p>
          {trend !== undefined && (
            <span className={clsx('flex items-center gap-0.5 text-xs font-medium',
              trend > 0 ? 'text-green-600' : trend < 0 ? 'text-red-500' : 'text-gray-400')}>
              {trend > 0 ? <TrendingUp className="w-3 h-3" /> :
               trend < 0 ? <TrendingDown className="w-3 h-3" /> :
               <Minus className="w-3 h-3" />}
              {Math.abs(trend)}%
            </span>
          )}
        </div>
        {sub && <p className="text-xs text-gray-400 mt-0.5 truncate">{sub}</p>}
      </div>
    </div>
  )
}
