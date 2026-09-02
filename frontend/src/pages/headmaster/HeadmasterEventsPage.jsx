import { useState, useCallback } from 'react'
import { eventApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import Modal from '../../components/ui/Modal'
import {
  BookOpen, Calendar, MapPin, CheckCircle2, Clock,
  Upload, Image, ChevronDown, ChevronUp, AlertCircle
} from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

const TYPE_COLORS = {
  CULTURAL: 'badge-purple', SPORTS: 'badge-green', ACADEMIC: 'badge-blue',
  HEALTH: 'badge-red', NATIONAL_DAY: 'badge-yellow', OTHER: 'badge-gray'
}

export default function HeadmasterEventsPage() {
  const { data: events, loading: eventsLoading } = useApi(() => eventApi.getAll())

  // We fetch each event's my-implementation lazily when the user expands/opens it
  // to avoid N+1 on mount. State: { [eventId]: impl | null }
  const [implCache,   setImplCache]   = useState({})
  const [loadingImpl, setLoadingImpl] = useState({})
  const [expanded,    setExpanded]    = useState({})
  const [showModal,   setShowModal]   = useState(null) // eventId
  const [description, setDescription] = useState('')
  const [saving,      setSaving]      = useState(false)
  const [uploading,   setUploading]   = useState(null) // eventId

  const fetchImpl = useCallback(async (eventId) => {
    if (implCache[eventId] !== undefined || loadingImpl[eventId]) return
    setLoadingImpl(p => ({ ...p, [eventId]: true }))
    try {
      const res = await eventApi.getMyImplementation(eventId)
      setImplCache(p => ({ ...p, [eventId]: res.data.data || null }))
    } catch {
      setImplCache(p => ({ ...p, [eventId]: null }))
    } finally {
      setLoadingImpl(p => ({ ...p, [eventId]: false }))
    }
  }, [implCache, loadingImpl])

  const toggleExpand = (eventId) => {
    fetchImpl(eventId)
    setExpanded(p => ({ ...p, [eventId]: !p[eventId] }))
  }

  const openModal = (event) => {
    fetchImpl(event.id)
    setDescription(implCache[event.id]?.description || '')
    setShowModal(event.id)
  }

  // When modal opens, pre-fill description from cache if available
  const getModalDescription = () => {
    if (showModal && implCache[showModal]?.description) return implCache[showModal].description
    return description
  }

  const handleSave = async () => {
    if (!description.trim()) { toast.error('Please write how you implemented this event'); return }
    setSaving(true)
    try {
      const res = await eventApi.submitImplementation(showModal, description.trim())
      setImplCache(p => ({ ...p, [showModal]: res.data.data }))
      toast.success('Implementation saved!')
      setShowModal(null)
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to save')
    } finally { setSaving(false) }
  }

  const handlePhoto = async (eventId, file) => {
    setUploading(eventId)
    try {
      const res = await eventApi.uploadImplPhoto(eventId, file)
      setImplCache(p => ({ ...p, [eventId]: res.data.data }))
      toast.success('Photo uploaded!')
    } catch (err) {
      toast.error(err.response?.data?.message || 'Upload failed')
    } finally { setUploading(null) }
  }

  if (eventsLoading) return <ListSkeleton items={4} />

  const sorted = (events || []).sort((a, b) => new Date(b.eventDate) - new Date(a.eventDate))

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Events</h1>
          <p className="page-subtitle">Submit your school's implementation report for each event</p>
        </div>
      </div>

      {sorted.length === 0 ? (
        <EmptyState
          icon={BookOpen} title="No events assigned"
          description="The cluster head hasn't created any events yet"
        />
      ) : (
        <div className="space-y-4">
          {sorted.map(event => {
            const impl = implCache[event.id]
            const implemented = !!impl
            const isExpanded = !!expanded[event.id]

            return (
              <div key={event.id}
                className={clsx('card p-5 border-l-4', implemented ? 'border-l-green-400' : 'border-l-orange-400')}>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-3 flex-1 min-w-0">
                    <div className={clsx('w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0',
                      implemented ? 'bg-green-100' : 'bg-orange-100')}>
                      {implemented
                        ? <CheckCircle2 className="w-5 h-5 text-green-600" />
                        : <Clock className="w-5 h-5 text-orange-500" />
                      }
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <h3 className="font-semibold text-gray-900">{event.title}</h3>
                        <span className={clsx('badge', TYPE_COLORS[event.eventType] || 'badge-gray')}>
                          {event.eventType?.replace('_', ' ')}
                        </span>
                        <span className={clsx('badge', implemented ? 'badge-green' : 'badge-yellow')}>
                          {implemented ? 'Implemented' : 'Pending'}
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
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <button
                      onClick={() => { setDescription(implCache[event.id]?.description || ''); openModal(event) }}
                      className={clsx('btn-sm', implemented ? 'btn-secondary' : 'btn-primary')}
                    >
                      {implemented ? 'Edit Report' : 'Submit Report'}
                    </button>
                    <button onClick={() => toggleExpand(event.id)} className="btn-ghost btn-sm p-1.5">
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Expanded implementation details */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-gray-100 space-y-3">
                    {loadingImpl[event.id] && (
                      <p className="text-sm text-gray-400">Loading…</p>
                    )}
                    {!loadingImpl[event.id] && !impl && (
                      <p className="text-sm text-gray-400">No implementation submitted yet.</p>
                    )}
                    {impl && (
                      <>
                        {impl.description && (
                          <div>
                            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Your Report</p>
                            <p className="text-sm text-gray-700 whitespace-pre-wrap">{impl.description}</p>
                          </div>
                        )}
                        {impl.photoPaths?.length > 0 && (
                          <div>
                            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
                              Photos ({impl.photoPaths.length})
                            </p>
                            <div className="flex gap-2 flex-wrap">
                              {impl.photoPaths.map((path, i) => (
                                <a key={i} href={`/uploads/${path}`} target="_blank" rel="noreferrer">
                                  <img src={`/uploads/${path}`} alt={`impl photo ${i + 1}`}
                                    className="w-20 h-20 rounded-lg object-cover border border-gray-200 hover:opacity-80 transition-opacity" />
                                </a>
                              ))}
                            </div>
                          </div>
                        )}
                        <label className={clsx('btn-secondary btn-sm cursor-pointer inline-flex', uploading === event.id && 'opacity-50')}>
                          <Upload className="w-3 h-3" />
                          {uploading === event.id ? 'Uploading…' : 'Add More Photos'}
                          <input type="file" accept="image/*" className="hidden" disabled={uploading === event.id}
                            onChange={e => e.target.files[0] && handlePhoto(event.id, e.target.files[0])} />
                        </label>
                      </>
                    )}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}

      {/* Submit/Edit Modal */}
      {showModal && (
        <Modal
          open={!!showModal}
          onClose={() => setShowModal(null)}
          title={implCache[showModal] ? `Edit Implementation — ${(events || []).find(e => e.id === showModal)?.title}` : `Submit Implementation — ${(events || []).find(e => e.id === showModal)?.title}`}
          footer={
            <>
              <button onClick={() => setShowModal(null)} className="btn-secondary" disabled={saving}>Cancel</button>
              <button onClick={handleSave} className="btn-primary" disabled={saving}>
                {saving ? 'Saving…' : 'Save Report'}
              </button>
            </>
          }
        >
          <div className="space-y-4">
            <div className="form-group">
              <label className="label">How did you implement this event? *</label>
              <textarea
                className="input"
                rows={5}
                placeholder="Describe what activities were conducted, how many students participated, outcomes, challenges faced…"
                value={description}
                onChange={e => setDescription(e.target.value)}
              />
              {!description.trim() && (
                <p className="text-xs text-gray-400 mt-1 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />Description is required
                </p>
              )}
            </div>
            <div className="form-group">
              <label className="label">Upload Photos</label>
              <label className={clsx('btn-secondary btn-sm cursor-pointer inline-flex', uploading === showModal && 'opacity-50')}>
                <Image className="w-3 h-3" />
                {uploading === showModal ? 'Uploading…' : 'Choose Photo'}
                <input type="file" accept="image/*" className="hidden" disabled={uploading === showModal}
                  onChange={e => e.target.files[0] && handlePhoto(showModal, e.target.files[0])} />
              </label>
              {implCache[showModal]?.photoPaths?.length > 0 && (
                <div className="flex gap-2 mt-2 flex-wrap">
                  {implCache[showModal].photoPaths.map((path, i) => (
                    <img key={i} src={`/uploads/${path}`} alt={`photo ${i + 1}`}
                      className="w-16 h-16 rounded-lg object-cover border border-gray-200" />
                  ))}
                </div>
              )}
            </div>
          </div>
        </Modal>
      )}
    </div>
  )
}
