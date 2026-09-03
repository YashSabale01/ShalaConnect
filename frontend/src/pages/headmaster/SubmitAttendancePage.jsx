import { useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { attendanceApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import { useForm } from 'react-hook-form'
import EmptyState from '../../components/ui/EmptyState'
import { TableSkeleton } from '../../components/ui/Skeleton'
import {
  CalendarCheck2, Send, CheckCircle2, AlertCircle, Building2
} from 'lucide-react'
import { format } from 'date-fns'
import toast from 'react-hot-toast'
import clsx from 'clsx'

export default function SubmitAttendancePage() {
  const { user } = useAuth()
  const { data: records, loading, refetch } = useApi(
    () => user?.school?.id
      ? attendanceApi.getBySchool(user.school.id)
      : Promise.resolve({ data: { data: [] } }),
    [user?.school?.id]
  )
  const [submitting, setSubmitting] = useState(false)

  const { register, handleSubmit, watch, reset, formState: { errors } } = useForm({
    defaultValues: {
      attendanceDate: format(new Date(), 'yyyy-MM-dd'),
      totalStudents: user?.school ? '' : '',
    }
  })

  const today = new Date().toLocaleDateString('en-CA') // yyyy-MM-dd in local timezone
  const alreadySubmittedToday = (records || []).some(r => r.attendanceDate === today)

  const totalStudents = parseInt(watch('totalStudents')) || 0
  const presentStudents = parseInt(watch('presentStudents')) || 0
  const absentStudents = totalStudents - presentStudents
  const attendancePct = totalStudents > 0 ? Math.round((presentStudents / totalStudents) * 100) : 0

  const onSubmit = async (data) => {
    if (!user?.school?.id) {
      toast.error('No school assigned to your account. Please contact admin.')
      return
    }
    if (parseInt(data.presentStudents) > parseInt(data.totalStudents)) {
      toast.error('Present students cannot exceed total students')
      return
    }
    setSubmitting(true)
    try {
      await attendanceApi.submit({
        ...data,
        schoolId: user.school.id,
        totalStudents: parseInt(data.totalStudents),
        presentStudents: parseInt(data.presentStudents),
        totalTeachers: data.totalTeachers ? parseInt(data.totalTeachers) : null,
        presentTeachers: data.presentTeachers ? parseInt(data.presentTeachers) : null,
      })
      toast.success('Attendance submitted successfully!')
      reset({ attendanceDate: format(new Date(), 'yyyy-MM-dd') })
      refetch()
    } catch (err) {
      toast.error(err.response?.data?.message || 'Failed to submit attendance')
    } finally {
      setSubmitting(false)
    }
  }

  if (!user?.school) {
    return (
      <EmptyState
        icon={Building2}
        title="No school assigned"
        description="Your account is not linked to any school. Please contact the admin to assign a school to your account."
      />
    )
  }

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">Attendance</h1>
          <p className="page-subtitle">{user.school.name}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Submit form */}
        <div className="lg:col-span-2">
          <div className="card p-6">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center">
                <CalendarCheck2 className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h2 className="font-semibold text-gray-900">Submit Attendance</h2>
                <p className="text-xs text-gray-400">Fill in today's data</p>
              </div>
            </div>

            {alreadySubmittedToday && (
              <div className="mb-4 flex items-center gap-2.5 bg-green-50 border border-green-200 rounded-xl px-4 py-3">
                <CheckCircle2 className="w-4 h-4 text-green-600 flex-shrink-0" />
                <p className="text-sm text-green-700 font-medium">Today's attendance already submitted!</p>
              </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="form-group">
                <label className="label">Date *</label>
                <input type="date" className={`input ${errors.attendanceDate ? 'input-error' : ''}`}
                  max={today}
                  {...register('attendanceDate', { required: 'Date is required' })} />
                {errors.attendanceDate && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.attendanceDate.message}</p>}
              </div>

              <div className="p-3 bg-gray-50 rounded-xl space-y-3">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Students</p>
                <div className="grid grid-cols-2 gap-3">
                  <div className="form-group">
                    <label className="label">Total *</label>
                    <input type="number" min="0" className={`input ${errors.totalStudents ? 'input-error' : ''}`}
                      placeholder="0"
                      {...register('totalStudents', { required: 'Required', min: { value: 1, message: 'Must be > 0' } })} />
                    {errors.totalStudents && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.totalStudents.message}</p>}
                  </div>
                  <div className="form-group">
                    <label className="label">Present *</label>
                    <input type="number" min="0" className={`input ${errors.presentStudents ? 'input-error' : ''}`}
                      placeholder="0"
                      {...register('presentStudents', {
                        required: 'Required',
                        validate: v => parseInt(v) <= totalStudents || 'Cannot exceed total'
                      })} />
                    {errors.presentStudents && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.presentStudents.message}</p>}
                  </div>
                </div>
              </div>

              <div className="p-3 bg-gray-50 rounded-xl space-y-3">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Teachers (Optional)</p>
                <div className="grid grid-cols-2 gap-3">
                  <div className="form-group">
                    <label className="label">Total</label>
                    <input type="number" min="0" className="input" placeholder="0"
                      {...register('totalTeachers')} />
                  </div>
                  <div className="form-group">
                    <label className="label">Present</label>
                    <input type="number" min="0" className="input" placeholder="0"
                      {...register('presentTeachers')} />
                  </div>
                </div>
              </div>

              {/* Live preview */}
              {totalStudents > 0 && (
                <div className="p-3 bg-blue-50 rounded-xl">
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">Absent: <strong className="text-red-500">{absentStudents < 0 ? '—' : absentStudents}</strong></span>
                    <span className="font-semibold text-primary-700">{attendancePct}%</span>
                  </div>
                  <div className="h-2 bg-blue-200 rounded-full overflow-hidden">
                    <div
                      className={clsx('h-full rounded-full transition-all duration-300',
                        attendancePct >= 80 ? 'bg-green-500' :
                        attendancePct >= 60 ? 'bg-yellow-500' : 'bg-red-500')}
                      style={{ width: `${Math.min(attendancePct, 100)}%` }}
                    />
                  </div>
                </div>
              )}

              <div className="form-group">
                <label className="label">Remarks (Optional)</label>
                <textarea className="input" rows={2} placeholder="Any notes about today's attendance…"
                  {...register('remarks')} />
              </div>

              <button type="submit" disabled={submitting} className="btn-primary w-full">
                {submitting ? 'Submitting…' : <><Send className="w-4 h-4" />Submit Attendance</>}
              </button>
            </form>
          </div>
        </div>

        {/* History table */}
        <div className="lg:col-span-3">
          <div className="card">
            <div className="p-5 border-b border-gray-100">
              <h2 className="font-semibold text-gray-900">Attendance History</h2>
              <p className="text-xs text-gray-400 mt-0.5">Previous submissions for {user.school.name}</p>
            </div>
            {loading ? <TableSkeleton rows={6} cols={5} /> : (records || []).length === 0 ? (
              <div className="py-12 text-center">
                <CalendarCheck2 className="w-10 h-10 text-gray-300 mx-auto mb-2" />
                <p className="text-sm text-gray-400">No attendance records yet</p>
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
                      <th>%</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(records || []).map(r => (
                      <tr key={r.id}>
                        <td>
                          <div className="flex items-center gap-1.5">
                            {r.attendanceDate === today && (
                              <span className="badge badge-green text-[10px] px-1.5 py-0">Today</span>
                            )}
                            <span>{format(new Date(r.attendanceDate), 'dd MMM yyyy')}</span>
                          </div>
                        </td>
                        <td>{r.totalStudents}</td>
                        <td className="text-green-600 font-medium">{r.presentStudents}</td>
                        <td className="text-red-500">{r.absentStudents}</td>
                        <td>
                          <span className={clsx('font-semibold text-sm',
                            r.attendancePercentage >= 80 ? 'text-green-600' :
                            r.attendancePercentage >= 60 ? 'text-yellow-600' : 'text-red-500')}>
                            {Math.round(r.attendancePercentage)}%
                          </span>
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
    </div>
  )
}
