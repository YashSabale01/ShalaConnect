import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { schoolApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import ConfirmDialog from '../../components/ui/ConfirmDialog'
import EmptyState from '../../components/ui/EmptyState'
import { TableSkeleton } from '../../components/ui/Skeleton'
import {
  Building2, Plus, Search, Edit2, Trash2,
  MapPin, Phone, Users, Eye, AlertCircle
} from 'lucide-react'
import toast from 'react-hot-toast'
import clsx from 'clsx'

export default function SchoolsPage() {
  const { data: schools, loading, refetch } = useApi(() => schoolApi.getAll())
  const [search,      setSearch]      = useState('')
  const [showForm,    setShowForm]    = useState(false)
  const [editing,     setEditing]     = useState(null)
  const [deleting,    setDeleting]    = useState(null)
  const [submitting,  setSubmitting]  = useState(false)

  const { register, handleSubmit, reset, formState: { errors } } = useForm()

  const filtered = (schools || []).filter(s =>
    s.name.toLowerCase().includes(search.toLowerCase()) ||
    s.village?.toLowerCase().includes(search.toLowerCase()) ||
    s.udiseCode?.includes(search)
  )

  const openCreate = () => { setEditing(null); reset({}); setShowForm(true) }
  const openEdit   = (s)  => { setEditing(s); reset(s); setShowForm(true) }

  const onSubmit = async (data) => {
    setSubmitting(true)
    try {
      if (editing) {
        await schoolApi.update(editing.id, data)
        toast.success('School updated successfully')
      } else {
        await schoolApi.create(data)
        toast.success('School added successfully')
      }
      setShowForm(false)
      refetch()
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to save school'
      toast.error(msg)
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async () => {
    setSubmitting(true)
    try {
      await schoolApi.delete(deleting.id)
      toast.success('School removed')
      setDeleting(null)
      refetch()
    } catch {
      toast.error('Failed to delete school')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Schools</h1>
          <p className="page-subtitle">Manage all schools in your cluster</p>
        </div>
        <button onClick={openCreate} className="btn-primary">
          <Plus className="w-4 h-4" /> Add School
        </button>
      </div>

      {/* Search */}
      <div className="relative mb-5 max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          placeholder="Search schools…"
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="input pl-9"
        />
      </div>

      {loading ? (
        <TableSkeleton rows={5} cols={5} />
      ) : filtered.length === 0 ? (
        <EmptyState
          icon={Building2}
          title={search ? 'No schools match your search' : 'No schools yet'}
          description={search ? 'Try a different search term' : 'Add your first school to get started'}
          action={!search && <button onClick={openCreate} className="btn-primary"><Plus className="w-4 h-4" />Add School</button>}
        />
      ) : (
        <>
          {/* Cards grid for mobile, table for desktop */}
          <div className="hidden md:block table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>School Name</th>
                  <th>UDISE Code</th>
                  <th>Location</th>
                  <th>Students / Teachers</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(school => (
                  <tr key={school.id}>
                    <td>
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                          <Building2 className="w-4 h-4 text-blue-600" />
                        </div>
                        <div>
                          <div className="font-medium text-gray-900">{school.name}</div>
                          {school.topperName && (
                            <div className="text-xs text-gray-400">🏆 {school.topperName} — {school.topperPercentage}%</div>
                          )}
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="font-mono text-xs bg-gray-100 px-2 py-0.5 rounded">{school.udiseCode}</span>
                    </td>
                    <td>
                      <div className="flex items-center gap-1 text-gray-600">
                        <MapPin className="w-3 h-3 text-gray-400" />
                        <span>{[school.village, school.taluka].filter(Boolean).join(', ') || '—'}</span>
                      </div>
                    </td>
                    <td>
                      <div className="flex items-center gap-1 text-gray-600">
                        <Users className="w-3 h-3 text-gray-400" />
                        <span>{school.totalStudents ?? '—'} / {school.totalTeachers ?? '—'}</span>
                      </div>
                    </td>
                    <td>
                      <div className="flex items-center gap-2">
                        <Link to={`/admin/schools/${school.id}`} className="btn-ghost btn-sm p-1.5" title="View">
                          <Eye className="w-4 h-4" />
                        </Link>
                        <button onClick={() => openEdit(school)} className="btn-ghost btn-sm p-1.5" title="Edit">
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button onClick={() => setDeleting(school)} className="btn-ghost btn-sm p-1.5 text-red-400 hover:text-red-600 hover:bg-red-50" title="Delete">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Mobile cards */}
          <div className="md:hidden space-y-3">
            {filtered.map(school => (
              <div key={school.id} className="card p-4">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h3 className="font-semibold text-gray-900">{school.name}</h3>
                    <span className="font-mono text-xs bg-gray-100 px-1.5 py-0.5 rounded text-gray-500">{school.udiseCode}</span>
                  </div>
                  <div className="flex gap-1">
                    <Link to={`/admin/schools/${school.id}`} className="btn-ghost btn-sm p-1.5"><Eye className="w-4 h-4" /></Link>
                    <button onClick={() => openEdit(school)} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-4 h-4" /></button>
                    <button onClick={() => setDeleting(school)} className="btn-ghost btn-sm p-1.5 text-red-400"><Trash2 className="w-4 h-4" /></button>
                  </div>
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{school.village || '—'}</span>
                  <span className="flex items-center gap-1"><Users className="w-3 h-3" />{school.totalStudents ?? 0}</span>
                </div>
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-400 mt-3">{filtered.length} school{filtered.length !== 1 ? 's' : ''} found</p>
        </>
      )}

      {/* Create/Edit Modal */}
      <Modal
        open={showForm}
        onClose={() => setShowForm(false)}
        title={editing ? 'Edit School' : 'Add New School'}
        size="lg"
        footer={
          <>
            <button onClick={() => setShowForm(false)} className="btn-secondary" disabled={submitting}>Cancel</button>
            <button onClick={handleSubmit(onSubmit)} className="btn-primary" disabled={submitting}>
              {submitting ? 'Saving…' : editing ? 'Save Changes' : 'Add School'}
            </button>
          </>
        }
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="sm:col-span-2 form-group">
            <label className="label">School Name *</label>
            <input className={`input ${errors.name ? 'input-error' : ''}`}
              placeholder="e.g. Zilla Parishad Primary School"
              {...register('name', { required: 'Name is required' })} />
            {errors.name && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.name.message}</p>}
          </div>
          <div className="form-group">
            <label className="label">UDISE Code *</label>
            <input className={`input ${errors.udiseCode ? 'input-error' : ''}`}
              placeholder="e.g. 27110100101"
              {...register('udiseCode', { required: 'UDISE code is required' })}
              disabled={!!editing} />
            {errors.udiseCode && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.udiseCode.message}</p>}
          </div>
          <div className="form-group">
            <label className="label">Phone</label>
            <input className="input" placeholder="School phone" {...register('phone')} />
          </div>
          <div className="form-group">
            <label className="label">Village / Area</label>
            <input className="input" placeholder="Village name" {...register('village')} />
          </div>
          <div className="form-group">
            <label className="label">Taluka</label>
            <input className="input" placeholder="Taluka" {...register('taluka')} />
          </div>
          <div className="form-group">
            <label className="label">District</label>
            <input className="input" placeholder="District" {...register('district')} />
          </div>
          <div className="form-group">
            <label className="label">Total Students</label>
            <input type="number" min="0" className="input" placeholder="0" {...register('totalStudents', { valueAsNumber: true })} />
          </div>
          <div className="form-group">
            <label className="label">Total Teachers</label>
            <input type="number" min="0" className="input" placeholder="0" {...register('totalTeachers', { valueAsNumber: true })} />
          </div>
          <div className="sm:col-span-2">
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Topper Info (Optional)</p>
            <div className="grid grid-cols-3 gap-3">
              <div className="form-group">
                <label className="label">Name</label>
                <input className="input" placeholder="Student name" {...register('topperName')} />
              </div>
              <div className="form-group">
                <label className="label">Class</label>
                <input className="input" placeholder="e.g. 10th" {...register('topperClass')} />
              </div>
              <div className="form-group">
                <label className="label">Percentage</label>
                <input type="number" min="0" max="100" className="input" placeholder="95.5"
                  {...register('topperPercentage', { valueAsNumber: true })} />
              </div>
            </div>
          </div>
        </div>
      </Modal>

      <ConfirmDialog
        open={!!deleting}
        onClose={() => setDeleting(null)}
        onConfirm={handleDelete}
        loading={submitting}
        title="Delete School"
        description={`Are you sure you want to remove "${deleting?.name}"? This cannot be undone.`}
      />
    </div>
  )
}
