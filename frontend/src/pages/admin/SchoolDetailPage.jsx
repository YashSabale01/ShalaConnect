import { useState, useRef } from 'react'
import { useParams, Link } from 'react-router-dom'
import { schoolApi, attendanceApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import { CardSkeleton } from '../../components/ui/Skeleton'
import {
  ArrowLeft, Building2, MapPin, Phone, Mail, Users,
  Trophy, Upload, CalendarCheck2, TrendingUp
} from 'lucide-react'
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid
} from 'recharts'
import { format } from 'date-fns'
import toast from 'react-hot-toast'
import clsx from 'clsx'

export default function SchoolDetailPage() {
  const { id } = useParams()
  const { data: school, loading, refetch } = useApi(() => schoolApi.getById(id), [id])
  const { data: attendance } = useApi(() => attendanceApi.getBySchool(id), [id])
  const [uploading, setUploading] = useState(false)
  const photoRef = useRef()

  const handlePhotoUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    setUploading(true)
    try {
      await schoolApi.uploadPhoto(id, file)
      toast.success('School photo updated!')
      refetch()
    } catch { toast.error('Photo upload failed') }
    finally { setUploading(false) }
  }

  const chartData = (attendance || []).slice(0, 30).reverse().map(r => ({
    date: format(new Date(r.attendanceDate), 'dd MMM'),
    attendance: Math.round(r.attendancePercentage),
    present: r.presentStudents,
  }))

  const avgAttendance = attendance?.length
    ? Math.round(attendance.slice(0, 30).reduce((sum, r) => sum + r.attendancePercentage, 0) / Math.min(attendance.length, 30))
    : 0

  if (loading) {
    return (
      <div>
        <div className="h-6 w-32 skeleton rounded mb-6" />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <CardSkeleton /><CardSkeleton /><CardSkeleton />
        </div>
      </div>
    )
  }

  if (!school) return (
    <div className="text-center py-20 text-gray-400">School not found</div>
  )

  return (
    <div className="page-transition">
      <Link to="/admin/schools" className="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 mb-5">
        <ArrowLeft className="w-4 h-4" /> Back to Schools
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* School profile card */}
        <div className="card p-6">
          {/* Photo */}
          <div className="relative mb-5">
            <div className="w-full h-36 rounded-xl bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center overflow-hidden">
              {school.schoolPhoto ? (
                <img src={`/uploads/${school.schoolPhoto}`} alt={school.name}
                  className="w-full h-full object-cover" />
              ) : (
                <Building2 className="w-16 h-16 text-primary-400" />
              )}
            </div>
            <button
              onClick={() => photoRef.current?.click()}
              disabled={uploading}
              className="absolute bottom-2 right-2 btn-secondary btn-sm shadow-sm"
            >
              <Upload className="w-3 h-3" />
              {uploading ? 'Uploading…' : 'Change Photo'}
            </button>
            <input type="file" ref={photoRef} accept="image/*" className="hidden" onChange={handlePhotoUpload} />
          </div>

          <h1 className="text-xl font-bold text-gray-900 mb-1">{school.name}</h1>
          <p className="text-sm font-mono text-gray-400 bg-gray-100 px-2 py-0.5 rounded inline-block mb-4">
            UDISE: {school.udiseCode}
          </p>

          <div className="space-y-3 text-sm">
            {school.village && (
              <div className="flex items-start gap-2 text-gray-600">
                <MapPin className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
                <span>{[school.village, school.taluka, school.district].filter(Boolean).join(', ')}</span>
              </div>
            )}
            {school.phone && (
              <div className="flex items-center gap-2 text-gray-600">
                <Phone className="w-4 h-4 text-gray-400 flex-shrink-0" />
                <span>{school.phone}</span>
              </div>
            )}
            {school.email && (
              <div className="flex items-center gap-2 text-gray-600">
                <Mail className="w-4 h-4 text-gray-400 flex-shrink-0" />
                <span className="truncate">{school.email}</span>
              </div>
            )}
          </div>

          <div className="grid grid-cols-2 gap-3 mt-5 pt-5 border-t border-gray-100">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{school.totalStudents ?? '—'}</div>
              <div className="text-xs text-gray-400 mt-0.5">Students</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{school.totalTeachers ?? '—'}</div>
              <div className="text-xs text-gray-400 mt-0.5">Teachers</div>
            </div>
          </div>

          {school.topperName && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-xl">
              <div className="flex items-center gap-2 mb-1">
                <Trophy className="w-4 h-4 text-yellow-500" />
                <span className="text-sm font-semibold text-yellow-800">School Topper</span>
              </div>
              <p className="text-sm font-medium text-gray-900">{school.topperName}</p>
              <p className="text-xs text-gray-500">{school.topperClass} • {school.topperPercentage}%</p>
            </div>
          )}
        </div>

        {/* Attendance section */}
        <div className="lg:col-span-2 space-y-6">
          {/* Attendance stats */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="card p-4 text-center">
              <div className="text-2xl font-bold text-primary-600">{avgAttendance}%</div>
              <div className="text-xs text-gray-400 mt-1">Avg Attendance (30d)</div>
            </div>
            <div className="card p-4 text-center">
              <div className="text-2xl font-bold text-gray-900">{attendance?.length || 0}</div>
              <div className="text-xs text-gray-400 mt-1">Days Recorded</div>
            </div>
            <div className="card p-4 text-center">
              <div className="text-2xl font-bold text-gray-900">
                {attendance?.[0]?.presentStudents ?? '—'}
              </div>
              <div className="text-xs text-gray-400 mt-1">Present (Latest)</div>
            </div>
          </div>

          {/* Chart */}
          <div className="card p-5">
            <h2 className="font-semibold text-gray-900 mb-4">Attendance Trend (Last 30 Days)</h2>
            {chartData.length === 0 ? (
              <div className="h-40 flex items-center justify-center text-sm text-gray-400">
                No attendance records yet
              </div>
            ) : (
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={chartData} margin={{ top: 4, right: 4, bottom: 4, left: -20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
                  <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 10 }} />
                  <Tooltip
                    formatter={(v) => [`${v}%`, 'Attendance']}
                    contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb', fontSize: '12px' }}
                  />
                  <Line type="monotone" dataKey="attendance" stroke="#3b82f6" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>

          {/* Attendance records table */}
          <div className="card">
            <div className="p-5 border-b border-gray-100">
              <h2 className="font-semibold text-gray-900">Recent Attendance Records</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Total</th>
                    <th>Present</th>
                    <th>Absent</th>
                    <th>%</th>
                    <th>Submitted By</th>
                  </tr>
                </thead>
                <tbody>
                  {(attendance || []).slice(0, 15).map(r => (
                    <tr key={r.id}>
                      <td>{format(new Date(r.attendanceDate), 'dd MMM yyyy')}</td>
                      <td>{r.totalStudents}</td>
                      <td className="text-green-600 font-medium">{r.presentStudents}</td>
                      <td className="text-red-500">{r.absentStudents}</td>
                      <td>
                        <span className={clsx('font-semibold',
                          r.attendancePercentage >= 80 ? 'text-green-600' :
                          r.attendancePercentage >= 60 ? 'text-yellow-600' : 'text-red-500')}>
                          {Math.round(r.attendancePercentage)}%
                        </span>
                      </td>
                      <td className="text-gray-400">{r.submittedByName || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {(!attendance || attendance.length === 0) && (
                <div className="py-8 text-center text-sm text-gray-400">No attendance records</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
