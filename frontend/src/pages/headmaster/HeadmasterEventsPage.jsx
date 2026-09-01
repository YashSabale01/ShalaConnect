import { useState, useRef } from 'react'
import { useForm } from 'react-hook-form'
import { eventApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import ConfirmDialog from '../../components/ui/ConfirmDialog'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import {
  BookOpen, Plus, Calendar, MapPin, Image, FileText,
  Upload, Edit2, Trash2, AlertCircle
} from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

const EVENT_TYPES = ['CULTURAL', 'SPORTS', 'ACADEMIC', 'HEALTH', 'NATIONAL_DAY', 'OTHER']
const TYPE_COLORS = {
  CULTURAL: 'badge-purple', SPORTS: 'badge-green', ACADEMIC: 'badge-blue',
  HEALTH: 'badge-red', NATIONAL_DAY: 'badge-yellow', OTHER: 'badge-gray'
}

export default function HeadmasterEventsPage() {
  const { data: events, loading, refetch } = useApi(() => eventApi.getAll())
  const [showForm,   setShowForm]   = useState(false)
  const [editing,    setEditing]    = useState(null)
  const [deleting,   setDeleting]   = useState(null)
  const [uploading,  setUploading]  = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const { register, handleSubmit, reset, formState: { errors } } = useForm()

  const openCreate = () => { setEditing(null); reset({ eventType: 'CULTURAL' }); setShowForm(true) }
  const openEdit   = (e) => { setEditing(e); reset({ ...e, eventDate: e.eventDate }); setShowForm(true) }

  const onSubmit = async (data) => {
    setSubmitting(true)
    try {
      if (editing) { await eventApi.update(editing.id, data); toast.success('Event updated') }
      else { await eventApi.create(data); toast.success('Event created!') }
      setShowForm(false); refetch()
    } catch (err) { toast.error(err.response?.data?.message || 'Failed to save') }
    finally { setSubmitting(false) }
  }

  const handleDelete = async () => {
    setSubmitting(true)
    try { await eventApi.delete(deleting.id); toast.success('Event deleted'); setDeleting(null); refetch() }
    catch { toast.error('Failed to delete') }
    finally { setSubmitting(false) }
  }

  const handleFileUpload = async (eventId, file, type) => {
    setUploading({ id: eventId, type })
    try {
      if (type === 'media') await eventApi.uploadMedia(eventId, file)
      else await eventApi.uploadReport(eventId, file)
      toast.success(`${type === 'media' ? 'Photo' : 'Report'} uploaded!`)
      refetch()
    } catch { toast.error('Upload failed') }
    finally { setUploading(null) }
  }

  if (loading) return <ListSkeleton items={4} />

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Events</h1>
          <p className="page-subtitle">Document school events and activities</p>
        </div>
        <button onClick={openCreate} className="btn-primary"><Plus className="w-4 h-4" />Add Event</button>
      </div>

      {(events || []).length === 0 ? (
        <EmptyState
          icon={BookOpen} title="No events yet"
          description="Add school events and cultural activities"
          action={<button onClick={openCreate} className="btn-primary"><Plus className="w-4 h-4" />Add Event</button>}
        />
      ) : (
        <div className="space-y-4">
          {(events || []).map(event => (
            <div key={event.id} className="card p-5">
              <div className="flex items-start justify-between gap-4 mb-3">
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
                    {event.description && <p className="text-sm text-gray-500 line-clamp-2 mb-1">{event.description}</p>}
                    <div className="flex flex-wrap gap-4 text-xs text-gray-400">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {event.eventDate && format(new Date(event.eventDate), 'dd MMMM yyyy')}
                      </span>
                      {event.venue && <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{event.venue}</span>}
                      <span className="flex items-center gap-1"><Image className="w-3 h-3" />{event.mediaPaths?.length || 0} photos</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2 flex-shrink-0">
                  <button onClick={() => openEdit(event)} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-4 h-4" /></button>
                  <button onClick={() => setDeleting(event)}
                    className="btn-ghost btn-sm p-1.5 text-red-400 hover:text-red-600 hover:bg-red-50">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Media thumbnails */}
              {event.mediaPaths?.length > 0 && (
                <div className="flex gap-2 mb-3 flex-wrap">
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

              {/* Upload buttons */}
              <div className="flex gap-2 pt-3 border-t border-gray-50 flex-wrap">
                <label className={clsx('btn-secondary btn-sm cursor-pointer',
                  uploading?.id === event.id && uploading?.type === 'media' && 'opacity-50')}>
                  <Upload className="w-3 h-3" />
                  {uploading?.id === event.id && uploading?.type === 'media' ? 'Uploading…' : 'Add Photo'}
                  <input type="file" accept="image/*" className="hidden"
                    onChange={e => e.target.files[0] && handleFileUpload(event.id, e.target.files[0], 'media')} />
                </label>
                <label className={clsx('btn-secondary btn-sm cursor-pointer',
                  uploading?.id === event.id && uploading?.type === 'report' && 'opacity-50')}>
                  <FileText className="w-3 h-3" />
                  {uploading?.id === event.id && uploading?.type === 'report' ? 'Uploading…' : event.reportPath ? 'Replace Report' : 'Upload Report'}
                  <input type="file" accept=".pdf,image/*" className="hidden"
                    onChange={e => e.target.files[0] && handleFileUpload(event.id, e.target.files[0], 'report')} />
                </label>
                {event.reportPath && (
                  <a href={`/uploads/${event.reportPath}`} target="_blank" rel="noreferrer" className="btn-secondary btn-sm">
                    <FileText className="w-3 h-3" />View Report
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

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
            <label className="label">Description</label>
            <textarea className="input" rows={3} placeholder="Event details…" {...register('description')} />
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
        title="Delete Event" description={`Delete "${deleting?.title}"?`}
      />
    </div>
  )
}
