import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { eventApi, schoolApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import ConfirmDialog from '../../components/ui/ConfirmDialog'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import {
  BookOpen, Plus, Trash2, Edit2, Calendar, MapPin,
  AlertCircle, Eye, CheckCircle2, Clock, ChevronDown, ChevronUp, X
} from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

const EVENT_TYPES = ['CULTURAL', 'SPORTS', 'ACADEMIC', 'HEALTH', 'NATIONAL_DAY', 'OTHER']
const TYPE_COLORS = {
  CULTURAL: 'badge-purple', SPORTS: 'badge-green', ACADEMIC: 'badge-blue',
  HEALTH: 'badge-red', NATIONAL_DAY: 'badge-yellow', OTHER: 'badge-gray'
}

function ImplementationsPanel({ event, totalSchools, onClose }) {
  const { data: impls, loading } = useApi(() => eventApi.getImplementations(event.id), [event.id])

  const implMap = {}
  ;(impls || []).forEach(i => { implMap[i.schoolId] = i })

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[85vh] flex flex-col">
        <div className="flex items-center justify-between p-5 border-b border-gray-100">
          <div>
            <h2 className="font-semibold text-gray-900">{event.title} — Implementations</h2>
            <p className="text-xs text-gray-400 mt-0.5">
              {(impls || []).length} of {totalSchools} schools submitted
            </p>
          </div>
          <button onClick={onClose} className="btn-ghost p-1.5"><X className="w-5 h-5" /></button>
        </div>
        <div className="overflow-y-auto flex-1 p-5 space-y-4">
          {loading ? (
            <div className="text-center text-sm text-gray-400 py-8">Loading…</div>
          ) : (impls || []).length === 0 ? (
            <div className="text-center text-sm text-gray-400 py-8">
              No schools have submitted their implementation yet.
            </div>
          ) : (
            (impls || []).map(impl => (
              <div key={impl.id} className="border border-gray-100 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0" />
                  <span className="font-medium text-gray-900">{impl.schoolName}</span>
                  <span className="text-xs text-gray-400 ml-auto">
                    {impl.updatedAt && format(new Date(impl.updatedAt), 'dd MMM yyyy')}
                  </span>
                </div>
                {impl.submittedByName && (
                  <p className="text-xs text-gray-400 mb-2">by {impl.submittedByName}</p>
                )}
                {impl.description && (
                  <p className="text-sm text-gray-700 whitespace-pre-wrap mb-3">{impl.description}</p>
                )}
                {impl.photoPaths?.length > 0 && (
                  <div className="flex gap-2 flex-wrap">
                    {impl.photoPaths.map((path, i) => (
                      <a key={i} href={`/uploads/${path}`} target="_blank" rel="noreferrer">
                        <img src={`/uploads/${path}`} alt={`photo ${i + 1}`}
                          className="w-20 h-20 rounded-lg object-cover border border-gray-200 hover:opacity-80 transition-opacity" />
                      </a>
                    ))}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default function EventsPage() {
  const { data: events, loading, refetch } = useApi(() => eventApi.getAll())
  const { data: schools } = useApi(() => schoolApi.getAll())
  const [showForm,    setShowForm]    = useState(false)
  const [editing,     setEditing]     = useState(null)
  const [deleting,    setDeleting]    = useState(null)
  const [monitoring,  setMonitoring]  = useState(null) // event being monitored
  const [submitting,  setSubmitting]  = useState(false)

  const { register, handleSubmit, reset, formState: { errors } } = useForm()

  const totalSchools = (schools || []).length

  const openCreate = () => { setEditing(null); reset({ eventType: 'CULTURAL' }); setShowForm(true) }
  const openEdit   = (e) => { setEditing(e); reset({ ...e, eventDate: e.eventDate }); setShowForm(true) }

  const onSubmit = async (data) => {
    setSubmitting(true)
    try {
      if (editing) { await eventApi.update(editing.id, data); toast.success('Event updated') }
      else { await eventApi.create(data); toast.success('Event created — all headmasters can now see it') }
      setShowForm(false); refetch()
    } catch (err) { toast.error(err.response?.data?.message || 'Failed to save') }
    finally { setSubmitting(false) }
  }

  const handleDelete = async () => {
    setSubmitting(true)
    try { await eventApi.delete(deleting.id); toast.success('Event deleted'); setDeleting(null); refetch() }
    catch (err) { toast.error(err.response?.data?.message || 'Failed to delete') }
    finally { setSubmitting(false) }
  }

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Events</h1>
          <p className="page-subtitle">Create events for headmasters to implement and monitor progress</p>
        </div>
        <button onClick={openCreate} className="btn-primary"><Plus className="w-4 h-4" />Create Event</button>
      </div>

      {loading ? <ListSkeleton items={4} /> : (events || []).length === 0 ? (
        <EmptyState
          icon={BookOpen} title="No events yet"
          description="Create events that all headmasters will implement at their schools"
          action={<button onClick={openCreate} className="btn-primary"><Plus className="w-4 h-4" />Create Event</button>}
        />
      ) : (
        <div className="space-y-4">
          {(events || []).map(event => (
            <EventRow
              key={event.id}
              event={event}
              totalSchools={totalSchools}
              onEdit={() => openEdit(event)}
              onDelete={() => setDeleting(event)}
              onMonitor={() => setMonitoring(event)}
            />
          ))}
        </div>
      )}

      {/* Create / Edit Modal */}
      <Modal
        open={showForm} onClose={() => setShowForm(false)}
        title={editing ? 'Edit Event' : 'Create Event'}
        footer={
          <>
            <button onClick={() => setShowForm(false)} className="btn-secondary" disabled={submitting}>Cancel</button>
            <button onClick={handleSubmit(onSubmit)} className="btn-primary" disabled={submitting}>
              {submitting ? 'Saving…' : editing ? 'Update' : 'Create Event'}
            </button>
          </>
        }
      >
        <div className="space-y-4">
          <div className="form-group">
            <label className="label">Event Title *</label>
            <input className={`input ${errors.title ? 'input-error' : ''}`}
              placeholder="e.g. Annual Sports Day"
              {...register('title', { required: 'Title is required' })} />
            {errors.title && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.title.message}</p>}
          </div>
          <div className="form-group">
            <label className="label">Description / Instructions</label>
            <textarea className="input" rows={3}
              placeholder="Describe the event and what headmasters should do…"
              {...register('description')} />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="form-group">
              <label className="label">Event Date *</label>
              <input type="date" className={`input ${errors.eventDate ? 'input-error' : ''}`}
                {...register('eventDate', { required: 'Date is required' })} />
              {errors.eventDate && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.eventDate.message}</p>}
            </div>
            <div className="form-group">
              <label className="label">Event Type *</label>
              <select className="input" {...register('eventType', { required: true })}>
                {EVENT_TYPES.map(t => <option key={t} value={t}>{t.replace('_', ' ')}</option>)}
              </select>
            </div>
          </div>
          <div className="form-group">
            <label className="label">Venue</label>
            <input className="input" placeholder="e.g. School Ground" {...register('venue')} />
          </div>
        </div>
      </Modal>

      <ConfirmDialog
        open={!!deleting} onClose={() => setDeleting(null)}
        onConfirm={handleDelete} loading={submitting}
        title="Delete Event" description={`Delete "${deleting?.title}"? All implementation reports will also be removed.`}
      />

      {monitoring && (
        <ImplementationsPanel
          event={monitoring}
          totalSchools={totalSchools}
          onClose={() => setMonitoring(null)}
        />
      )}
    </div>
  )
}

function EventRow({ event, totalSchools, onEdit, onDelete, onMonitor }) {
  const { data: impls } = useApi(() => eventApi.getImplementations(event.id), [event.id])
  const implCount = (impls || []).length

  return (
    <div className="card p-5">
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3 flex-1 min-w-0">
          <div className="w-10 h-10 rounded-xl bg-orange-100 flex items-center justify-center flex-shrink-0">
            <BookOpen className="w-5 h-5 text-orange-600" />
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2 flex-wrap mb-1">
              <h3 className="font-semibold text-gray-900">{event.title}</h3>
              <span className={clsx('badge', TYPE_COLORS[event.eventType] || 'badge-gray')}>
                {event.eventType?.replace('_', ' ')}
              </span>
            </div>
            {event.description && (
              <p className="text-sm text-gray-500 line-clamp-2 mb-1">{event.description}</p>
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
          <button onClick={onMonitor} className="btn-secondary btn-sm flex items-center gap-1.5">
            <Eye className="w-3.5 h-3.5" />
            <span className={clsx(implCount === totalSchools && totalSchools > 0 ? 'text-green-600' : 'text-orange-500')}>
              {implCount}/{totalSchools}
            </span>
          </button>
          <button onClick={onEdit} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-4 h-4" /></button>
          <button onClick={onDelete}
            className="btn-ghost btn-sm p-1.5 text-red-400 hover:text-red-600 hover:bg-red-50">
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Progress bar */}
      {totalSchools > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-50">
          <div className="flex items-center justify-between text-xs text-gray-400 mb-1">
            <span className="flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3 text-green-500" />
              {implCount} implemented
            </span>
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3 text-orange-400" />
              {totalSchools - implCount} pending
            </span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-1.5">
            <div
              className="bg-green-500 h-1.5 rounded-full transition-all"
              style={{ width: `${totalSchools > 0 ? (implCount / totalSchools) * 100 : 0}%` }}
            />
          </div>
        </div>
      )}
    </div>
  )
}
