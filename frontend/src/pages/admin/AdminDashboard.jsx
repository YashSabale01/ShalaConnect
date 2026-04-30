import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { attendanceApi, schoolApi, meetingApi, grApi } from '../../services/api'
import StatCard from '../../components/ui/StatCard'
import { CardSkeleton } from '../../components/ui/Skeleton'
import {
  Building2, Users, CalendarCheck2, TrendingUp,
  Clock, FileText, CalendarDays, AlertCircle,
  CheckCircle2, XCircle
} from 'lucide-react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function AdminDashboard() {
  const [summary,  setSummary]  = useState(null)
  const [schools,  setSchools]  = useState([])
  const [meetings, setMeetings] = useState([])
  const [grDocs,   setGrDocs]   = useState([])
  const [loading,  setLoading]  = useState(true)

  useEffect(() => {
    Promise.all([
      attendanceApi.getSummary(),
      schoolApi.getAll(),
      meetingApi.getUpcoming(),
      grApi.getAll(),
    ]).then(([s, sc, m, gr]) => {
      setSummary(s.data.data)
      setSchools(sc.data.data || [])
      setMeetings(m.data.data || [])
      setGrDocs(gr.data.data || [])
    }).finally(() => setLoading(false))
  }, [])

  // Build bar chart data from today's records
  const chartData = (summary?.todayRecords || []).map(r => ({
    school: r.schoolName?.split(' ')[0] || 'School',
    attendance: Math.round(r.attendancePercentage),
  }))

  if (loading) {
    return (
      <div>
        <div className="page-header">
          <div>
            <div className="h-7 w-48 skeleton rounded mb-1" />
            <div className="h-4 w-64 skeleton rounded" />
          </div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {[...Array(4)].map((_, i) => <CardSkeleton key={i} />)}
        </div>
      </div>
    )
  }

  const submissionRate = schools.length
    ? Math.round(((summary?.submittedToday || 0) / schools.length) * 100)
    : 0

  return (
    <div className="page-transition">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">
            {format(new Date(), 'EEEE, dd MMMM yyyy')} — Overview of all schools
          </p>
        </div>
        <Link to="/admin/attendance" className="btn-primary">
          <CalendarCheck2 className="w-4 h-4" />
          View Attendance
        </Link>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard
          icon={Building2} label="Total Schools" value={schools.length}
          sub="Active schools in cluster" color="blue"
        />
        <StatCard
          icon={CalendarCheck2} label="Submitted Today"
          value={`${summary?.submittedToday || 0}/${schools.length}`}
          sub={`${submissionRate}% submission rate`}
          color={submissionRate >= 80 ? 'green' : 'orange'}
        />
        <StatCard
          icon={TrendingUp} label="Avg Attendance Today"
          value={`${summary?.avgAttendanceToday || 0}%`}
          sub="Across all schools" color="purple"
        />
        <StatCard
          icon={TrendingUp} label="Avg Attendance (Month)"
          value={`${summary?.avgAttendanceMonth || 0}%`}
          sub="This month average" color="teal"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Attendance Chart */}
        <div className="lg:col-span-2 card p-5">
          <h2 className="text-base font-semibold text-gray-900 mb-4">Today's Attendance by School</h2>
          {chartData.length === 0 ? (
            <div className="h-48 flex items-center justify-center text-gray-400 text-sm">
              No attendance data for today yet
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={chartData} margin={{ top: 4, right: 4, bottom: 4, left: -20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
                <XAxis dataKey="school" tick={{ fontSize: 11 }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
                <Tooltip
                  formatter={(v) => [`${v}%`, 'Attendance']}
                  contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb', fontSize: '12px' }}
                />
                <Bar dataKey="attendance" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Pending schools */}
        <div className="card p-5">
          <h2 className="text-base font-semibold text-gray-900 mb-4">Submission Status</h2>
          <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
            {schools.map(school => {
              const submitted = summary?.todayRecords?.some(r => r.schoolId === school.id)
              return (
                <div key={school.id} className="flex items-center gap-2.5 py-1.5">
                  {submitted
                    ? <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0" />
                    : <XCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
                  }
                  <span className="text-sm text-gray-700 flex-1 truncate">{school.name}</span>
                  <span className={clsx('badge text-xs',
                    submitted ? 'badge-green' : 'badge-red')}>
                    {submitted ? 'Done' : 'Pending'}
                  </span>
                </div>
              )
            })}
          </div>
        </div>

        {/* Upcoming meetings */}
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-gray-900">Upcoming Meetings</h2>
            <Link to="/admin/meetings" className="text-xs text-primary-600 hover:underline font-medium">View all</Link>
          </div>
          <div className="space-y-3">
            {meetings.length === 0 ? (
              <p className="text-sm text-gray-400 text-center py-4">No upcoming meetings</p>
            ) : meetings.slice(0, 4).map(m => (
              <div key={m.id} className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-purple-100 flex items-center justify-center flex-shrink-0">
                  <CalendarDays className="w-4 h-4 text-purple-600" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-gray-900 truncate">{m.title}</p>
                  <p className="text-xs text-gray-400">
                    {m.scheduledAt && format(new Date(m.scheduledAt), 'dd MMM, hh:mm a')}
                  </p>
                </div>
                <span className={clsx('badge flex-shrink-0',
                  m.meetingType === 'ONLINE' ? 'badge-blue' : 'badge-purple')}>
                  {m.meetingType}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Recent GR Docs */}
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-gray-900">Recent GR Documents</h2>
            <Link to="/admin/gr-documents" className="text-xs text-primary-600 hover:underline font-medium">View all</Link>
          </div>
          <div className="space-y-3">
            {grDocs.length === 0 ? (
              <p className="text-sm text-gray-400 text-center py-4">No GR documents uploaded</p>
            ) : grDocs.slice(0, 4).map(d => (
              <div key={d.id} className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                  <FileText className="w-4 h-4 text-blue-600" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-gray-900 truncate">{d.title}</p>
                  <p className="text-xs text-gray-400">GR #{d.grNumber}</p>
                </div>
                <span className="text-xs text-gray-400 flex-shrink-0">{d.seenCount} seen</span>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card p-5">
          <h2 className="text-base font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="space-y-2">
            {[
              { to: '/admin/schools', label: 'Add New School', icon: Building2, color: 'text-blue-600 bg-blue-50' },
              { to: '/admin/gr-documents', label: 'Upload GR Document', icon: FileText, color: 'text-green-600 bg-green-50' },
              { to: '/admin/meetings', label: 'Schedule Meeting', icon: CalendarDays, color: 'text-purple-600 bg-purple-50' },
              { to: '/admin/forms', label: 'Create Form', icon: AlertCircle, color: 'text-orange-600 bg-orange-50' },
            ].map(({ to, label, icon: Icon, color }) => (
              <Link
                key={to}
                to={to}
                className="flex items-center gap-3 p-2.5 rounded-lg hover:bg-gray-50 transition-colors group"
              >
                <div className={clsx('w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0', color)}>
                  <Icon className="w-4 h-4" />
                </div>
                <span className="text-sm text-gray-700 group-hover:text-gray-900 font-medium">{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
