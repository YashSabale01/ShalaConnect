import { useState, useEffect, useRef } from 'react'
import { Bell, CheckCheck } from 'lucide-react'
import { notificationApi } from '../../services/api'
import { format } from 'date-fns'
import toast from 'react-hot-toast'
import clsx from 'clsx'

export default function NotificationBell() {
  const [open, setOpen]             = useState(false)
  const [notifications, setNotifs]  = useState([])
  const [unreadCount, setCount]     = useState(0)
  const ref = useRef(null)

  const fetchCount = async () => {
    try {
      const res = await notificationApi.getCount()
      setCount(res.data.data.count)
    } catch {}
  }

  const fetchAll = async () => {
    try {
      const res = await notificationApi.getAll()
      setNotifs(res.data.data || [])
      setCount(res.data.data?.filter(n => !n.read).length || 0)
    } catch {}
  }

  useEffect(() => {
    fetchCount()
    const interval = setInterval(fetchCount, 30000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    if (open) fetchAll()
  }, [open])

  useEffect(() => {
    const handleClick = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false) }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  const markAllRead = async () => {
    try {
      await notificationApi.markAllRead()
      setNotifs(prev => prev.map(n => ({ ...n, read: true })))
      setCount(0)
      toast.success('All notifications marked as read')
    } catch {}
  }

  const markRead = async (id) => {
    try {
      await notificationApi.markRead(id)
      setNotifs(prev => prev.map(n => n.id === id ? { ...n, read: true } : n))
      setCount(prev => Math.max(0, prev - 1))
    } catch {}
  }

  const typeColors = {
    GR_DOCUMENT: 'bg-blue-500',
    MEETING:     'bg-purple-500',
    FORM:        'bg-green-500',
    EVENT:       'bg-orange-500',
    GENERAL:     'bg-gray-500',
  }

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className="relative p-2 rounded-lg text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 w-4 h-4 rounded-full bg-red-500 text-white text-[10px] font-bold flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 top-11 w-80 bg-white rounded-xl shadow-2xl border border-gray-100 z-50 animate-slide-up overflow-hidden">
          <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100">
            <h3 className="font-semibold text-gray-900 text-sm">Notifications</h3>
            {unreadCount > 0 && (
              <button onClick={markAllRead} className="flex items-center gap-1 text-xs text-primary-600 hover:text-primary-700 font-medium">
                <CheckCheck className="w-3.5 h-3.5" />
                Mark all read
              </button>
            )}
          </div>

          <div className="max-h-80 overflow-y-auto divide-y divide-gray-50">
            {notifications.length === 0 ? (
              <div className="py-10 text-center">
                <Bell className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                <p className="text-sm text-gray-400">No notifications</p>
              </div>
            ) : (
              notifications.slice(0, 20).map(n => (
                <button
                  key={n.id}
                  onClick={() => !n.read && markRead(n.id)}
                  className={clsx(
                    'w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors',
                    !n.read && 'bg-blue-50/50'
                  )}
                >
                  <div className="flex items-start gap-3">
                    <div className={clsx('w-2 h-2 rounded-full mt-1.5 flex-shrink-0',
                      typeColors[n.type] || 'bg-gray-400')} />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-gray-900 truncate">{n.title}</div>
                      <div className="text-xs text-gray-500 mt-0.5 line-clamp-2">{n.message}</div>
                      <div className="text-[10px] text-gray-400 mt-1">
                        {n.createdAt && format(new Date(n.createdAt), 'dd MMM, hh:mm a')}
                      </div>
                    </div>
                    {!n.read && <div className="w-1.5 h-1.5 rounded-full bg-primary-500 mt-1.5 flex-shrink-0" />}
                  </div>
                </button>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}
