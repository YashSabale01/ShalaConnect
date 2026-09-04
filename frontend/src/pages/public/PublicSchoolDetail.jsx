import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { schoolApi, attendanceApi, eventApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import {
  ArrowLeft, Building2, MapPin, Phone, Mail, Users,
  Trophy, TrendingUp, GraduationCap, CalendarCheck2,
  Camera, Calendar, X, ZoomIn, Sparkles
} from 'lucide-react'
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function PublicSchoolDetail() {
  const { id } = useParams()
  const { data: school, loading: sLoading } = useApi(() => schoolApi.getById(id), [id])
  const { data: attendance } = useApi(() => attendanceApi.getBySchool(id), [id])
  const { data: implementations, loading: iLoading } = useApi(() => eventApi.getSchoolImplementations(id), [id])
  const [selectedPhoto, setSelectedPhoto] = useState(null)

  const chartData = (attendance || []).slice(0, 30).reverse().map(r => ({
    date: format(new Date(r.attendanceDate), 'dd MMM'),
    attendance: Math.round(r.attendancePercentage),
  }))

  const avgAttendance = attendance?.length
    ? Math.round(attendance.slice(0, 30).reduce((s, r) => s + r.attendancePercentage, 0) / Math.min(attendance.length, 30))
    : 0

  if (sLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-primary-600 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (!school) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <p className="text-gray-500">School not found</p>
    </div>
  )

  const activeImplementations = (implementations || []).filter(impl => impl.photoPaths?.length > 0 || impl.description)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="sticky top-0 z-40 bg-white border-b border-gray-100 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-gray-600 hover:text-gray-900">
            <ArrowLeft className="w-4 h-4" />
            <span className="text-sm font-medium">Back to Portal</span>
          </Link>
          <div className="flex items-center gap-2">
            <GraduationCap className="w-5 h-5 text-primary-600" />
            <span className="font-bold text-gray-900 text-sm">ShalaConnect | शाळाकनेक्ट</span>
          </div>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
        {/* Hero section */}
        <div className="card overflow-hidden mb-6">
          <div className="h-48 bg-gradient-to-br from-primary-600 to-primary-800 flex items-center justify-center relative overflow-hidden">
            {school.schoolPhoto ? (
              <img src={`/uploads/${school.schoolPhoto}`} alt={school.name}
                className="w-full h-full object-cover" />
            ) : (
              <Building2 className="w-20 h-20 text-white/30" />
            )}
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
            <div className="absolute bottom-0 left-0 p-6 text-white">
              <h1 className="text-2xl font-bold drop-shadow-sm">{school.name}</h1>
              <p className="text-sm text-white/90 font-mono mt-1">UDISE: {school.udiseCode}</p>
            </div>
          </div>

          <div className="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-xl">
              <div className="text-2xl font-bold text-blue-700">{school.totalStudents ?? '—'}</div>
              <div className="text-xs text-blue-500 mt-1">Total Students</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-xl">
              <div className="text-2xl font-bold text-green-700">{school.totalTeachers ?? '—'}</div>
              <div className="text-xs text-green-500 mt-1">Total Teachers</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-xl">
              <div className="text-2xl font-bold text-purple-700">{avgAttendance}%</div>
              <div className="text-xs text-purple-500 mt-1">Avg Attendance</div>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-xl">
              <div className="text-2xl font-bold text-orange-700">{attendance?.length ?? 0}</div>
              <div className="text-xs text-orange-500 mt-1">Days Tracked</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* School info */}
          <div className="card p-6 space-y-4">
            <h2 className="font-semibold text-gray-900">School Information</h2>
            {school.village && (
              <div className="flex items-start gap-2.5 text-sm text-gray-600">
                <MapPin className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
                <div>
                  <div>{school.address || school.village}</div>
                  <div className="text-gray-400">{[school.taluka, school.district, school.pincode].filter(Boolean).join(', ')}</div>
                </div>
              </div>
            )}
            {school.phone && (
              <div className="flex items-center gap-2.5 text-sm text-gray-600">
                <Phone className="w-4 h-4 text-gray-400 flex-shrink-0" />
                <span>{school.phone}</span>
              </div>
            )}
            {school.email && (
              <div className="flex items-center gap-2.5 text-sm text-gray-600">
                <Mail className="w-4 h-4 text-gray-400 flex-shrink-0" />
                <span className="truncate">{school.email}</span>
              </div>
            )}
            {school.topperName && (
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-xl mt-4">
                <div className="flex items-center gap-2 mb-2">
                  <Trophy className="w-5 h-5 text-yellow-500" />
                  <span className="font-semibold text-yellow-800">School Topper</span>
                </div>
                <p className="text-base font-bold text-gray-900">{school.topperName}</p>
                <p className="text-sm text-gray-500">
                  Class {school.topperClass} • <strong className="text-yellow-700">{school.topperPercentage}%</strong>
                </p>
              </div>
            )}
          </div>

          {/* Attendance chart */}
          <div className="lg:col-span-2 card p-6">
            <h2 className="font-semibold text-gray-900 mb-4">
              <CalendarCheck2 className="w-4 h-4 inline mr-2 text-primary-500" />
              Attendance Trend (Last 30 Days)
            </h2>
            {chartData.length === 0 ? (
              <div className="h-48 flex items-center justify-center text-sm text-gray-400">
                No attendance data available
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
                  <Line type="monotone" dataKey="attendance" stroke="#3b82f6" strokeWidth={2.5} dot={{ r: 3, fill: '#3b82f6' }} />
                </LineChart>
              </ResponsiveContainer>
            )}

            {/* Recent records */}
            {attendance?.length > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-100">
                <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Recent Records</p>
                <div className="space-y-2">
                  {attendance.slice(0, 5).map(r => (
                    <div key={r.id} className="flex items-center gap-3">
                      <span className="text-xs text-gray-400 w-24 flex-shrink-0">
                        {format(new Date(r.attendanceDate), 'dd MMM yyyy')}
                      </span>
                      <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className={clsx('h-full rounded-full',
                            r.attendancePercentage >= 80 ? 'bg-green-500' :
                            r.attendancePercentage >= 60 ? 'bg-yellow-500' : 'bg-red-500')}
                          style={{ width: `${r.attendancePercentage}%` }}
                        />
                      </div>
                      <span className={clsx('text-xs font-semibold w-10 text-right',
                        r.attendancePercentage >= 80 ? 'text-green-600' :
                        r.attendancePercentage >= 60 ? 'text-yellow-600' : 'text-red-500')}>
                        {Math.round(r.attendancePercentage)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Event Implementations & Photo Proof Gallery */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <Camera className="w-5 h-5 text-primary-600" />
                School Activities & Event Celebrations (शालेय उपक्रम व छायाचित्रे)
              </h2>
              <p className="text-sm text-gray-500 mt-0.5">
                Official event implementation reports and photo proof uploaded by the school
              </p>
            </div>
            {activeImplementations.length > 0 && (
              <span className="badge badge-blue">
                {activeImplementations.length} Events Documented
              </span>
            )}
          </div>

          {iLoading ? (
            <div className="py-12 flex justify-center">
              <div className="w-6 h-6 border-2 border-primary-600 border-t-transparent rounded-full animate-spin" />
            </div>
          ) : activeImplementations.length === 0 ? (
            <div className="text-center py-12 text-gray-400 bg-gray-50 rounded-xl border border-dashed border-gray-200">
              <Camera className="w-10 h-10 mx-auto mb-2 text-gray-300" />
              <p className="text-sm font-medium text-gray-600">No event photos uploaded yet</p>
              <p className="text-xs text-gray-400 mt-1">
                Event implementation photos will appear here once submitted by the school.
              </p>
            </div>
          ) : (
            <div className="space-y-6">
              {activeImplementations.map(impl => (
                <div key={impl.id} className="border border-gray-100 rounded-2xl p-5 bg-gradient-to-br from-white to-gray-50/50 shadow-sm">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-3">
                    <div>
                      <h3 className="font-bold text-gray-900 text-base">
                        {impl.eventTitle || 'Cluster Event Celebration'}
                      </h3>
                      {impl.eventDate && (
                        <div className="flex items-center gap-1.5 text-xs text-gray-400 mt-0.5">
                          <Calendar className="w-3.5 h-3.5" />
                          <span>{format(new Date(impl.eventDate), 'dd MMMM yyyy')}</span>
                        </div>
                      )}
                    </div>
                    {impl.photoPaths?.length > 0 && (
                      <span className="badge badge-green text-xs w-fit">
                        📸 {impl.photoPaths.length} Photo{impl.photoPaths.length > 1 ? 's' : ''}
                      </span>
                    )}
                  </div>

                  {impl.description && (
                    <div className="p-3.5 bg-white border border-gray-100 rounded-xl text-sm text-gray-700 mb-4 whitespace-pre-wrap leading-relaxed">
                      {impl.description}
                    </div>
                  )}

                  {/* Photo Gallery Grid */}
                  {impl.photoPaths?.length > 0 && (
                    <div>
                      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2.5">
                        Activity Photographs
                      </p>
                      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                        {impl.photoPaths.map((photo, pIdx) => (
                          <div
                            key={pIdx}
                            onClick={() => setSelectedPhoto(`/uploads/${photo}`)}
                            className="group relative h-32 rounded-xl overflow-hidden cursor-pointer border border-gray-200 bg-gray-100 shadow-sm transition-transform duration-200 hover:-translate-y-1 hover:shadow-md"
                          >
                            <img
                              src={`/uploads/${photo}`}
                              alt={`Event photo ${pIdx + 1}`}
                              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                              loading="lazy"
                            />
                            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                              <ZoomIn className="w-6 h-6 text-white drop-shadow-md" />
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Lightbox / Zoom Modal */}
      {selectedPhoto && (
        <div
          className="fixed inset-0 z-50 bg-black/90 backdrop-blur-sm flex items-center justify-center p-4"
          onClick={() => setSelectedPhoto(null)}
        >
          <button
            onClick={() => setSelectedPhoto(null)}
            className="absolute top-4 right-4 text-white hover:text-gray-300 p-2 rounded-full bg-white/10 hover:bg-white/20 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
          <img
            src={selectedPhoto}
            alt="Enlarged implementation photograph"
            className="max-h-[90vh] max-w-[95vw] rounded-xl shadow-2xl object-contain"
            onClick={e => e.stopPropagation()}
          />
        </div>
      )}
    </div>
  )
}
