import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { meetingApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import ConfirmDialog from '../../components/ui/ConfirmDialog'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import {
  CalendarDays, Plus, Trash2, Edit2, Users,
  Video, MapPin, Clock, CheckCircle2, AlertCircle
} from 'lucide-react'
import toast from 'react-hot-toast'
import { format, isPast } from 'date-fns'
import clsx from 'clsx'

export default function MeetingsPage() {
  const { data: meetings, loading, refetch } = useApi(() => meetingApi.getAll())
  const [showForm,   setShowForm]   = useState(false)
  const [editing,    setEditing]    = useState(null)
  const [deleting,   setDeleting]   = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const { register, handleSubmit, reset, watch, formState: { errors } } = useForm()
  const meetingType = watch('meetingType')

  const openCreate = () => { setEditing(null); reset({ meetingType: 'OFFLINE' }); setShowForm(true) }
  const openEdit   = (m) => {
    setEditing(m)
    reset({
      ...m,
      scheduledAt: m.scheduledAt ? m.scheduledAt.substring(0, 16) : '',
    })
    setShowForm(true)
  }

  const onSubmit = async (data) => {
    setSubmitting(true)
    try {
      if (editing) {
        await meetingApi.update(editing.id, data)
        toast.success('Meeting updated')
      } else {
        await meetingApi.create(data)
        toast.success('Meeting scheduled — headmasters notified!')
      }
      setShowForm(false)
      refetch()
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to save meeting')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async () => {
    setSubmitting(true)
    try {
      await meetingApi.delete(deleting.id)
      toast.success('Meeting cancelled')
      setDeleting(null)
      refetch()
    } catch { toast.error('Failed to cancel meeting') }
    finally { setSubmitting(false) }
  }

  const statusBadge = (m) => {
    const past = m.scheduledAt && isPast(new Date(m.scheduledAt))
    if (m.status === 'CANCELLED') return <span className="badge badge-red">Cancelled</span>
    if (past || m.status === 'COMPLETED') return <span className="badge badge-gray">Completed</span>
    return <span className="badge badge-green">Upcoming</span>
  }

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Meetings</h1>
          <p className="page-subtitle">Schedule and manage headmaster meetings</p>
        </div>
        <button onClick={openCreate} className="btn-primary">
          <Plus className="w-4 h-4" /> Schedule Meeting
        </button>
      </div>

      {loading ? <ListSkeleton items={4} /> : (meetings || []).length === 0 ? (
        <EmptyState
          icon={CalendarDays}
          title="No meetings scheduled"
          description="Schedule your first meeting for headmasters"
          action={<button onClick={openCreate} className="btn-primary"><Plus className="w-4 h-4" />Schedule Meeting</button>}
        />
      ) : (
        <div className="space-y-3">
          {(meetings || []).map(m => (
            <div key={m.id} className="card-hover p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-start gap-4 flex-1 min-w-0">
                  <div className={clsx('w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0',
                    m.meetingType === 'ONLINE' ? 'bg-blue-100' : 'bg-purple-100')}>
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
                      {statusBadge(m)}
                    </div>
                    {m.agenda && <p className="text-sm text-gray-500 mb-2 line-clamp-2">{m.agenda}</p>}
                    <div className="flex flex-wrap gap-4 text-xs text-gray-400">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {m.scheduledAt && format(new Date(m.scheduledAt), 'dd MMM yyyy, hh:mm a')}
                      </span>
                      {m.venue && <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{m.venue}</span>}
                      {m.meetingLink && (
                        <a href={m.meetingLink} target="_blank" rel="noreferrer"
                          className="flex items-center gap-1 text-primary-600 hover:underline">
                          <Video className="w-3 h-3" />Join Link
                        </a>
                      )}
                      <span className="flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3 text-green-500" />
                        {m.acknowledgedCount} acknowledged
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2 flex-shrink-0">
                  <button onClick={() => openEdit(m)} className="btn-ghost btn-sm p-1.5" title="Edit">
                    <Edit2 className="w-4 h-4" />
                  </button>
                  <button onClick={() => setDeleting(m)}
                    className="btn-ghost btn-sm p-1.5 text-red-400 hover:text-red-600 hover:bg-red-50" title="Cancel">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Form Modal */}
      <Modal
        open={showForm} onClose={() => setShowForm(false)}
        title={editing ? 'Edit Meeting' : 'Schedule Meeting'}
        footer={
          <>
            <button onClick={() => setShowForm(false)} className="btn-secondary" disabled={submitting}>Cancel</button>
            <button onClick={handleSubmit(onSubmit)} className="btn-primary" disabled={submitting}>
              {submitting ? 'Saving…' : editing ? 'Update' : 'Schedule & Notify'}
            </button>
          </>
        }
      >
        <div className="space-y-4">
          <div className="form-group">
            <label className="label">Meeting Title *</label>
            <input className={`input ${errors.title ? 'input-error' : ''}`}
              placeholder="e.g. Monthly Review Meeting"
              {...register('title', { required: 'Title is required' })} />
            {errors.title && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.title.message}</p>}
          </div>
          <div className="form-group">
            <label className="label">Agenda</label>
            <textarea className="input" rows={3} placeholder="Meeting agenda and topics to discuss…"
              {...register('agenda')} />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="form-group">
              <label className="label">Date & Time *</label>
              <input type="datetime-local" className={`input ${errors.scheduledAt ? 'input-error' : ''}`}
                {...register('scheduledAt', { required: 'Date and time is required' })} />
              {errors.scheduledAt && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.scheduledAt.message}</p>}
            </div>
            <div className="form-group">
              <label className="label">Meeting Type *</label>
              <select className="input" {...register('meetingType', { required: true })}>
                <option value="OFFLINE">Offline (In-Person)</option>
                <option value="ONLINE">Online</option>
              </select>
            </div>
          </div>
          {meetingType === 'OFFLINE' ? (
            <div className="form-group">
              <label className="label">Venue</label>
              <input className="input" placeholder="e.g. Cluster Head Office, Pune"
                {...register('venue')} />
            </div>
          ) : (
            <div className="form-group">
              <label className="label">Meeting Link</label>
              <input className="input" placeholder="https://meet.google.com/..."
                {...register('meetingLink')} />
            </div>
          )}
        </div>
      </Modal>

      <ConfirmDialog
        open={!!deleting} onClose={() => setDeleting(null)}
        onConfirm={handleDelete} loading={submitting}
        title="Cancel Meeting"
        description={`Cancel "${deleting?.title}"?`}
        confirmLabel="Cancel Meeting"
      />
    </div>
  )
}
