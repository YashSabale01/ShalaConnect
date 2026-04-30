import { useState, useRef } from 'react'
import { grApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import Modal from '../../components/ui/Modal'
import ConfirmDialog from '../../components/ui/ConfirmDialog'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import {
  FileText, Plus, Upload, Trash2, Eye, Download,
  CheckCircle2, Clock, AlertCircle, Search
} from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function GrDocumentsPage() {
  const { data: docs, loading, refetch } = useApi(() => grApi.getAll())
  const [showUpload, setShowUpload] = useState(false)
  const [deleting,   setDeleting]   = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [search,     setSearch]     = useState('')
  const [form, setForm] = useState({ title: '', grNumber: '', description: '' })
  const [file, setFile] = useState(null)
  const fileRef = useRef()

  const filtered = (docs || []).filter(d =>
    d.title.toLowerCase().includes(search.toLowerCase()) ||
    d.grNumber?.toLowerCase().includes(search.toLowerCase())
  )

  const handleUpload = async () => {
    if (!form.title || !form.grNumber || !file) {
      toast.error('Please fill all required fields and select a file')
      return
    }
    setSubmitting(true)
    try {
      const fd = new FormData()
      fd.append('title', form.title)
      fd.append('grNumber', form.grNumber)
      if (form.description) fd.append('description', form.description)
      fd.append('file', file)
      await grApi.upload(fd)
      toast.success('GR document uploaded and headmasters notified!')
      setShowUpload(false)
      setForm({ title: '', grNumber: '', description: '' })
      setFile(null)
      refetch()
    } catch (err) {
      toast.error(err.response?.data?.message || 'Upload failed')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async () => {
    setSubmitting(true)
    try {
      await grApi.delete(deleting.id)
      toast.success('GR document deleted')
      setDeleting(null)
      refetch()
    } catch {
      toast.error('Failed to delete document')
    } finally {
      setSubmitting(false)
    }
  }

  const formatSize = (bytes) => {
    if (!bytes) return ''
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">GR Documents</h1>
          <p className="page-subtitle">Upload and manage government resolutions & circulars</p>
        </div>
        <button onClick={() => setShowUpload(true)} className="btn-primary">
          <Upload className="w-4 h-4" /> Upload GR
        </button>
      </div>

      <div className="relative mb-5 max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text" placeholder="Search by title or GR number…"
          value={search} onChange={e => setSearch(e.target.value)}
          className="input pl-9"
        />
      </div>

      {loading ? (
        <ListSkeleton items={5} />
      ) : filtered.length === 0 ? (
        <EmptyState
          icon={FileText}
          title={search ? 'No documents found' : 'No GR documents yet'}
          description="Upload government resolutions for headmasters to read"
          action={!search && <button onClick={() => setShowUpload(true)} className="btn-primary"><Upload className="w-4 h-4" />Upload GR</button>}
        />
      ) : (
        <div className="space-y-3">
          {filtered.map(doc => (
            <div key={doc.id} className="card-hover p-4 flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center flex-shrink-0">
                <FileText className="w-5 h-5 text-blue-600" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <h3 className="font-semibold text-gray-900 truncate">{doc.title}</h3>
                  <span className="badge badge-blue">GR #{doc.grNumber}</span>
                </div>
                {doc.description && <p className="text-sm text-gray-500 truncate mt-0.5">{doc.description}</p>}
                <div className="flex items-center gap-3 mt-1 text-xs text-gray-400">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {doc.createdAt && format(new Date(doc.createdAt), 'dd MMM yyyy')}
                  </span>
                  {doc.fileName && <span>{doc.fileName} {doc.fileSize ? `(${formatSize(doc.fileSize)})` : ''}</span>}
                  <span className="flex items-center gap-1 text-green-600">
                    <CheckCircle2 className="w-3 h-3" />
                    {doc.seenCount} headmaster{doc.seenCount !== 1 ? 's' : ''} seen
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                <a
                  href={`/uploads/${doc.filePath}`}
                  target="_blank"
                  rel="noreferrer"
                  className="btn-ghost btn-sm p-1.5"
                  title="Download"
                >
                  <Download className="w-4 h-4" />
                </a>
                <button
                  onClick={() => setDeleting(doc)}
                  className="btn-ghost btn-sm p-1.5 text-red-400 hover:text-red-600 hover:bg-red-50"
                  title="Delete"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Upload Modal */}
      <Modal
        open={showUpload}
        onClose={() => { setShowUpload(false); setFile(null) }}
        title="Upload GR Document"
        footer={
          <>
            <button onClick={() => setShowUpload(false)} className="btn-secondary" disabled={submitting}>Cancel</button>
            <button onClick={handleUpload} className="btn-primary" disabled={submitting}>
              {submitting ? 'Uploading…' : 'Upload & Notify'}
            </button>
          </>
        }
      >
        <div className="space-y-4">
          <div className="form-group">
            <label className="label">Title *</label>
            <input className="input" placeholder="e.g. Attendance Policy 2024"
              value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))} />
          </div>
          <div className="form-group">
            <label className="label">GR Number *</label>
            <input className="input" placeholder="e.g. MSHRD/2024/CR-45"
              value={form.grNumber} onChange={e => setForm(f => ({ ...f, grNumber: e.target.value }))} />
          </div>
          <div className="form-group">
            <label className="label">Description (Optional)</label>
            <textarea className="input" rows={2} placeholder="Brief description of this GR…"
              value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))} />
          </div>
          <div className="form-group">
            <label className="label">Document File * (PDF or Image)</label>
            <div
              onClick={() => fileRef.current?.click()}
              className={clsx(
                'border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-colors',
                file ? 'border-green-400 bg-green-50' : 'border-gray-300 hover:border-primary-400 hover:bg-blue-50/30'
              )}
            >
              <input
                type="file" ref={fileRef} className="hidden"
                accept=".pdf,image/*"
                onChange={e => setFile(e.target.files[0])}
              />
              {file ? (
                <div className="flex items-center justify-center gap-2 text-green-700">
                  <CheckCircle2 className="w-5 h-5" />
                  <span className="text-sm font-medium">{file.name}</span>
                  <span className="text-xs text-green-500">({formatSize(file.size)})</span>
                </div>
              ) : (
                <>
                  <Upload className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                  <p className="text-sm text-gray-500">Click to upload PDF or image</p>
                  <p className="text-xs text-gray-400 mt-1">Max size: 20MB</p>
                </>
              )}
            </div>
          </div>
          <div className="p-3 bg-amber-50 border border-amber-200 rounded-lg flex gap-2">
            <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
            <p className="text-xs text-amber-700">All headmasters will receive a notification when you upload this document.</p>
          </div>
        </div>
      </Modal>

      <ConfirmDialog
        open={!!deleting} onClose={() => setDeleting(null)}
        onConfirm={handleDelete} loading={submitting}
        title="Delete GR Document"
        description={`Delete "${deleting?.title}"? This cannot be undone.`}
      />
    </div>
  )
}
