import { useState, useCallback, useRef } from 'react'
import { eventApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import { useAuth } from '../../context/AuthContext'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import Modal from '../../components/ui/Modal'
import {
  BookOpen, Calendar, MapPin, CheckCircle2, Clock,
  Upload, AlertCircle, ChevronDown, ChevronUp
} from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

const TYPE_COLORS = {
  CULTURAL: 'badge-purple', SPORTS: 'badge-green', ACADEMIC: 'badge-blue',
  HEALTH: 'badge-red', NATIONAL_DAY: 'badge-yellow', OTHER: 'badge-gray'
}

export default function HeadmasterEventsPage() {
  const { user } = useAuth()
  const hasSchool = !!user?.school?.id
  const { data: events, loading: eventsLoading } = useApi(() => eventApi.getAll())

  const [implCache,   setImplCache]   = useState({})   // { [eventId]: impl | null }
  const [loadingImpl, setLoadingImpl] = useState({})
  const [expanded,    setExpanded]    = useState({})
  const [modalEvent,  setModalEvent]  = useState(null) // full event object
  const [description, setDescription] = useState('')
  const [saving,      setSaving]      = useState(false)
  const [uploading,   setUploading]   = useState(null)

  // Ref so fetchImpl never goes stale
  const implCacheRef    = useRef({})
  const loadingImplRef  = useRef({})

  const fetchImpl = useCallback(async (eventId) => {
    if (implCacheRef.current[eventId] !== undefined) return implCacheRef.current[eventId]
    if (loadingImplRef.current[eventId]) return null
    loadingImplRef.current[eventId] = true
    setLoadingImpl(p => ({ ...p, [eventId]: true }))
    try {
      const res = await eventApi.getMyImplementation(eventId)
      const impl = res.data.data ?? null
      implCacheRef.current[eventId] = impl
      setImplCache(p => ({ ...p, [eventId]: impl }))
      return impl
    } catch {
      implCacheRef.current[eventId] = null
      setImplCache(p => ({ ...p, [eventId]: null }))
      return null
    } finally {
      loadingImplRef.current[eventId] = false
      setLoadingImpl(p => ({ ...p, [eventId]: false }))
    }
  }, [])

  const updateCache = (eventId, impl) => {
    implCacheRef.current[eventId] = impl
    setImplCache(p => ({ ...p, [eventId]: impl }))
  }

  const toggleExpand = (eventId) => {
    fetchImpl(eventId)
    setExpanded(p => ({ ...p, [eventId]: !p[eventId] }))
  }

  const openModal = async (event) => {
    if (!hasSchool) {
      toast.error('You must be assigned to a school by the administrator to submit event reports.')
      return
    }
    const impl = implCacheRef.current[event.id] !== undefined
      ? implCacheRef.current[event.id]
      : await fetchImpl(event.id)
    setDescription(impl?.description || '')
    setModalEvent(event)
  }

  const handleSave = async () => {
    if (!description.trim()) { toast.error('Please describe how you implemented this event'); return }
    setSaving(true)
    try {
      const res = await eventApi.submitImplementation(modalEvent.id, description.trim())
      updateCache(modalEvent.id, res.data.data)
      toast.success('Implementation saved!')
      setModalEvent(null)
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to save')
    } finally { setSaving(false) }
  }

  const handlePhoto = async (eventId, file) => {
    if (!hasSchool) {
      toast.error('You must be assigned to a school by the administrator to upload photos.')
      return
    }
    if (!file) return
    if (file.size > 20 * 1024 * 1024) {
      toast.error('Photo size exceeds the 20MB limit')
      return
    }
    setUploading(eventId)
    try {
      const res = await eventApi.uploadImplPhoto(eventId, file)
      updateCache(eventId, res.data.data)
      toast.success('Photo uploaded!')
    } catch (err) {
      const msg = err.response?.data?.message || (err.response?.status === 413 ? 'Photo too large (max 20MB)' : 'Upload failed')
      toast.error(msg)
    } finally { setUploading(null) }
  }

  if (eventsLoading) return <ListSkeleton items={4} />

  const sorted = [...(events || [])].sort((a, b) => new Date(b.eventDate) - new Date(a.eventDate))

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Events</h1>
          <p className="page-subtitle">Submit your school's implementation report for each event</p>
        </div>
      </div>

      {!hasSchool && (
        <div className="mb-5 p-4 bg-amber-50 border border-amber-200 rounded-xl flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-amber-800">
            <span className="font-semibold">School Assignment Required:</span> Your account is not currently assigned to a school. Please contact the administrator to assign your school before submitting event reports.
          </div>
        </div>
      )}

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
                          {event.eventDate && format(new Date(event.eventDate + 'T00:00:00'), 'dd MMMM yyyy')}
                        </span>
                        {event.venue && (
                          <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{event.venue}</span>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <button
                      onClick={() => openModal(event)}
                      className={clsx('btn-sm', implemented ? 'btn-secondary' : 'btn-primary')}
                    >
                      {implemented ? 'Edit Report' : 'Submit Report'}
                    </button>
                    <button onClick={() => toggleExpand(event.id)} className="btn-ghost btn-sm p-1.5">
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-gray-100 space-y-3">
                    {loadingImpl[event.id] && <p className="text-sm text-gray-400">Loading…</p>}
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
                                <a key={i} href={`/uploads/${path}`} target="_blank" rel="noreferrer" className="group block">
                                  <img src={`/uploads/${path}`} alt={`impl photo ${i + 1}`}
                                    className="w-20 h-20 rounded-lg object-cover border border-gray-200 hover:opacity-80 transition-opacity cursor-pointer shadow-sm bg-gray-50" />
                                </a>
                              ))}
                            </div>
                          </div>
                        )}
                        <label className={clsx('btn-secondary btn-sm cursor-pointer inline-flex items-center gap-1.5', uploading === event.id && 'opacity-50 pointer-events-none')}>
                          <Upload className="w-3 h-3" />
                          {uploading === event.id ? 'Uploading…' : 'Add Photo'}
                          <input type="file" accept="image/*" className="hidden"
                            onChange={e => {
                              const file = e.target.files[0]
                              if (file) handlePhoto(event.id, file)
                              e.target.value = ''
                            }} />
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

      {/* Submit / Edit Modal */}
      {modalEvent && (
        <Modal
          open
          onClose={() => setModalEvent(null)}
          title={`${implCache[modalEvent.id] ? 'Edit' : 'Submit'} Report — ${modalEvent.title}`}
          footer={
            <>
              <button onClick={() => setModalEvent(null)} className="btn-secondary" disabled={saving}>Cancel</button>
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
                placeholder="Describe what activities were conducted, how many students participated, outcomes…"
                value={description}
                onChange={e => setDescription(e.target.value)}
                autoFocus
              />
              {!description.trim() && (
                <p className="text-xs text-gray-400 mt-1 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />Description is required
                </p>
              )}
            </div>

            {/* Photo upload — only available after first save */}
            {implCache[modalEvent.id] && (
              <div className="form-group">
                <label className="label">Upload Photos</label>
                <label className={clsx('btn-secondary btn-sm cursor-pointer inline-flex items-center gap-1.5', uploading === modalEvent.id && 'opacity-50 pointer-events-none')}>
                  <Upload className="w-3 h-3" />
                  {uploading === modalEvent.id ? 'Uploading…' : 'Choose Photo'}
                  <input type="file" accept="image/*" className="hidden"
                    onChange={e => {
                      const file = e.target.files[0]
                      if (file) handlePhoto(modalEvent.id, file)
                      e.target.value = ''
                    }} />
                </label>
                {implCache[modalEvent.id]?.photoPaths?.length > 0 && (
                  <div className="flex gap-2 mt-2 flex-wrap">
                    {implCache[modalEvent.id].photoPaths.map((path, i) => (
                      <a key={i} href={`/uploads/${path}`} target="_blank" rel="noreferrer" className="group block">
                        <img src={`/uploads/${path}`} alt={`photo ${i + 1}`}
                          className="w-16 h-16 rounded-lg object-cover border border-gray-200 hover:opacity-80 transition-opacity cursor-pointer shadow-sm bg-gray-50" />
                      </a>
                    ))}
                  </div>
                )}
              </div>
            )}
            {!implCache[modalEvent.id] && (
              <p className="text-xs text-gray-400">Save the report first, then you can upload photos.</p>
            )}
          </div>
        </Modal>
      )}
    </div>
  )
}
