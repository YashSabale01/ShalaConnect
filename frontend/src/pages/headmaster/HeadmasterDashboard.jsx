import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { attendanceApi, grApi, meetingApi, formApi } from '../../services/api'
import StatCard from '../../components/ui/StatCard'
import { CardSkeleton } from '../../components/ui/Skeleton'
import {
  CalendarCheck2, FileText, CalendarDays, ClipboardList,
  CheckCircle2, Clock, AlertCircle, TrendingUp, ArrowRight
} from 'lucide-react'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function HeadmasterDashboard() {
  const { user } = useAuth()
  const [attendance, setAttendance] = useState([])
  const [grDocs,     setGrDocs]     = useState([])
  const [meetings,   setMeetings]   = useState([])
  const [forms,      setForms]      = useState([])
  const [loading,    setLoading]    = useState(true)

  useEffect(() => {
    Promise.all([
      user?.school?.id ? attendanceApi.getBySchool(user.school.id) : Promise.resolve({ data: { data: [] } }),
      grApi.getAll(),
      meetingApi.getUpcoming(),
      formApi.getAll(),
    ]).then(([att, gr, mtg, frm]) => {
      setAttendance(att.data.data || [])
      setGrDocs(gr.data.data || [])
      setMeetings(mtg.data.data || [])
      setForms(frm.data.data || [])
    }).finally(() => setLoading(false))
  }, [user])

  const today = format(new Date(), 'yyyy-MM-dd')
  const todaySubmitted = attendance.some(a => a.attendanceDate === today)
  const unreadGr = grDocs.filter(d => !d.seenByCurrentUser).length
  const pendingForms = forms.filter(f => !f.hasResponded).length
  const avgAttendance = attendance.length
    ? Math.round(attendance.slice(0, 30).reduce((s, r) => s + r.attendancePercentage, 0) / Math.min(attendance.length, 30))
    : 0

  if (loading) {
    return (
      <div>
        <div className="h-7 w-56 skeleton rounded mb-1" />
        <div className="h-4 w-72 skeleton rounded mb-6" />
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {[...Array(4)].map((_, i) => <CardSkeleton key={i} />)}
        </div>
      </div>
    )
  }

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Welcome, {user?.name?.split(' ')[0]} 👋</h1>
          <p className="page-subtitle">
            {user?.school?.name || 'Your School'} •{' '}
            {format(new Date(), 'EEEE, dd MMMM yyyy')}
          </p>
        </div>
      </div>

      {/* Alert banners */}
      <div className="space-y-2 mb-6">
        {!todaySubmitted && (
          <div className="flex items-center gap-3 bg-amber-50 border border-amber-200 rounded-xl px-4 py-3">
            <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0" />
            <div className="flex-1 text-sm text-amber-800">
              <span className="font-semibold">Attendance pending!</span> You haven't submitted today's attendance yet.
            </div>
            <Link to="/headmaster/attendance" className="btn-sm btn text-amber-700 bg-amber-100 hover:bg-amber-200 flex-shrink-0">
              Submit Now <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
        )}
        {unreadGr > 0 && (
          <div className="flex items-center gap-3 bg-blue-50 border border-blue-200 rounded-xl px-4 py-3">
            <FileText className="w-5 h-5 text-blue-600 flex-shrink-0" />
            <span className="text-sm text-blue-800 flex-1">
              <span className="font-semibold">{unreadGr} unread GR document{unreadGr > 1 ? 's' : ''}</span> — please review them.
            </span>
            <Link to="/headmaster/gr-documents" className="btn-sm btn text-blue-700 bg-blue-100 hover:bg-blue-200 flex-shrink-0">
              View <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
        )}
        {pendingForms > 0 && (
          <div className="flex items-center gap-3 bg-purple-50 border border-purple-200 rounded-xl px-4 py-3">
            <ClipboardList className="w-5 h-5 text-purple-600 flex-shrink-0" />
            <span className="text-sm text-purple-800 flex-1">
              <span className="font-semibold">{pendingForms} form{pendingForms > 1 ? 's' : ''}</span> waiting for your response.
            </span>
            <Link to="/headmaster/forms" className="btn-sm btn text-purple-700 bg-purple-100 hover:bg-purple-200 flex-shrink-0">
              Fill Now <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard icon={TrendingUp} label="Avg Attendance"
          value={`${avgAttendance}%`} sub="Last 30 days" color="blue" />
        <StatCard icon={CalendarCheck2} label="Today"
          value={todaySubmitted ? 'Done ✓' : 'Pending'}
          sub="Attendance status"
          color={todaySubmitted ? 'green' : 'orange'} />
        <StatCard icon={FileText} label="Unread GRs"
          value={unreadGr} sub="Documents to review" color="purple" />
        <StatCard icon={ClipboardList} label="Pending Forms"
          value={pendingForms} sub="Need your response" color="red" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upcoming meetings */}
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-900">Upcoming Meetings</h2>
            <Link to="/headmaster/meetings" className="text-xs text-primary-600 hover:underline font-medium">View all</Link>
          </div>
          {meetings.length === 0 ? (
            <p className="text-sm text-gray-400 text-center py-6">No upcoming meetings scheduled</p>
          ) : (
            <div className="space-y-3">
              {meetings.slice(0, 4).map(m => (
                <div key={m.id} className="flex items-center gap-3 p-3 rounded-xl bg-gray-50">
                  <div className={clsx('w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0',
                    m.meetingType === 'ONLINE' ? 'bg-blue-100' : 'bg-purple-100')}>
                    <CalendarDays className={clsx('w-4 h-4',
                      m.meetingType === 'ONLINE' ? 'text-blue-600' : 'text-purple-600')} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{m.title}</p>
                    <p className="text-xs text-gray-400">
                      {m.scheduledAt && format(new Date(m.scheduledAt), 'dd MMM, hh:mm a')}
                    </p>
                  </div>
                  {m.acknowledgedByCurrentUser
                    ? <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0" />
                    : <Clock className="w-4 h-4 text-amber-400 flex-shrink-0" />
                  }
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent GR docs */}
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-900">Recent GR Documents</h2>
            <Link to="/headmaster/gr-documents" className="text-xs text-primary-600 hover:underline font-medium">View all</Link>
          </div>
          {grDocs.length === 0 ? (
            <p className="text-sm text-gray-400 text-center py-6">No GR documents yet</p>
          ) : (
            <div className="space-y-3">
              {grDocs.slice(0, 4).map(d => (
                <div key={d.id} className="flex items-center gap-3 p-3 rounded-xl bg-gray-50">
                  <div className="w-9 h-9 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                    <FileText className="w-4 h-4 text-blue-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{d.title}</p>
                    <p className="text-xs text-gray-400">GR #{d.grNumber}</p>
                  </div>
                  {d.seenByCurrentUser
                    ? <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0" />
                    : <div className="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0" />
                  }
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent attendance */}
        <div className="card p-5 lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-900">Recent Attendance</h2>
            <Link to="/headmaster/attendance" className="text-xs text-primary-600 hover:underline font-medium">Submit / View</Link>
          </div>
          {attendance.length === 0 ? (
            <div className="text-center py-6">
              <p className="text-sm text-gray-400">No attendance records yet</p>
              <Link to="/headmaster/attendance" className="btn-primary btn-sm mt-3 inline-flex">
                Submit First Attendance
              </Link>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Total</th>
                    <th>Present</th>
                    <th>Absent</th>
                    <th>Attendance %</th>
                  </tr>
                </thead>
                <tbody>
                  {attendance.slice(0, 7).map(r => (
                    <tr key={r.id}>
                      <td>{format(new Date(r.attendanceDate), 'EEE, dd MMM yyyy')}</td>
                      <td>{r.totalStudents}</td>
                      <td className="text-green-600 font-medium">{r.presentStudents}</td>
                      <td className="text-red-500">{r.absentStudents}</td>
                      <td>
                        <div className="flex items-center gap-2">
                          <div className="flex-1 max-w-[80px] h-1.5 bg-gray-200 rounded-full overflow-hidden">
                            <div
                              className={clsx('h-full rounded-full',
                                r.attendancePercentage >= 80 ? 'bg-green-500' :
                                r.attendancePercentage >= 60 ? 'bg-yellow-500' : 'bg-red-500')}
                              style={{ width: `${r.attendancePercentage}%` }}
                            />
                          </div>
                          <span className="text-xs font-medium text-gray-700">
                            {Math.round(r.attendancePercentage)}%
                          </span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
