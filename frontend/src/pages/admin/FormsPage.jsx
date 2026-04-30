import { useState } from 'react'
import { formApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import ConfirmDialog from '../../components/ui/ConfirmDialog'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import {
  ClipboardList, Plus, Trash2, Download, Clock,
  CheckCircle2, AlertCircle, GripVertical, X
} from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

const FIELD_TYPES = [
  { value: 'text',     label: 'Short Text' },
  { value: 'textarea', label: 'Long Text' },
  { value: 'number',   label: 'Number' },
  { value: 'date',     label: 'Date' },
  { value: 'select',   label: 'Dropdown' },
  { value: 'radio',    label: 'Radio (Single Choice)' },
]

export default function FormsPage() {
  const { data: forms, loading, refetch } = useApi(() => formApi.getAll())
  const [showForm,   setShowForm]   = useState(false)
  const [deleting,   setDeleting]   = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [exporting,  setExporting]  = useState(null)

  // Form builder state
  const [title, setTitle]           = useState('')
  const [description, setDesc]      = useState('')
  const [deadline, setDeadline]     = useState('')
  const [fields, setFields]         = useState([])

  const addField = () => {
    setFields(f => [...f, {
      id: `field_${Date.now()}`,
      label: '',
      type: 'text',
      required: false,
      options: '',
    }])
  }

  const updateField = (idx, key, val) => {
    setFields(f => f.map((field, i) => i === idx ? { ...field, [key]: val } : field))
  }

  const removeField = (idx) => setFields(f => f.filter((_, i) => i !== idx))

  const openCreate = () => {
    setTitle(''); setDesc(''); setDeadline(''); setFields([])
    setShowForm(true)
  }

  const handleCreate = async () => {
    if (!title.trim()) { toast.error('Form title is required'); return }
    if (fields.length === 0) { toast.error('Add at least one field'); return }
    const emptyLabels = fields.some(f => !f.label.trim())
    if (emptyLabels) { toast.error('All fields must have labels'); return }

    setSubmitting(true)
    try {
      const processedFields = fields.map(f => ({
        id: f.id, label: f.label, type: f.type, required: f.required,
        options: f.options ? f.options.split(',').map(o => o.trim()).filter(Boolean) : [],
      }))
      await formApi.create({
        title, description, deadline: deadline || null,
        fieldsJson: JSON.stringify(processedFields),
      })
      toast.success('Form created and headmasters notified!')
      setShowForm(false)
      refetch()
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to create form')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async () => {
    setSubmitting(true)
    try {
      await formApi.delete(deleting.id)
      toast.success('Form deleted')
      setDeleting(null)
      refetch()
    } catch { toast.error('Failed to delete form') }
    finally { setSubmitting(false) }
  }

  const handleExport = async (form) => {
    setExporting(form.id)
    try {
      const res = await formApi.export(form.id)
      const url  = URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.download = `${form.title}-responses.xlsx`
      link.click()
      URL.revokeObjectURL(url)
      toast.success('Excel file downloaded!')
    } catch { toast.error('Export failed') }
    finally { setExporting(null) }
  }

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Forms</h1>
          <p className="page-subtitle">Create data-collection forms for headmasters</p>
        </div>
        <button onClick={openCreate} className="btn-primary"><Plus className="w-4 h-4" />Create Form</button>
      </div>

      {loading ? <ListSkeleton items={3} /> : (forms || []).length === 0 ? (
        <EmptyState
          icon={ClipboardList} title="No forms yet"
          description="Create forms to collect data from all headmasters"
          action={<button onClick={openCreate} className="btn-primary"><Plus className="w-4 h-4" />Create Form</button>}
        />
      ) : (
        <div className="space-y-4">
          {(forms || []).map(f => {
            let fieldCount = 0
            try { fieldCount = JSON.parse(f.fieldsJson || '[]').length } catch {}
            return (
              <div key={f.id} className="card p-5">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-4 flex-1 min-w-0">
                    <div className="w-10 h-10 rounded-xl bg-green-100 flex items-center justify-center flex-shrink-0">
                      <ClipboardList className="w-5 h-5 text-green-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 mb-1">{f.title}</h3>
                      {f.description && <p className="text-sm text-gray-500 mb-2 line-clamp-1">{f.description}</p>}
                      <div className="flex flex-wrap gap-4 text-xs text-gray-400">
                        <span>{fieldCount} field{fieldCount !== 1 ? 's' : ''}</span>
                        <span className="flex items-center gap-1">
                          <CheckCircle2 className="w-3 h-3 text-green-500" />
                          {f.responseCount || 0} response{f.responseCount !== 1 ? 's' : ''}
                        </span>
                        {f.deadline && (
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            Due {format(new Date(f.deadline), 'dd MMM yyyy')}
                          </span>
                        )}
                        <span>{f.createdAt && format(new Date(f.createdAt), 'dd MMM yyyy')}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <button
                      onClick={() => handleExport(f)}
                      disabled={exporting === f.id || !f.responseCount}
                      className="btn-secondary btn-sm"
                      title={!f.responseCount ? 'No responses yet' : 'Export to Excel'}
                    >
                      <Download className="w-3.5 h-3.5" />
                      {exporting === f.id ? 'Exporting…' : 'Export'}
                    </button>
                    <button onClick={() => setDeleting(f)}
                      className="btn-ghost btn-sm p-1.5 text-red-400 hover:text-red-600 hover:bg-red-50">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Form Builder Modal */}
      <Modal open={showForm} onClose={() => setShowForm(false)} title="Create Form" size="lg"
        footer={
          <>
            <button onClick={() => setShowForm(false)} className="btn-secondary" disabled={submitting}>Cancel</button>
            <button onClick={handleCreate} className="btn-primary" disabled={submitting}>
              {submitting ? 'Creating…' : 'Create & Notify'}
            </button>
          </>
        }
      >
        <div className="space-y-4">
          <div className="form-group">
            <label className="label">Form Title *</label>
            <input className="input" placeholder="e.g. Monthly School Data Collection"
              value={title} onChange={e => setTitle(e.target.value)} />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="form-group">
              <label className="label">Description</label>
              <input className="input" placeholder="Instructions for headmasters"
                value={description} onChange={e => setDesc(e.target.value)} />
            </div>
            <div className="form-group">
              <label className="label">Deadline (Optional)</label>
              <input type="datetime-local" className="input"
                value={deadline} onChange={e => setDeadline(e.target.value)} />
            </div>
          </div>

          {/* Fields */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="label mb-0">Form Fields *</label>
              <button onClick={addField} className="btn-secondary btn-sm">
                <Plus className="w-3 h-3" />Add Field
              </button>
            </div>
            {fields.length === 0 ? (
              <div className="border-2 border-dashed border-gray-200 rounded-xl p-6 text-center">
                <ClipboardList className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                <p className="text-sm text-gray-400">No fields yet. Click "Add Field" to start building your form.</p>
              </div>
            ) : (
              <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
                {fields.map((field, idx) => (
                  <div key={field.id} className="border border-gray-200 rounded-xl p-3 bg-gray-50/50">
                    <div className="flex items-center gap-2 mb-2">
                      <GripVertical className="w-4 h-4 text-gray-300 flex-shrink-0" />
                      <input
                        className="input flex-1 text-sm py-1.5"
                        placeholder={`Field ${idx + 1} label *`}
                        value={field.label}
                        onChange={e => updateField(idx, 'label', e.target.value)}
                      />
                      <select
                        className="input w-36 text-sm py-1.5"
                        value={field.type}
                        onChange={e => updateField(idx, 'type', e.target.value)}
                      >
                        {FIELD_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
                      </select>
                      <button onClick={() => removeField(idx)} className="p-1 rounded text-gray-400 hover:text-red-500 hover:bg-red-50">
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                    <div className="flex items-center gap-4 ml-6">
                      <label className="flex items-center gap-1.5 text-xs text-gray-600 cursor-pointer">
                        <input type="checkbox" className="rounded"
                          checked={field.required}
                          onChange={e => updateField(idx, 'required', e.target.checked)} />
                        Required
                      </label>
                      {(field.type === 'select' || field.type === 'radio') && (
                        <input
                          className="input flex-1 text-xs py-1"
                          placeholder="Options (comma-separated): Option 1, Option 2"
                          value={field.options}
                          onChange={e => updateField(idx, 'options', e.target.value)}
                        />
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </Modal>

      <ConfirmDialog
        open={!!deleting} onClose={() => setDeleting(null)}
        onConfirm={handleDelete} loading={submitting}
        title="Delete Form" description={`Delete "${deleting?.title}" and all its responses?`}
      />
    </div>
  )
}
