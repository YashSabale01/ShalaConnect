import { useState } from 'react'
import { formApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import {
  ClipboardList, CheckCircle2, Clock, AlertCircle, Send
} from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function HeadmasterFormsPage() {
  const { data: forms, loading, refetch } = useApi(() => formApi.getAll())
  const [activeForm,  setActiveForm]  = useState(null)
  const [answers,     setAnswers]     = useState({})
  const [submitting,  setSubmitting]  = useState(false)
  const [errors,      setErrors]      = useState({})

  const openForm = async (form) => {
    // Fetch full form details (with fields)
    try {
      const res = await formApi.getById(form.id)
      setActiveForm(res.data.data)
      setAnswers({})
      setErrors({})
    } catch { toast.error('Failed to load form') }
  }

  const getFields = () => {
    if (!activeForm?.fieldsJson) return []
    if (Array.isArray(activeForm.fieldsJson)) return activeForm.fieldsJson
    try {
      return typeof activeForm.fieldsJson === 'string' ? JSON.parse(activeForm.fieldsJson) : []
    } catch { return [] }
  }

  const validate = () => {
    const fields = getFields()
    const errs = {}
    fields.forEach(f => {
      if (f.required && !answers[f.id]?.toString().trim()) {
        errs[f.id] = 'This field is required'
      }
    })
    setErrors(errs)
    return Object.keys(errs).length === 0
  }

  const handleSubmit = async () => {
    if (!validate()) { toast.error('Please fill all required fields'); return }
    setSubmitting(true)
    try {
      await formApi.respond(activeForm.id, { answersJson: JSON.stringify(answers) })
      toast.success('Form submitted successfully!')
      setActiveForm(null)
      refetch()
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to submit form')
    } finally {
      setSubmitting(false)
    }
  }

  const renderField = (field) => {
    const value = answers[field.id] || ''
    const error = errors[field.id]
    const baseClass = `input${error ? ' input-error' : ''}`
    const onChange = (v) => {
      setAnswers(a => ({ ...a, [field.id]: v }))
      if (errors[field.id]) setErrors(e => ({ ...e, [field.id]: '' }))
    }

    switch (field.type) {
      case 'textarea':
        return <textarea className={baseClass} rows={3} value={value}
          onChange={e => onChange(e.target.value)} placeholder={`Enter ${field.label}…`} />
      case 'number':
        return <input type="number" className={baseClass} value={value}
          onChange={e => onChange(e.target.value)} placeholder="0" />
      case 'date':
        return <input type="date" className={baseClass} value={value}
          onChange={e => onChange(e.target.value)} />
      case 'select':
        return (
          <select className={baseClass} value={value} onChange={e => onChange(e.target.value)}>
            <option value="">Select an option…</option>
            {(field.options || []).map(opt => <option key={opt} value={opt}>{opt}</option>)}
          </select>
        )
      case 'radio':
        return (
          <div className="space-y-2 mt-1">
            {(field.options || []).map(opt => (
              <label key={opt} className="flex items-center gap-2.5 cursor-pointer">
                <input type="radio" name={field.id} value={opt}
                  checked={value === opt} onChange={() => onChange(opt)}
                  className="text-primary-600" />
                <span className="text-sm text-gray-700">{opt}</span>
              </label>
            ))}
          </div>
        )
      default:
        return <input type="text" className={baseClass} value={value}
          onChange={e => onChange(e.target.value)} placeholder={`Enter ${field.label}…`} />
    }
  }

  const pending  = (forms || []).filter(f => !f.hasResponded)
  const completed = (forms || []).filter(f => f.hasResponded)

  if (loading) return <ListSkeleton items={4} />

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Forms</h1>
          <p className="page-subtitle">
            {pending.length > 0
              ? `${pending.length} pending form${pending.length > 1 ? 's' : ''} to fill`
              : 'All forms completed'}
          </p>
        </div>
      </div>

      {(forms || []).length === 0 ? (
        <EmptyState
          icon={ClipboardList}
          title="No forms assigned"
          description="Forms assigned by the admin will appear here"
        />
      ) : (
        <div className="space-y-6">
          {pending.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Pending ({pending.length})
              </h2>
              <div className="space-y-3">
                {pending.map(f => (
                  <div key={f.id} className="card-hover p-5 border-l-4 border-l-amber-400">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0">
                        <ClipboardList className="w-5 h-5 text-amber-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-900">{f.title}</h3>
                        {f.description && <p className="text-sm text-gray-500 mt-0.5 line-clamp-1">{f.description}</p>}
                        <div className="flex gap-4 text-xs text-gray-400 mt-1">
                          <span>{f.createdAt && format(new Date(f.createdAt), 'dd MMM yyyy')}</span>
                          {f.deadline && (
                            <span className="flex items-center gap-1 text-red-500">
                              <Clock className="w-3 h-3" />
                              Due {format(new Date(f.deadline), 'dd MMM yyyy')}
                            </span>
                          )}
                        </div>
                      </div>
                      <button onClick={() => openForm(f)} className="btn-primary btn-sm flex-shrink-0">
                        Fill Form
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {completed.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
                Completed ({completed.length})
              </h2>
              <div className="space-y-3 opacity-70">
                {completed.map(f => (
                  <div key={f.id} className="card p-5 border-l-4 border-l-green-400">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-xl bg-green-100 flex items-center justify-center flex-shrink-0">
                        <CheckCircle2 className="w-5 h-5 text-green-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-700">{f.title}</h3>
                        {f.description && <p className="text-sm text-gray-400 mt-0.5 line-clamp-1">{f.description}</p>}
                      </div>
                      <span className="badge badge-green flex-shrink-0">Submitted</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Dynamic Form Modal */}
      {activeForm && (
        <Modal
          open={!!activeForm}
          onClose={() => setActiveForm(null)}
          title={activeForm.title}
          size="lg"
          footer={
            <>
              <button onClick={() => setActiveForm(null)} className="btn-secondary" disabled={submitting}>Cancel</button>
              <button onClick={handleSubmit} className="btn-primary" disabled={submitting}>
                {submitting ? 'Submitting…' : <><Send className="w-4 h-4" />Submit Response</>}
              </button>
            </>
          }
        >
          <div className="space-y-5">
            {activeForm.description && (
              <div className="p-3 bg-blue-50 border border-blue-100 rounded-xl text-sm text-blue-700">
                {activeForm.description}
              </div>
            )}
            {getFields().map((field, idx) => (
              <div key={field.id} className="form-group">
                <label className="label">
                  {idx + 1}. {field.label}
                  {field.required && <span className="text-red-500 ml-0.5">*</span>}
                </label>
                {renderField(field)}
                {errors[field.id] && (
                  <p className="error-message">
                    <AlertCircle className="w-3 h-3" />{errors[field.id]}
                  </p>
                )}
              </div>
            ))}
          </div>
        </Modal>
      )}
    </div>
  )
}
