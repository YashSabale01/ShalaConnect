import { useState } from 'react'
import { formApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import {
  ClipboardList, CheckCircle2, Clock, AlertCircle, Send,
  Plus, Trash2, Copy, Layers, Eye
} from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function HeadmasterFormsPage() {
  const { data: forms, loading, refetch } = useApi(() => formApi.getAll())
  const [activeForm,     setActiveForm]     = useState(null)
  const [viewingForm,    setViewingForm]    = useState(null)
  const [viewingData,    setViewingData]    = useState(null)
  const [rows,           setRows]           = useState([{}])
  const [submitting,     setSubmitting]     = useState(false)
  const [errors,         setErrors]         = useState({})

  const openForm = async (form) => {
    try {
      const res = await formApi.getById(form.id)
      setActiveForm(res.data.data)
      setRows([{}])
      setErrors({})
    } catch {
      toast.error('Failed to load form')
    }
  }

  const openViewResponse = async (form) => {
    try {
      const res = await formApi.getById(form.id)
      const data = res.data.data
      setViewingForm(data)

      // Parse response data
      let parsed = []
      try {
        const raw = data.myResponse?.answersJson || data.answersJson
        if (raw) {
          const json = typeof raw === 'string' ? JSON.parse(raw) : raw
          if (Array.isArray(json)) {
            parsed = json
          } else if (json.rows && Array.isArray(json.rows)) {
            parsed = json.rows
          } else {
            parsed = [json]
          }
        }
      } catch (e) {
        parsed = []
      }
      setViewingData(parsed)
    } catch {
      toast.error('Failed to load response')
    }
  }

  const getFields = (formObj = activeForm) => {
    if (!formObj?.fieldsJson) return []
    if (Array.isArray(formObj.fieldsJson)) return formObj.fieldsJson
    try {
      return typeof formObj.fieldsJson === 'string' ? JSON.parse(formObj.fieldsJson) : []
    } catch {
      return []
    }
  }

  const addRow = () => {
    setRows(r => [...r, {}])
  }

  const duplicateRow = (index) => {
    setRows(r => {
      const copy = [...r]
      copy.splice(index + 1, 0, { ...r[index] })
      return copy
    })
    toast.success(`Row #${index + 1} duplicated`)
  }

  const removeRow = (index) => {
    if (rows.length <= 1) return
    setRows(r => r.filter((_, i) => i !== index))
    // Clear errors for removed row
    setErrors(prev => {
      const updated = { ...prev }
      delete updated[index]
      return updated
    })
  }

  const updateRowField = (rowIndex, fieldId, value) => {
    setRows(r => {
      const copy = [...r]
      copy[rowIndex] = { ...copy[rowIndex], [fieldId]: value }
      return copy
    })
    if (errors[rowIndex]?.[fieldId]) {
      setErrors(prev => ({
        ...prev,
        [rowIndex]: { ...prev[rowIndex], [fieldId]: '' }
      }))
    }
  }

  const validate = () => {
    const fields = getFields()
    const errs = {}
    let hasError = false

    rows.forEach((row, rIdx) => {
      const rowErrs = {}
      fields.forEach(f => {
        if (f.required && !row[f.id]?.toString().trim()) {
          rowErrs[f.id] = 'Required'
          hasError = true
        }
      })
      if (Object.keys(rowErrs).length > 0) {
        errs[rIdx] = rowErrs
      }
    })

    setErrors(errs)
    return !hasError
  }

  const handleSubmit = async () => {
    if (!validate()) {
      toast.error('Please fill all required fields in each row')
      return
    }

    setSubmitting(true)
    try {
      const payload = rows.length > 1 ? { isMultiRow: true, rows } : rows[0]
      await formApi.respond(activeForm.id, { answersJson: JSON.stringify(payload) })
      toast.success(rows.length > 1
        ? `Form submitted successfully with ${rows.length} rows!`
        : 'Form submitted successfully!')
      setActiveForm(null)
      refetch()
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to submit form')
    } finally {
      setSubmitting(false)
    }
  }

  const renderField = (field, rIdx) => {
    const value = rows[rIdx]?.[field.id] || ''
    const error = errors[rIdx]?.[field.id]
    const baseClass = `input text-sm py-2${error ? ' input-error' : ''}`

    switch (field.type) {
      case 'textarea':
        return (
          <textarea
            className={baseClass}
            rows={2}
            value={value}
            onChange={e => updateRowField(rIdx, field.id, e.target.value)}
            placeholder={`Enter ${field.label}…`}
          />
        )
      case 'number':
        return (
          <input
            type="number"
            className={baseClass}
            value={value}
            onChange={e => updateRowField(rIdx, field.id, e.target.value)}
            placeholder="0"
          />
        )
      case 'date':
        return (
          <input
            type="date"
            className={baseClass}
            value={value}
            onChange={e => updateRowField(rIdx, field.id, e.target.value)}
          />
        )
      case 'select':
        return (
          <select
            className={baseClass}
            value={value}
            onChange={e => updateRowField(rIdx, field.id, e.target.value)}
          >
            <option value="">Select an option…</option>
            {(field.options || []).map(opt => (
              <option key={opt} value={opt}>{opt}</option>
            ))}
          </select>
        )
      case 'radio':
        return (
          <div className="flex flex-wrap gap-4 mt-1">
            {(field.options || []).map(opt => (
              <label key={opt} className="flex items-center gap-2 cursor-pointer text-sm">
                <input
                  type="radio"
                  name={`${field.id}_${rIdx}`}
                  value={opt}
                  checked={value === opt}
                  onChange={() => updateRowField(rIdx, field.id, opt)}
                  className="text-primary-600"
                />
                <span className="text-gray-700">{opt}</span>
              </label>
            ))}
          </div>
        )
      default:
        return (
          <input
            type="text"
            className={baseClass}
            value={value}
            onChange={e => updateRowField(rIdx, field.id, e.target.value)}
            placeholder={`Enter ${field.label}…`}
          />
        )
    }
  }

  const pending   = (forms || []).filter(f => !f.hasResponded)
  const completed = (forms || []).filter(f => f.hasResponded)

  if (loading) return <ListSkeleton items={4} />

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Forms (माहिती प्रपत्रे)</h1>
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
          description="Forms assigned by the cluster administrator will appear here"
        />
      ) : (
        <div className="space-y-6">
          {pending.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Pending Forms ({pending.length})
              </h2>
              <div className="space-y-3">
                {pending.map(f => (
                  <div key={f.id} className="card p-5 hover:border-primary-200 transition-colors">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-4 flex-1 min-w-0">
                        <div className="w-10 h-10 rounded-xl bg-primary-100 flex items-center justify-center flex-shrink-0">
                          <ClipboardList className="w-5 h-5 text-primary-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="font-semibold text-gray-900">{f.title}</h3>
                          {f.description && (
                            <p className="text-sm text-gray-500 mt-0.5 line-clamp-1">{f.description}</p>
                          )}
                          <div className="flex gap-4 text-xs text-gray-400 mt-2">
                            <span>Assigned: {f.createdAt && format(new Date(f.createdAt), 'dd MMM yyyy')}</span>
                            {f.deadline && (
                              <span className="flex items-center gap-1 text-red-500 font-medium">
                                <Clock className="w-3 h-3" />
                                Due: {format(new Date(f.deadline), 'dd MMM yyyy')}
                              </span>
                            )}
                          </div>
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
              <div className="space-y-3">
                {completed.map(f => (
                  <div key={f.id} className="card p-5 border-l-4 border-l-green-500 flex items-center justify-between gap-4">
                    <div className="flex items-center gap-4 flex-1 min-w-0">
                      <div className="w-10 h-10 rounded-xl bg-green-100 flex items-center justify-center flex-shrink-0">
                        <CheckCircle2 className="w-5 h-5 text-green-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-800">{f.title}</h3>
                        {f.description && (
                          <p className="text-sm text-gray-400 mt-0.5 line-clamp-1">{f.description}</p>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <span className="badge badge-green">Submitted</span>
                      <button
                        onClick={() => openViewResponse(f)}
                        className="btn-secondary btn-sm flex items-center gap-1"
                      >
                        <Eye className="w-3.5 h-3.5" /> View
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Multi-Row Form Modal */}
      {activeForm && (
        <Modal
          open={!!activeForm}
          onClose={() => setActiveForm(null)}
          title={activeForm.title}
          size="xl"
          footer={
            <div className="flex items-center justify-between w-full">
              <div className="text-xs text-gray-500 flex items-center gap-2">
                <span className="font-medium text-gray-700">
                  Total Rows / Entries: {rows.length}
                </span>
                {rows.length > 1 && (
                  <span className="badge badge-blue text-[10px]">Multi-Row Mode</span>
                )}
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setActiveForm(null)}
                  className="btn-secondary"
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button
                  onClick={handleSubmit}
                  className="btn-primary"
                  disabled={submitting}
                >
                  {submitting ? 'Submitting…' : (
                    <>
                      <Send className="w-4 h-4" />
                      Submit {rows.length > 1 ? `All ${rows.length} Entries` : 'Response'}
                    </>
                  )}
                </button>
              </div>
            </div>
          }
        >
          <div className="space-y-6">
            {/* Form Info Banner */}
            {activeForm.description && (
              <div className="p-3.5 bg-blue-50 border border-blue-100 rounded-xl text-sm text-blue-800 leading-relaxed">
                {activeForm.description}
              </div>
            )}

            {/* Helper Notice for Multiple Entries */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-amber-600 flex-shrink-0" />
                <span>
                  <strong>Need to submit multiple records (e.g. 4 Teachers, multiple students)?</strong>
                  <br />Click <strong>"+ Add Another Row"</strong> below to add rows for each person.
                </span>
              </div>
              <button
                type="button"
                onClick={addRow}
                className="btn-secondary btn-xs bg-white text-amber-800 border-amber-300 hover:bg-amber-100 flex items-center gap-1.5 self-start sm:self-auto flex-shrink-0"
              >
                <Plus className="w-3.5 h-3.5" /> + Add Another Row
              </button>
            </div>

            {/* Rows List */}
            <div className="space-y-5">
              {rows.map((row, rIdx) => (
                <div
                  key={rIdx}
                  className={clsx(
                    'rounded-2xl border p-5 transition-all shadow-sm',
                    rows.length > 1
                      ? 'border-gray-200 bg-gray-50/60'
                      : 'border-transparent bg-transparent p-0 shadow-none'
                  )}
                >
                  {rows.length > 1 && (
                    <div className="flex items-center justify-between mb-4 pb-2 border-b border-gray-200">
                      <div className="flex items-center gap-2">
                        <span className="w-6 h-6 rounded-full bg-primary-600 text-white font-bold text-xs flex items-center justify-center">
                          {rIdx + 1}
                        </span>
                        <h4 className="font-semibold text-gray-800 text-sm">
                          Entry #{rIdx + 1} (नोंद {rIdx + 1})
                        </h4>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <button
                          type="button"
                          onClick={() => duplicateRow(rIdx)}
                          title="Duplicate this row"
                          className="btn-ghost btn-xs text-gray-500 hover:text-gray-700 flex items-center gap-1"
                        >
                          <Copy className="w-3 h-3" /> Duplicate
                        </button>
                        <button
                          type="button"
                          onClick={() => removeRow(rIdx)}
                          title="Remove this row"
                          className="btn-ghost btn-xs text-red-500 hover:text-red-700 hover:bg-red-50 flex items-center gap-1"
                        >
                          <Trash2 className="w-3.5 h-3.5" /> Delete
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Form fields for this row */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {getFields().map((field, fIdx) => (
                      <div
                        key={field.id}
                        className={clsx(
                          'form-group mb-0',
                          field.type === 'textarea' && 'sm:col-span-2'
                        )}
                      >
                        <label className="label text-xs mb-1">
                          {rows.length > 1 ? field.label : `${fIdx + 1}. ${field.label}`}
                          {field.required && <span className="text-red-500 ml-0.5">*</span>}
                        </label>
                        {renderField(field, rIdx)}
                        {errors[rIdx]?.[field.id] && (
                          <p className="error-message text-xs mt-1 flex items-center gap-1">
                            <AlertCircle className="w-3 h-3 text-red-500" />
                            {errors[rIdx][field.id]}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Bottom Add Row Button */}
            <div className="pt-2 flex justify-center">
              <button
                type="button"
                onClick={addRow}
                className="btn-secondary btn-sm flex items-center gap-2 border-dashed border-gray-300 hover:border-primary-500 hover:text-primary-600 px-6 py-2 rounded-xl"
              >
                <Plus className="w-4 h-4 text-primary-600" />
                + Add Another Row / Person (+ आणखी {rows.length + 1} वी नोंद जोडा)
              </button>
            </div>
          </div>
        </Modal>
      )}

      {/* View Submitted Response Modal */}
      {viewingForm && (
        <Modal
          open={!!viewingForm}
          onClose={() => setViewingForm(null)}
          title={`Submitted: ${viewingForm.title}`}
          size="lg"
          footer={
            <button onClick={() => setViewingForm(null)} className="btn-secondary">
              Close
            </button>
          }
        >
          <div className="space-y-4">
            <div className="flex items-center justify-between text-xs text-gray-500 pb-3 border-b border-gray-100">
              <span>Form ID: #{viewingForm.id}</span>
              <span className="badge badge-green">Submitted</span>
            </div>

            {viewingData && viewingData.length > 0 ? (
              <div className="overflow-x-auto border border-gray-200 rounded-xl">
                <table className="w-full text-left text-xs border-collapse">
                  <thead className="bg-gray-50 border-b border-gray-200 text-gray-600">
                    <tr>
                      <th className="py-2.5 px-3 font-semibold w-12">#</th>
                      {getFields(viewingForm).map(f => (
                        <th key={f.id} className="py-2.5 px-3 font-semibold">
                          {f.label}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {viewingData.map((rowItem, idx) => (
                      <tr key={idx} className="hover:bg-gray-50/60">
                        <td className="py-2.5 px-3 font-bold text-gray-400">{idx + 1}</td>
                        {getFields(viewingForm).map(f => (
                          <td key={f.id} className="py-2.5 px-3 text-gray-800">
                            {rowItem[f.id] ? String(rowItem[f.id]) : '—'}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-6 text-gray-400 text-sm">
                No response details available
              </div>
            )}
          </div>
        </Modal>
      )}
    </div>
  )
}
