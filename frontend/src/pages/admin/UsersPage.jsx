import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { userApi, authApi, schoolApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import ConfirmDialog from '../../components/ui/ConfirmDialog'
import EmptyState from '../../components/ui/EmptyState'
import { TableSkeleton } from '../../components/ui/Skeleton'
import { Users, Plus, ToggleLeft, ToggleRight, Trash2, AlertCircle, School } from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

// Defined OUTSIDE to prevent remounting on every render
function UserRow({ user, onAssign, onToggle, onDelete }) {
  return (
    <tr>
      <td>
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0">
            <span className="text-primary-700 text-xs font-semibold">{user.name?.[0]?.toUpperCase()}</span>
          </div>
          <span className="font-medium text-gray-900">{user.name}</span>
        </div>
      </td>
      <td className="text-gray-500">{user.email}</td>
      <td>
        <span className={clsx('badge', user.role === 'ADMIN' ? 'badge-purple' : 'badge-blue')}>{user.role}</span>
      </td>
      <td className="text-gray-500 max-w-[160px]">
        {user.school?.name
          ? <span className="truncate block">{user.school.name}</span>
          : <span className="text-gray-300">—</span>
        }
      </td>
      <td>
        <span className={clsx('badge', user.active ? 'badge-green' : 'badge-red')}>
          {user.active ? 'Active' : 'Inactive'}
        </span>
      </td>
      <td className="text-gray-400 text-xs">
        {user.createdAt ? format(new Date(user.createdAt), 'dd MMM yyyy') : '—'}
      </td>
      <td>
        {user.role !== 'ADMIN' && (
          <div className="flex items-center gap-1">
            <button onClick={() => onAssign(user)} className="btn-ghost btn-sm p-1.5" title="Assign School">
              <School className="w-4 h-4 text-blue-400" />
            </button>
            <button onClick={() => onToggle(user)} className="btn-ghost btn-sm p-1.5"
              title={user.active ? 'Deactivate' : 'Activate'}>
              {user.active
                ? <ToggleRight className="w-4 h-4 text-green-500" />
                : <ToggleLeft className="w-4 h-4 text-gray-400" />
              }
            </button>
            <button onClick={() => onDelete(user)}
              className="btn-ghost btn-sm p-1.5 text-red-400 hover:text-red-600 hover:bg-red-50" title="Delete">
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        )}
      </td>
    </tr>
  )
}

const TABLE_HEADERS = (
  <tr>
    <th>Name</th><th>Email</th><th>Role</th><th>School</th>
    <th>Status</th><th>Joined</th><th>Actions</th>
  </tr>
)

export default function UsersPage() {
  const { data: users, loading, refetch } = useApi(() => userApi.getAll())
  const { data: schools } = useApi(() => schoolApi.getAll())
  const [showForm,        setShowForm]        = useState(false)
  const [deleting,        setDeleting]        = useState(null)
  const [assigningSchool, setAssigningSchool] = useState(null)
  const [newSchoolId,     setNewSchoolId]     = useState('')
  const [submitting,      setSubmitting]      = useState(false)

  const { register, handleSubmit, reset, formState: { errors } } = useForm()

  const headmasters = (users || []).filter(u => u.role === 'HEADMASTER')
  const admins      = (users || []).filter(u => u.role === 'ADMIN')

  const onAssign = (user) => {
    setAssigningSchool(user)
    setNewSchoolId(user.school?.id?.toString() || '')
  }

  const onSubmit = async (data) => {
    setSubmitting(true)
    try {
      await authApi.registerHeadmaster(data)
      toast.success('Headmaster account created!')
      setShowForm(false)
      reset()
      refetch()
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to create user')
    } finally {
      setSubmitting(false)
    }
  }

  const toggleActive = async (user) => {
    try {
      await userApi.toggleActive(user.id)
      toast.success(`User ${user.active ? 'deactivated' : 'activated'}`)
      refetch()
    } catch (err) { toast.error(err.response?.data?.message || 'Failed to update') }
  }

  const handleDelete = async () => {
    setSubmitting(true)
    try {
      await userApi.delete(deleting.id)
      toast.success('User removed')
      setDeleting(null)
      refetch()
    } catch (err) { toast.error(err.response?.data?.message || 'Failed to remove user') }
    finally { setSubmitting(false) }
  }

  const handleAssignSchool = async () => {
    setSubmitting(true)
    try {
      const schoolId = newSchoolId ? parseInt(newSchoolId) : null
      await userApi.assignSchool(assigningSchool.id, schoolId)
      toast.success('School assigned successfully')
      setAssigningSchool(null)
      setNewSchoolId('')
      refetch()
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to assign school')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Users</h1>
          <p className="page-subtitle">Manage headmaster accounts</p>
        </div>
        <button onClick={() => { reset(); setShowForm(true) }} className="btn-primary">
          <Plus className="w-4 h-4" /> Add Headmaster
        </button>
      </div>

      {loading ? <TableSkeleton rows={5} cols={7} /> : (users || []).length === 0 ? (
        <EmptyState icon={Users} title="No users yet"
          description="Add headmaster accounts to give them portal access"
          action={<button onClick={() => setShowForm(true)} className="btn-primary"><Plus className="w-4 h-4" />Add Headmaster</button>}
        />
      ) : (
        <div className="space-y-6">
          {/* Headmasters */}
          <div>
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
              Headmasters ({headmasters.length})
            </h2>
            {headmasters.length === 0 ? (
              <div className="card p-6 text-center text-sm text-gray-400">
                No headmaster accounts yet.{' '}
                <button onClick={() => { reset(); setShowForm(true) }} className="text-primary-600 hover:underline font-medium">
                  Add one
                </button>
              </div>
            ) : (
              <div className="table-container">
                <table className="table">
                  <thead>{TABLE_HEADERS}</thead>
                  <tbody>
                    {headmasters.map(u => (
                      <UserRow key={u.id} user={u} onAssign={onAssign} onToggle={toggleActive} onDelete={setDeleting} />
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Admins */}
          {admins.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Admins ({admins.length})
              </h2>
              <div className="table-container">
                <table className="table">
                  <thead>{TABLE_HEADERS}</thead>
                  <tbody>
                    {admins.map(u => (
                      <UserRow key={u.id} user={u} onAssign={onAssign} onToggle={toggleActive} onDelete={setDeleting} />
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Create Headmaster Modal */}
      <Modal
        open={showForm} onClose={() => setShowForm(false)}
        title="Add Headmaster Account"
        footer={
          <>
            <button onClick={() => setShowForm(false)} className="btn-secondary" disabled={submitting}>Cancel</button>
            <button onClick={handleSubmit(onSubmit)} className="btn-primary" disabled={submitting}>
              {submitting ? 'Creating…' : 'Create Account'}
            </button>
          </>
        }
      >
        <div className="space-y-4">
          <div className="form-group">
            <label className="label">Full Name *</label>
            <input className={`input ${errors.name ? 'input-error' : ''}`}
              placeholder="e.g. Rajan Patil"
              {...register('name', { required: 'Name is required' })} />
            {errors.name && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.name.message}</p>}
          </div>
          <div className="form-group">
            <label className="label">Email Address *</label>
            <input type="email" className={`input ${errors.email ? 'input-error' : ''}`}
              placeholder="headmaster@school.in"
              {...register('email', { required: 'Email is required' })} />
            {errors.email && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.email.message}</p>}
          </div>
          <div className="form-group">
            <label className="label">Password *</label>
            <input type="password" className={`input ${errors.password ? 'input-error' : ''}`}
              placeholder="Min. 8 characters"
              {...register('password', { required: 'Password required', minLength: { value: 8, message: 'Min 8 characters' } })} />
            {errors.password && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.password.message}</p>}
          </div>
          <div className="form-group">
            <label className="label">Phone</label>
            <input className="input" placeholder="Mobile number" {...register('phone')} />
          </div>
          <div className="form-group">
            <label className="label">Assign School</label>
            <select className="input" {...register('schoolId')}>
              <option value="">Select a school (optional)</option>
              {(schools || []).map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
            </select>
          </div>
        </div>
      </Modal>

      {/* Assign School Modal */}
      <Modal
        open={!!assigningSchool} onClose={() => setAssigningSchool(null)}
        title={`Assign School — ${assigningSchool?.name}`}
        footer={
          <>
            <button onClick={() => setAssigningSchool(null)} className="btn-secondary" disabled={submitting}>Cancel</button>
            <button onClick={handleAssignSchool} className="btn-primary" disabled={submitting}>
              {submitting ? 'Saving…' : 'Assign School'}
            </button>
          </>
        }
      >
        <div className="form-group">
          <label className="label">School</label>
          <select className="input" value={newSchoolId} onChange={e => setNewSchoolId(e.target.value)}>
            <option value="">No school (unassign)</option>
            {(schools || []).map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
          <p className="text-xs text-gray-400 mt-1">Selecting "No school" will unassign the headmaster from their current school.</p>
        </div>
      </Modal>

      <ConfirmDialog
        open={!!deleting} onClose={() => setDeleting(null)}
        onConfirm={handleDelete} loading={submitting}
        title="Remove User"
        description={`Remove "${deleting?.name}"? They will lose access to the portal.`}
      />
    </div>
  )
}
