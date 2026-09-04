import { useState } from 'react'
import { formApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import {
  ClipboardList, CheckCircle2, Clock, AlertCircle, Send,
  Plus, Trash2, Copy, Eye, Table, LayoutList, School,
  Edit3, Lock
} from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function HeadmasterFormsPage() {
  const { data: forms, loading, refetch } = useApi(() => formApi.getAll())
  const [activeForm,     setActiveForm]     = useState(null)
  const [isEditing,      setIsEditing]      = useState(false)
  const [viewingForm,    setViewingForm]    = useState(null)
  const [viewingData,    setViewingData]    = useState(null)
  const [rows,           setRows]           = useState([{}])
  const [viewMode,       setViewMode]       = useState('table') // 'table' | 'cards'
  const [submitting,     setSubmitting]     = useState(false)
  const [errors,         setErrors]         = useState({})

  const getFields = (formObj = activeForm) => {
    if (!formObj?.fieldsJson) return []
    if (Array.isArray(formObj.fieldsJson)) return formObj.fieldsJson
    try {
      return typeof formObj.fieldsJson === 'string' ? JSON.parse(formObj.fieldsJson) : []
    } catch {
      return []
    }
  }

  const openForm = async (form) => {
    try {
      const res = await formApi.getById(form.id)
      const data = res.data.data
      if (data.isExpired) {
        toast.error('The deadline for this form has passed. Submissions are closed.')
        return
      }
      setActiveForm(data)
      setIsEditing(false)
      setRows([{}])
      setErrors({})
      const fieldCount = getFields(data).length
      setViewMode(fieldCount <= 5 ? 'table' : 'cards')
    } catch {
      toast.error('Failed to load form')
    }
  }

  const openEditForm = async (form) => {
    try {
      const res = await formApi.getById(form.id)
      const data = res.data.data
      if (data.isExpired) {
        toast.error('The deadline for this form has passed. Editing is locked.')
        return
      }
      setActiveForm(data)
      setIsEditing(true)
      setErrors({})

      let existingRows = [{}]
      const raw = data.myAnswersJson
      if (raw) {
        try {
          const json = typeof raw === 'string' ? JSON.parse(raw) : raw
          if (Array.isArray(json)) existingRows = json
          else if (json.rows && Array.isArray(json.rows)) existingRows = json.rows
          else existingRows = [json]
        } catch {}
      }
      setRows(existingRows.length > 0 ? existingRows : [{}])
      const fieldCount = getFields(data).length
      setViewMode(fieldCount <= 5 ? 'table' : 'cards')
    } catch {
      toast.error('Failed to load response for editing')
    }
  }

  const openViewResponse = async (form) => {
    try {
      const res = await formApi.getById(form.id)
      const data = res.data.data
      setViewingForm(data)

      let parsed = []
      try {
        const raw = data.myAnswersJson || data.answersJson
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
      const res = await formApi.respond(activeForm.id, { answersJson: JSON.stringify(payload) })
      toast.success(res.data?.message || (isEditing ? 'Response updated successfully!' : 'Response submitted successfully!'))
      setActiveForm(null)
      setIsEditing(false)
      refetch()
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to submit form')
    } finally {
      setSubmitting(false)
    }
  }

  const renderField = (field, rIdx, compact = false) => {
    const value = rows[rIdx]?.[field.id] || ''
    const error = errors[rIdx]?.[field.id]
    const baseClass = `input w-full ${compact ? 'text-xs py-1.5 px-2' : 'text-sm py-2'}${error ? ' input-error' : ''}`

    switch (field.type) {
      case 'textarea':
        return (
          <textarea
            className={baseClass}
            rows={compact ? 1 : 2}
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
          <div className={clsx('flex flex-wrap gap-2', compact ? 'text-xs' : 'text-sm mt-1')}>
            {(field.options || []).map(opt => (
              <label key={opt} className="flex items-center gap-1.5 cursor-pointer">
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

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Forms (माहिती प्रपत्रे)</h1>
          <p className="page-subtitle">
            {pending.length > 0
              ? `${pending.length} pending form${pending.length > 1 ? 's' : ''} to fill`
              : 'All assigned forms completed'}
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
          {/* Pending Forms */}
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
                              <span className={clsx('flex items-center gap-1 font-medium', f.isExpired ? 'text-gray-400' : 'text-red-500')}>
                                <Clock className="w-3 h-3" />
                                {f.isExpired ? 'Expired: ' : 'Due: '}
                                {format(new Date(f.deadline), 'dd MMM yyyy, hh:mm a')}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                      {f.isExpired ? (
                        <span className="badge badge-gray text-xs flex items-center gap-1">
                          <Lock className="w-3 h-3" /> Deadline Passed
                        </span>
                      ) : (
                        <button onClick={() => openForm(f)} className="btn-primary btn-sm flex-shrink-0">
                          Fill Form
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Completed Forms with View & Edit Support */}
          {completed.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
                Completed Forms ({completed.length})
              </h2>
              <div className="space-y-3">
                {completed.map(f => (
                  <div key={f.id} className="card p-5 border-l-4 border-l-green-500 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <div className="flex items-start gap-4 flex-1 min-w-0">
                      <div className="w-10 h-10 rounded-xl bg-green-100 flex items-center justify-center flex-shrink-0">
                        <CheckCircle2 className="w-5 h-5 text-green-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-800">{f.title}</h3>
                        {f.description && (
                          <p className="text-sm text-gray-400 mt-0.5 line-clamp-1">{f.description}</p>
                        )}
                        <div className="flex items-center gap-3 text-xs text-gray-400 mt-1.5">
                          {f.deadline && (
                            <span className={clsx('flex items-center gap-1', f.isExpired ? 'text-gray-400' : 'text-amber-600 font-medium')}>
                              <Clock className="w-3 h-3" />
                              Deadline: {format(new Date(f.deadline), 'dd MMM yyyy, hh:mm a')}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 flex-shrink-0 self-end sm:self-auto">
                      <span className="badge badge-green">Submitted</span>
                      <button
                        onClick={() => openViewResponse(f)}
                        className="btn-secondary btn-sm flex items-center gap-1"
                        title="View your submitted response"
                      >
                        <Eye className="w-3.5 h-3.5" /> View
                      </button>

                      {/* Edit Response Until Deadline */}
                      {!f.isExpired ? (
                        <button
                          onClick={() => openEditForm(f)}
                          className="btn-primary btn-sm flex items-center gap-1"
                          title="Edit response before deadline"
                        >
                          <Edit3 className="w-3.5 h-3.5" /> Edit Response
                        </button>
                      ) : (
                        <span
                          className="badge badge-gray text-[10px] flex items-center gap-1"
                          title="Deadline has passed. Editing is locked."
                        >
                          <Lock className="w-3 h-3" /> Locked
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Fill / Edit Form Modal */}
      {activeForm && (
        <Modal
          open={!!activeForm}
          onClose={() => { setActiveForm(null); setIsEditing(false) }}
          title={isEditing ? `Edit Response: ${activeForm.title}` : activeForm.title}
          size="xl"
          footer={
            <div className="flex items-center justify-between w-full">
              <div className="text-xs text-gray-600 flex items-center gap-2">
                <span className="font-semibold text-gray-800">
                  Total Rows: {rows.length}
                </span>
                {isEditing && (
                  <span className="badge badge-amber text-[10px]">Editing Mode</span>
                )}
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => { setActiveForm(null); setIsEditing(false) }}
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
                  {submitting ? 'Saving…' : (
                    <>
                      <Send className="w-4 h-4" />
                      {isEditing
                        ? `Update Response (${rows.length} Rows)`
                        : `Submit (${rows.length} Rows)`}
                    </>
                  )}
                </button>
              </div>
            </div>
          }
        >
          <div className="space-y-5">
            {/* Combined School Info Banner */}
            <div className="flex flex-wrap items-center justify-between gap-2 p-3 bg-gradient-to-r from-primary-50 to-blue-50/50 border border-primary-100 rounded-xl text-xs text-primary-950">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded-lg bg-primary-600 text-white flex items-center justify-center font-bold text-[10px] flex-shrink-0">
                  <School className="w-3.5 h-3.5" />
                </div>
                <span>
                  <strong>School:</strong> {activeForm.schoolName || 'Your Assigned School'}
                  {activeForm.udiseCode && <span className="text-primary-700 ml-1 font-mono">(UDISE: {activeForm.udiseCode})</span>}
                </span>
              </div>
              <span className="badge badge-green text-[10px]">
                School Tenancy Verified
              </span>
            </div>

            {/* Editing Notice Banner */}
            {isEditing && (
              <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 flex items-center gap-2">
                <Edit3 className="w-4 h-4 text-amber-600 flex-shrink-0" />
                <span>
                  <strong>Editing previously submitted response:</strong> You can add, edit, or remove rows until the deadline. Click <strong>"Update Response"</strong> to save your changes.
                </span>
              </div>
            )}

            {/* Form Description */}
            {activeForm.description && (
              <div className="p-3.5 bg-blue-50 border border-blue-100 rounded-xl text-sm text-blue-800 leading-relaxed">
                {activeForm.description}
              </div>
            )}

            {/* Controls Bar: View Mode & Add Row */}
            <div className="flex items-center justify-between bg-gray-50 border border-gray-200 rounded-xl p-2.5">
              <div className="flex items-center gap-1">
                <span className="text-xs font-semibold text-gray-500 mr-1 hidden sm:inline">View Mode:</span>
                <button
                  type="button"
                  onClick={() => setViewMode('table')}
                  className={clsx(
                    'btn-xs flex items-center gap-1 rounded-lg px-2.5 py-1',
                    viewMode === 'table'
                      ? 'bg-white text-primary-700 shadow-sm border border-gray-200 font-semibold'
                      : 'text-gray-500 hover:text-gray-700'
                  )}
                >
                  <Table className="w-3.5 h-3.5" /> Table Grid
                </button>
                <button
                  type="button"
                  onClick={() => setViewMode('cards')}
                  className={clsx(
                    'btn-xs flex items-center gap-1 rounded-lg px-2.5 py-1',
                    viewMode === 'cards'
                      ? 'bg-white text-primary-700 shadow-sm border border-gray-200 font-semibold'
                      : 'text-gray-500 hover:text-gray-700'
                  )}
                >
                  <LayoutList className="w-3.5 h-3.5" /> Cards View
                </button>
              </div>

              <button
                type="button"
                onClick={addRow}
                className="btn-primary btn-xs flex items-center gap-1"
              >
                <Plus className="w-3.5 h-3.5" /> + Add Row
              </button>
            </div>

            {/* TABLE GRID VIEW */}
            {viewMode === 'table' && (
              <div className="overflow-x-auto border border-gray-200 rounded-xl max-h-[60vh] overflow-y-auto">
                <table className="w-full text-left text-xs border-collapse min-w-[600px]">
                  <thead className="bg-gray-100 text-gray-700 sticky top-0 z-10 border-b border-gray-200">
                    <tr>
                      <th className="py-2.5 px-3 w-10 text-center font-bold text-gray-500">#</th>
                      {getFields().map(field => (
                        <th key={field.id} className="py-2.5 px-2 font-semibold">
                          {field.label}
                          {field.required && <span className="text-red-500 ml-0.5">*</span>}
                        </th>
                      ))}
                      <th className="py-2.5 px-2 w-16 text-center font-semibold">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 bg-white">
                    {rows.map((row, rIdx) => (
                      <tr key={rIdx} className="hover:bg-gray-50/50">
                        <td className="py-2 px-2 text-center font-bold text-gray-400 bg-gray-50/40">
                          {rIdx + 1}
                        </td>
                        {getFields().map(field => (
                          <td key={field.id} className="py-2 px-2 align-top">
                            {renderField(field, rIdx, true)}
                            {errors[rIdx]?.[field.id] && (
                              <span className="text-[10px] text-red-500 block mt-0.5">
                                {errors[rIdx][field.id]}
                              </span>
                            )}
                          </td>
                        ))}
                        <td className="py-2 px-2 text-center align-top">
                          <div className="flex items-center justify-center gap-1 mt-1">
                            <button
                              type="button"
                              onClick={() => duplicateRow(rIdx)}
                              title="Duplicate row"
                              className="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded"
                            >
                              <Copy className="w-3.5 h-3.5" />
                            </button>
                            {rows.length > 1 && (
                              <button
                                type="button"
                                onClick={() => removeRow(rIdx)}
                                title="Delete row"
                                className="p-1 text-red-400 hover:text-red-600 hover:bg-red-50 rounded"
                              >
                                <Trash2 className="w-3.5 h-3.5" />
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* STACKED CARDS VIEW */}
            {viewMode === 'cards' && (
              <div className="space-y-4 max-h-[60vh] overflow-y-auto pr-1">
                {rows.map((row, rIdx) => (
                  <div
                    key={rIdx}
                    className={clsx(
                      'rounded-xl border p-4 transition-all',
                      rows.length > 1 ? 'border-gray-200 bg-gray-50/50 shadow-sm' : 'border-gray-100 bg-white'
                    )}
                  >
                    {rows.length > 1 && (
                      <div className="flex items-center justify-between mb-3 pb-2 border-b border-gray-200">
                        <span className="font-semibold text-gray-700 text-xs flex items-center gap-1.5">
                          <span className="w-5 h-5 rounded-full bg-primary-600 text-white font-bold text-[10px] flex items-center justify-center">
                            {rIdx + 1}
                          </span>
                          Row #{rIdx + 1}
                        </span>
                        <div className="flex items-center gap-1">
                          <button
                            type="button"
                            onClick={() => duplicateRow(rIdx)}
                            className="btn-ghost btn-xs text-gray-500 hover:text-gray-700 flex items-center gap-1"
                          >
                            <Copy className="w-3 h-3" /> Duplicate
                          </button>
                          <button
                            type="button"
                            onClick={() => removeRow(rIdx)}
                            className="btn-ghost btn-xs text-red-500 hover:text-red-700 hover:bg-red-50 flex items-center gap-1"
                          >
                            <Trash2 className="w-3.5 h-3.5" /> Delete
                          </button>
                        </div>
                      </div>
                    )}

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                      {getFields().map((field, fIdx) => (
                        <div
                          key={field.id}
                          className={clsx(
                            'form-group mb-0',
                            field.type === 'textarea' && 'sm:col-span-2'
                          )}
                        >
                          <label className="label text-xs mb-1">
                            {field.label}
                            {field.required && <span className="text-red-500 ml-0.5">*</span>}
                          </label>
                          {renderField(field, rIdx, false)}
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
            )}

            {/* Bottom Add Row Bar */}
            <div className="pt-2 flex justify-center">
              <button
                type="button"
                onClick={addRow}
                className="btn-secondary btn-sm flex items-center gap-2 border-dashed border-gray-300 hover:border-primary-500 hover:text-primary-600 px-6 py-2 rounded-xl"
              >
                <Plus className="w-4 h-4 text-primary-600" />
                + Add Row ({rows.length + 1})
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
          title={`Submitted Response: ${viewingForm.title}`}
          size="lg"
          footer={
            <div className="flex items-center justify-between w-full">
              <span className="text-xs text-gray-500">
                {viewingForm.isExpired ? 'Form deadline passed (locked)' : 'Editable until deadline'}
              </span>
              <div className="flex items-center gap-2">
                {!viewingForm.isExpired && (
                  <button
                    onClick={() => {
                      const formToEdit = viewingForm
                      setViewingForm(null)
                      openEditForm(formToEdit)
                    }}
                    className="btn-primary btn-sm flex items-center gap-1"
                  >
                    <Edit3 className="w-3.5 h-3.5" /> Edit This Response
                  </button>
                )}
                <button onClick={() => setViewingForm(null)} className="btn-secondary btn-sm">
                  Close
                </button>
              </div>
            </div>
          }
        >
          <div className="space-y-4">
            {/* Combined School Info Banner */}
            <div className="flex flex-wrap items-center justify-between gap-2 p-3 bg-gradient-to-r from-primary-50 to-blue-50/50 border border-primary-100 rounded-xl text-xs text-primary-950">
              <div className="flex items-center gap-2">
                <School className="w-4 h-4 text-primary-600 flex-shrink-0" />
                <span>
                  <strong>School:</strong> {viewingForm.schoolName || 'Your School'}
                  {viewingForm.udiseCode && <span className="text-primary-700 ml-1 font-mono">(UDISE: {viewingForm.udiseCode})</span>}
                </span>
              </div>
              <span className="badge badge-green text-[10px]">
                {viewingData ? `${viewingData.length} Rows Submitted` : 'Submitted'}
              </span>
            </div>

            <div className="flex items-center justify-between text-xs text-gray-500 pb-2 border-b border-gray-100">
              <span>Form ID: #{viewingForm.id}</span>
              <span>
                {viewingForm.mySubmittedAt && `Submitted: ${format(new Date(viewingForm.mySubmittedAt), 'dd/MM/yyyy HH:mm')}`}
                {viewingForm.myUpdatedAt && viewingForm.myUpdatedAt !== viewingForm.mySubmittedAt && ` • Updated: ${format(new Date(viewingForm.myUpdatedAt), 'dd/MM/yyyy HH:mm')}`}
              </span>
            </div>

            {viewingData && viewingData.length > 0 ? (
              <div className="overflow-x-auto border border-gray-200 rounded-xl">
                <table className="w-full text-left text-xs border-collapse">
                  <thead className="bg-gray-50 border-b border-gray-200 text-gray-600">
                    <tr>
                      <th className="py-2.5 px-3 font-semibold w-12 text-center">#</th>
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
                        <td className="py-2.5 px-3 text-center font-bold text-gray-400 bg-gray-50/30">
                          {idx + 1}
                        </td>
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
