import { useState, useEffect } from 'react'
import { attendanceApi, schoolApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import StatCard from '../../components/ui/StatCard'
import EmptyState from '../../components/ui/EmptyState'
import { TableSkeleton } from '../../components/ui/Skeleton'
import {
  CalendarCheck2, TrendingUp, CheckCircle2, XCircle, AlertCircle
} from 'lucide-react'
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer,
  CartesianGrid, Legend
} from 'recharts'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function AttendancePage() {
  const { data: summary, loading: summaryLoading, refetch } = useApi(() => attendanceApi.getSummary())
  const { data: schools } = useApi(() => schoolApi.getAll())
  const [selectedSchool, setSelectedSchool] = useState('')
  const [chartData, setChartData] = useState([])
  const [chartLoading, setChartLoading] = useState(false)
  const [selectedDate, setSelectedDate] = useState(format(new Date(), 'yyyy-MM-dd'))

  useEffect(() => {
    if (!selectedSchool) return
    setChartLoading(true)
    const end = format(new Date(), 'yyyy-MM-dd')
    const start = format(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd')
    attendanceApi.getByRange(selectedSchool, start, end).then(res => {
      setChartData(res.data.data?.map(r => ({
        date: format(new Date(r.attendanceDate), 'dd MMM'),
        attendance: Math.round(r.attendancePercentage),
        present: r.presentStudents,
        total: r.totalStudents,
      })) || [])
    }).finally(() => setChartLoading(false))
  }, [selectedSchool])

  const todayRecords = summary?.todayRecords || []
  const totalSchools = schools?.length || 0
  const submittedToday = summary?.submittedToday || 0

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Attendance Overview</h1>
          <p className="page-subtitle">Monitor daily attendance across all schools</p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <StatCard icon={CalendarCheck2} label="Submitted Today"
          value={`${submittedToday}/${totalSchools}`}
          sub="Schools reported" color="blue" />
        <StatCard icon={TrendingUp} label="Avg Today"
          value={`${summary?.avgAttendanceToday || 0}%`}
          sub="Average attendance" color="green" />
        <StatCard icon={TrendingUp} label="Avg This Month"
          value={`${summary?.avgAttendanceMonth || 0}%`}
          sub="30-day average" color="purple" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Today's status table */}
        <div className="card">
          <div className="p-5 border-b border-gray-100">
            <h2 className="font-semibold text-gray-900">Today's Submission Status</h2>
            <p className="text-xs text-gray-400 mt-0.5">{format(new Date(), 'dd MMMM yyyy')}</p>
          </div>
          {summaryLoading ? (
            <TableSkeleton rows={4} cols={3} />
          ) : (
            <div className="divide-y divide-gray-50 max-h-80 overflow-y-auto">
              {(schools || []).map(school => {
                const record = todayRecords.find(r => r.schoolId === school.id)
                return (
                  <div key={school.id} className="flex items-center gap-3 px-5 py-3">
                    {record
                      ? <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0" />
                      : <XCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
                    }
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">{school.name}</p>
                      {record && (
                        <p className="text-xs text-gray-400">
                          {record.presentStudents}/{record.totalStudents} students present ({Math.round(record.attendancePercentage)}%)
                        </p>
                      )}
                    </div>
                    <span className={clsx('badge', record ? 'badge-green' : 'badge-red')}>
                      {record ? 'Submitted' : 'Pending'}
                    </span>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* School chart */}
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-900">30-Day Trend</h2>
            <select
              className="input w-52 text-sm py-1.5"
              value={selectedSchool}
              onChange={e => setSelectedSchool(e.target.value)}
            >
              <option value="">Select a school…</option>
              {(schools || []).map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
            </select>
          </div>
          {!selectedSchool ? (
            <EmptyState
              icon={AlertCircle}
              title="Select a school"
              description="Choose a school to view its 30-day attendance trend"
              className="py-10"
            />
          ) : chartLoading ? (
            <div className="h-48 flex items-center justify-center">
              <div className="w-6 h-6 border-2 border-primary-600 border-t-transparent rounded-full animate-spin" />
            </div>
          ) : chartData.length === 0 ? (
            <EmptyState icon={CalendarCheck2} title="No attendance data" description="No records for this school in the last 30 days" className="py-10" />
          ) : (
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={chartData} margin={{ top: 4, right: 4, bottom: 4, left: -20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 10 }} />
                <Tooltip
                  formatter={(v, name) => [name === 'attendance' ? `${v}%` : v, name]}
                  contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb', fontSize: '12px' }}
                />
                <Line type="monotone" dataKey="attendance" stroke="#3b82f6" strokeWidth={2} dot={false} name="Attendance %" />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>
    </div>
  )
}
