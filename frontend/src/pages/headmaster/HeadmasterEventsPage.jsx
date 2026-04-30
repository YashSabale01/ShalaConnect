import { eventApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import { BookOpen, Calendar, MapPin, Image, FileText, Download } from 'lucide-react'
import { format } from 'date-fns'
import clsx from 'clsx'

const TYPE_COLORS = {
  CULTURAL:'badge-purple', SPORTS:'badge-green', ACADEMIC:'badge-blue',
  HEALTH:'badge-red', NATIONAL_DAY:'badge-yellow', OTHER:'badge-gray'
}

export default function HeadmasterEventsPage() {
  const { data: events, loading } = useApi(() => eventApi.getAll())

  if (loading) return <ListSkeleton items={4} />

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Events</h1>
          <p className="page-subtitle">School events and activities</p>
        </div>
      </div>

      {(events || []).length === 0 ? (
        <EmptyState
          icon={BookOpen}
          title="No events yet"
          description="Events added by the admin will appear here"
        />
      ) : (
        <div className="space-y-4">
          {(events || []).map(event => (
            <div key={event.id} className="card p-5">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 rounded-xl bg-orange-100 flex items-center justify-center flex-shrink-0">
                  <BookOpen className="w-5 h-5 text-orange-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <h3 className="font-semibold text-gray-900">{event.title}</h3>
                    <span className={clsx('badge', TYPE_COLORS[event.eventType] || 'badge-gray')}>
                      {event.eventType?.replace('_', ' ')}
                    </span>
                  </div>
                  {event.description && (
                    <p className="text-sm text-gray-500 mb-2">{event.description}</p>
                  )}
                  <div className="flex flex-wrap gap-4 text-xs text-gray-400">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {event.eventDate && format(new Date(event.eventDate), 'dd MMMM yyyy')}
                    </span>
                    {event.venue && (
                      <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{event.venue}</span>
                    )}
                    {event.mediaPaths?.length > 0 && (
                      <span className="flex items-center gap-1">
                        <Image className="w-3 h-3" />{event.mediaPaths.length} photo{event.mediaPaths.length !== 1 ? 's' : ''}
                      </span>
                    )}
                  </div>

                  {/* Media thumbnails */}
                  {event.mediaPaths?.length > 0 && (
                    <div className="flex gap-2 mt-3 flex-wrap">
                      {event.mediaPaths.slice(0, 4).map((path, i) => (
                        <a key={i} href={`/uploads/${path}`} target="_blank" rel="noreferrer">
                          <img src={`/uploads/${path}`} alt={`Event photo ${i + 1}`}
                            className="w-16 h-16 rounded-lg object-cover border border-gray-200 hover:opacity-80 transition-opacity" />
                        </a>
                      ))}
                      {event.mediaPaths.length > 4 && (
                        <div className="w-16 h-16 rounded-lg bg-gray-100 flex items-center justify-center text-xs text-gray-500 font-medium">
                          +{event.mediaPaths.length - 4}
                        </div>
                      )}
                    </div>
                  )}

                  {event.reportPath && (
                    <a
                      href={`/uploads/${event.reportPath}`}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1.5 mt-3 text-xs text-primary-600 hover:underline font-medium"
                    >
                      <FileText className="w-3.5 h-3.5" />
                      Download Event Report
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
