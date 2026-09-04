import { useState } from 'react'
import { formApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import ConfirmDialog from '../../components/ui/ConfirmDialog'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import {
  ClipboardList, Plus, Trash2, Download, Clock,
  CheckCircle2, AlertCircle, GripVertical, X, Eye, School
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
  const [showForm,          setShowForm]          = useState(false)
  const [deleting,          setDeleting]          = useState(null)
  const [submitting,        setSubmitting]        = useState(false)
  const [exporting,         setExporting]         = useState(null)
  const [viewingForm,       setViewingForm]       = useState(null)
  const [responsesList,     setResponsesList]     = useState([])
  const [loadingResponses,  setLoadingResponses]  = useState(false)

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
    if (fields.length === 0) { toast.error('Add at least one column/field'); return }
    const emptyLabels = fields.some(f => !f.label.trim())
    if (emptyLabels) { toast.error('All columns must have labels'); return }

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

  const handleViewResponses = async (form) => {
    setViewingForm(form)
    setLoadingResponses(true)
    try {
      const res = await formApi.getResponses(form.id)
      setResponsesList(res.data?.data || [])
    } catch {
      toast.error('Failed to load responses')
      setResponsesList([])
    } finally {
      setLoadingResponses(false)
    }
  }

  const parseRows = (answersJson) => {
    try {
      const raw = typeof answersJson === 'string' ? JSON.parse(answersJson) : answersJson
      if (Array.isArray(raw)) return raw
      if (raw && raw.rows && Array.isArray(raw.rows)) return raw.rows
      return [raw || {}]
    } catch {
      return [{}]
    }
  }

  const getFormFields = (form) => {
    try {
      if (!form?.fieldsJson) return []
      return typeof form.fieldsJson === 'string' ? JSON.parse(form.fieldsJson) : form.fieldsJson
    } catch {
      return []
    }
  }

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Forms (माहिती प्रपत्रे)</h1>
          <p className="page-subtitle">Define columns and collect data across all cluster schools</p>
        </div>
        <button onClick={openCreate} className="btn-primary">
          <Plus className="w-4 h-4" />Create Form
        </button>
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
                        <span>{fieldCount} column{fieldCount !== 1 ? 's' : ''} defined</span>
                        <span className="flex items-center gap-1 font-medium text-green-600">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          {f.responseCount || 0} school{f.responseCount !== 1 ? 's' : ''} submitted
                        </span>
                        {f.deadline && (
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            Due {format(new Date(f.deadline), 'dd MMM yyyy')}
                          </span>
                        )}
                        <span>Created: {f.createdAt && format(new Date(f.createdAt), 'dd MMM yyyy')}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <button
                      onClick={() => handleViewResponses(f)}
                      disabled={!f.responseCount}
                      className="btn-secondary btn-sm"
                      title={!f.responseCount ? 'No responses yet' : 'View School Submissions'}
                    >
                      <Eye className="w-3.5 h-3.5" />
                      View ({f.responseCount || 0})
                    </button>
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
      <Modal open={showForm} onClose={() => setShowForm(false)} title="Create Form (स्तंभ निश्चित करा)" size="lg"
        footer={
          <>
            <button onClick={() => setShowForm(false)} className="btn-secondary" disabled={submitting}>Cancel</button>
            <button onClick={handleCreate} className="btn-primary" disabled={submitting}>
              {submitting ? 'Creating…' : 'Create & Notify Schools'}
            </button>
          </>
        }
      >
        <div className="space-y-4">
          <div className="form-group">
            <label className="label">Form Title *</label>
            <input className="input" placeholder="e.g. Monthly Data / Equipment Requirements / Staff Details"
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

          {/* Form Columns */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <div>
                <label className="label mb-0">Form Columns (Fields) *</label>
                <p className="text-xs text-gray-400">Headmasters can fill 1 or more rows for these columns</p>
              </div>
              <button onClick={addField} className="btn-secondary btn-sm">
                <Plus className="w-3 h-3" />Add Column
              </button>
            </div>
            {fields.length === 0 ? (
              <div className="border-2 border-dashed border-gray-200 rounded-xl p-6 text-center">
                <ClipboardList className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                <p className="text-sm text-gray-400">No columns defined yet. Click "Add Column" to define your fields.</p>
              </div>
            ) : (
              <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
                {fields.map((field, idx) => (
                  <div key={field.id} className="border border-gray-200 rounded-xl p-3 bg-gray-50/50">
                    <div className="flex items-center gap-2 mb-2">
                      <GripVertical className="w-4 h-4 text-gray-300 flex-shrink-0" />
                      <input
                        className="input flex-1 text-sm py-1.5"
                        placeholder={`Column ${idx + 1} header (e.g. Item Name, Quantity, Status) *`}
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

      {/* Admin View Responses Modal (Combined School View) */}
      {viewingForm && (
        <Modal
          open={!!viewingForm}
          onClose={() => setViewingForm(null)}
          title={`Responses: ${viewingForm.title}`}
          size="xl"
          footer={
            <div className="flex items-center justify-between w-full">
              <span className="text-xs text-gray-500">
                Total {responsesList.length} school{responsesList.length !== 1 ? 's' : ''} submitted
              </span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleExport(viewingForm)}
                  className="btn-secondary btn-sm flex items-center gap-1"
                >
                  <Download className="w-3.5 h-3.5" /> Export to Excel
                </button>
                <button onClick={() => setViewingForm(null)} className="btn-secondary btn-sm">
                  Close
                </button>
              </div>
            </div>
          }
        >
          <div className="space-y-6">
            {loadingResponses ? (
              <div className="py-12 flex justify-center">
                <div className="w-8 h-8 border-2 border-primary-600 border-t-transparent rounded-full animate-spin" />
              </div>
            ) : responsesList.length === 0 ? (
              <div className="text-center py-10 text-gray-400">
                No school responses submitted yet.
              </div>
            ) : (
              <div className="space-y-5">
                {responsesList.map((resp, sIdx) => {
                  const rowsData = parseRows(resp.answersJson)
                  const formFields = getFormFields(viewingForm)
                  return (
                    <div key={resp.id || sIdx} className="border border-gray-200 rounded-2xl overflow-hidden shadow-sm bg-white">
                      {/* Combined School Info Banner - Shown ONCE per school */}
                      <div className="bg-gradient-to-r from-primary-50 to-blue-50/50 p-4 border-b border-gray-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                        <div className="flex items-center gap-2.5">
                          <div className="w-8 h-8 rounded-lg bg-primary-600 text-white flex items-center justify-center flex-shrink-0">
                            <School className="w-4 h-4" />
                          </div>
                          <div>
                            <h4 className="font-bold text-gray-900 text-sm">{resp.schoolName}</h4>
                            <div className="text-xs text-gray-500 flex items-center gap-2 mt-0.5">
                              {resp.udiseCode && <span className="font-mono">UDISE: {resp.udiseCode}</span>}
                              {resp.village && <span>• {resp.village}</span>}
                            </div>
                          </div>
                        </div>

                        <div className="text-right sm:text-right text-xs text-gray-500">
                          <div>
                            Submitted by: <strong className="text-gray-700">{resp.submittedByName || 'Headmaster'}</strong>
                          </div>
                          <div className="flex items-center gap-2 mt-0.5 justify-end">
                            <span>{resp.submittedAt && format(new Date(resp.submittedAt), 'dd/MM/yyyy HH:mm')}</span>
                            <span className="badge badge-blue text-[10px]">{rowsData.length} Rows</span>
                          </div>
                        </div>
                      </div>

                      {/* Inner Data Table for this school */}
                      <div className="overflow-x-auto">
                        <table className="w-full text-left text-xs border-collapse">
                          <thead className="bg-gray-50 text-gray-600 border-b border-gray-200">
                            <tr>
                              <th className="py-2 px-3 w-10 text-center font-semibold">#</th>
                              {formFields.map(f => (
                                <th key={f.id} className="py-2 px-3 font-semibold">
                                  {f.label}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-gray-100">
                            {rowsData.map((rowItem, rIdx) => (
                              <tr key={rIdx} className="hover:bg-gray-50/50">
                                <td className="py-2 px-3 text-center font-bold text-gray-400 bg-gray-50/30">
                                  {rIdx + 1}
                                </td>
                                {formFields.map(f => (
                                  <td key={f.id} className="py-2 px-3 text-gray-800">
                                    {rowItem[f.id] ? String(rowItem[f.id]) : '—'}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </Modal>
      )}

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={!!deleting}
        onClose={() => setDeleting(null)}
        onConfirm={handleDelete}
        title="Delete Form"
        message={`Are you sure you want to deactivate "${deleting?.title}"? Existing responses will be preserved.`}
        confirmText="Deactivate"
        danger
      />
    </div>
  )
}
