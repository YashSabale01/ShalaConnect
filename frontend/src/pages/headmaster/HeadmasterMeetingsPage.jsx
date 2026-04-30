import { meetingApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import { CalendarDays, Video, MapPin, Clock, CheckCircle2, ExternalLink } from 'lucide-react'
import toast from 'react-hot-toast'
import { format, isPast } from 'date-fns'
import clsx from 'clsx'

export default function HeadmasterMeetingsPage() {
  const { data: meetings, loading, refetch } = useApi(() => meetingApi.getAll())

  const handleAcknowledge = async (meeting) => {
    if (meeting.acknowledgedByCurrentUser) return
    try {
      await meetingApi.acknowledge(meeting.id)
      toast.success('Meeting acknowledged!')
      refetch()
    } catch { toast.error('Failed to acknowledge') }
  }

  const upcomingMeetings = (meetings || []).filter(m =>
    m.scheduledAt && !isPast(new Date(m.scheduledAt))
  )
  const pastMeetings = (meetings || []).filter(m =>
    m.scheduledAt && isPast(new Date(m.scheduledAt))
  )

  const MeetingCard = ({ m }) => (
    <div className={clsx(
      'card p-5 border-l-4',
      m.acknowledgedByCurrentUser ? 'border-l-green-400' : 'border-l-amber-400'
    )}>
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-4 flex-1 min-w-0">
          <div className={clsx(
            'w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0',
            m.meetingType === 'ONLINE' ? 'bg-blue-100' : 'bg-purple-100'
          )}>
            {m.meetingType === 'ONLINE'
              ? <Video className="w-5 h-5 text-blue-600" />
              : <MapPin className="w-5 h-5 text-purple-600" />
            }
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap mb-1">
              <h3 className="font-semibold text-gray-900">{m.title}</h3>
              <span className={clsx('badge', m.meetingType === 'ONLINE' ? 'badge-blue' : 'badge-purple')}>
                {m.meetingType}
              </span>
            </div>
            {m.agenda && <p className="text-sm text-gray-500 mb-2 line-clamp-2">{m.agenda}</p>}
            <div className="flex flex-wrap gap-4 text-xs text-gray-400">
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {m.scheduledAt && format(new Date(m.scheduledAt), 'dd MMM yyyy, hh:mm a')}
              </span>
              {m.venue && <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{m.venue}</span>}
            </div>
            {m.meetingLink && (
              <a
                href={m.meetingLink}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 text-xs text-primary-600 hover:underline mt-1.5"
              >
                <ExternalLink className="w-3 h-3" />
                Join Meeting Link
              </a>
            )}
          </div>
        </div>

        <div className="flex-shrink-0">
          {m.acknowledgedByCurrentUser ? (
            <div className="flex items-center gap-1.5 text-sm text-green-600 font-medium">
              <CheckCircle2 className="w-5 h-5" />
              <span className="hidden sm:inline">Acknowledged</span>
            </div>
          ) : (
            <button
              onClick={() => handleAcknowledge(m)}
              className="btn-primary btn-sm"
            >
              Acknowledge
            </button>
          )}
        </div>
      </div>
    </div>
  )

  if (loading) return <ListSkeleton items={4} />

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Meetings</h1>
          <p className="page-subtitle">View and acknowledge scheduled meetings</p>
        </div>
      </div>

      {(meetings || []).length === 0 ? (
        <EmptyState
          icon={CalendarDays}
          title="No meetings scheduled"
          description="Meetings scheduled by the admin will appear here"
        />
      ) : (
        <div className="space-y-6">
          {upcomingMeetings.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Upcoming ({upcomingMeetings.length})
              </h2>
              <div className="space-y-3">
                {upcomingMeetings.map(m => <MeetingCard key={m.id} m={m} />)}
              </div>
            </div>
          )}
          {pastMeetings.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
                Past ({pastMeetings.length})
              </h2>
              <div className="space-y-3 opacity-70">
                {pastMeetings.map(m => <MeetingCard key={m.id} m={m} />)}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
