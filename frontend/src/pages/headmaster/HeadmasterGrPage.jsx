import { grApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import EmptyState from '../../components/ui/EmptyState'
import { ListSkeleton } from '../../components/ui/Skeleton'
import { FileText, Download, CheckCircle2, Clock } from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function HeadmasterGrPage() {
  const { data: docs, loading, refetch } = useApi(() => grApi.getAll())

  const handleMarkSeen = async (doc) => {
    if (doc.seenByCurrentUser) return
    try {
      await grApi.markSeen(doc.id)
      toast.success('Marked as read')
      refetch()
    } catch { toast.error('Failed to mark as seen') }
  }

  const unread = (docs || []).filter(d => !d.seenByCurrentUser).length

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">GR Documents</h1>
          <p className="page-subtitle">
            Government resolutions and circulars
            {unread > 0 && <span className="ml-2 badge badge-blue">{unread} unread</span>}
          </p>
        </div>
      </div>

      {loading ? <ListSkeleton items={5} /> : (docs || []).length === 0 ? (
        <EmptyState
          icon={FileText}
          title="No GR documents yet"
          description="Government resolutions will appear here when uploaded by the admin"
        />
      ) : (
        <div className="space-y-3">
          {(docs || []).map(doc => (
            <div
              key={doc.id}
              className={clsx(
                'card-hover p-4 flex items-center gap-4 border-l-4 transition-all',
                doc.seenByCurrentUser ? 'border-l-gray-200' : 'border-l-blue-500 bg-blue-50/30'
              )}
            >
              <div className={clsx('w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0',
                doc.seenByCurrentUser ? 'bg-gray-100' : 'bg-blue-100')}>
                <FileText className={clsx('w-5 h-5', doc.seenByCurrentUser ? 'text-gray-500' : 'text-blue-600')} />
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap mb-0.5">
                  <h3 className={clsx('font-semibold', doc.seenByCurrentUser ? 'text-gray-700' : 'text-gray-900')}>
                    {doc.title}
                  </h3>
                  <span className="badge badge-blue">GR #{doc.grNumber}</span>
                  {!doc.seenByCurrentUser && (
                    <span className="badge badge-blue bg-blue-500 text-white">New</span>
                  )}
                </div>
                {doc.description && <p className="text-sm text-gray-500 mb-1 line-clamp-1">{doc.description}</p>}
                <div className="flex items-center gap-4 text-xs text-gray-400">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {doc.createdAt && format(new Date(doc.createdAt), 'dd MMM yyyy')}
                  </span>
                  {doc.fileName && <span>{doc.fileName}</span>}
                </div>
              </div>

              <div className="flex items-center gap-2 flex-shrink-0">
                {doc.seenByCurrentUser ? (
                  <div className="flex items-center gap-1 text-xs text-green-600">
                    <CheckCircle2 className="w-4 h-4" />
                    <span className="hidden sm:inline">Read</span>
                  </div>
                ) : (
                  <button
                    onClick={() => handleMarkSeen(doc)}
                    className="btn-secondary btn-sm"
                  >
                    Mark as Read
                  </button>
                )}
                <a
                  href={`/uploads/${doc.filePath}`}
                  target="_blank"
                  rel="noreferrer"
                  onClick={() => handleMarkSeen(doc)}
                  className="btn-primary btn-sm"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">View</span>
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
