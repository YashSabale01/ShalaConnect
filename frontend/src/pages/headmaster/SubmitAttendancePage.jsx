import { useState, useEffect } from 'react'
import { useAuth } from '../../context/AuthContext'
import { useLanguage } from '../../context/LanguageContext'
import { attendanceApi } from '../../services/api'
import { useApi } from '../../hooks/useApi'
import { useForm } from 'react-hook-form'
import EmptyState from '../../components/ui/EmptyState'
import { TableSkeleton } from '../../components/ui/Skeleton'
import {
  CalendarCheck2, Send, CheckCircle2, AlertCircle, Building2, WifiOff, RefreshCw
} from 'lucide-react'
import { format } from 'date-fns'
import toast from 'react-hot-toast'
import clsx from 'clsx'

export default function SubmitAttendancePage() {
  const { user } = useAuth()
  const { t, lang } = useLanguage()
  const { data: records, loading, refetch } = useApi(
    () => user?.school?.id
      ? attendanceApi.getBySchool(user.school.id)
      : Promise.resolve({ data: { data: [] } }),
    [user?.school?.id]
  )
  const [submitting, setSubmitting] = useState(false)
  const [isOnline, setIsOnline] = useState(navigator.onLine)
  const [offlineCount, setOfflineCount] = useState(() => {
    try {
      const q = JSON.parse(localStorage.getItem('offline_attendance_queue') || '[]')
      return q.length
    } catch { return 0 }
  })

  const { register, handleSubmit, watch, reset, formState: { errors } } = useForm({
    defaultValues: {
      attendanceDate: format(new Date(), 'yyyy-MM-dd'),
      totalStudents: user?.school?.totalStudents ? String(user.school.totalStudents) : '',
      totalTeachers: user?.school?.totalTeachers ? String(user.school.totalTeachers) : '',
    }
  })

  // Auto-sync offline queue when internet connection restores
  const syncOfflineQueue = async () => {
    try {
      const raw = localStorage.getItem('offline_attendance_queue')
      if (!raw) return
      const queue = JSON.parse(raw)
      if (!Array.isArray(queue) || queue.length === 0) return

      toast.loading(t('syncingOffline'), { id: 'offline-sync' })
      const remaining = []

      for (const item of queue) {
        try {
          await attendanceApi.submit(item)
        } catch (err) {
          // If already submitted, ignore duplicate error
          if (!err.response?.data?.message?.includes('already submitted')) {
            remaining.push(item)
          }
        }
      }

      localStorage.setItem('offline_attendance_queue', JSON.stringify(remaining))
      setOfflineCount(remaining.length)
      toast.success(t('offlineSyncSuccess'), { id: 'offline-sync' })
      refetch()
    } catch {
      toast.dismiss('offline-sync')
    }
  }

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true)
      syncOfflineQueue()
    }
    const handleOffline = () => setIsOnline(false)

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  const today = new Date().toLocaleDateString('en-CA')
  const alreadySubmittedToday = (records || []).some(r => {
    const d = r.attendanceDate
    if (!d) return false
    if (typeof d === 'string') return d.slice(0, 10) === today
    return new Date(d).toLocaleDateString('en-CA') === today
  })

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
      toast.error(lang === 'mr' ? 'उपस्थित विद्यार्थी एकूण विद्यार्थ्यांपेक्षा जास्त असू शकत नाहीत' : 'Present students cannot exceed total students')
      return
    }

    const payload = {
      ...data,
      schoolId: user.school.id,
      totalStudents: parseInt(data.totalStudents),
      presentStudents: parseInt(data.presentStudents),
      totalTeachers: data.totalTeachers ? parseInt(data.totalTeachers) : null,
      presentTeachers: data.presentTeachers ? parseInt(data.presentTeachers) : null,
    }

    // If offline, store in offline queue
    if (!navigator.onLine) {
      const q = JSON.parse(localStorage.getItem('offline_attendance_queue') || '[]')
      q.push(payload)
      localStorage.setItem('offline_attendance_queue', JSON.stringify(q))
      setOfflineCount(q.length)
      toast.success(t('offlineMode'), { duration: 5000 })
      reset({ attendanceDate: format(new Date(), 'yyyy-MM-dd') })
      return
    }

    setSubmitting(true)
    try {
      await attendanceApi.submit(payload)
      toast.success(lang === 'mr' ? 'उपस्थिती यशस्वीरित्या नोंद झाली!' : 'Attendance submitted successfully!')
      reset({ attendanceDate: format(new Date(), 'yyyy-MM-dd') })
      refetch()
    } catch (err) {
      // If network failure during submission, offer offline save
      if (!err.response) {
        const q = JSON.parse(localStorage.getItem('offline_attendance_queue') || '[]')
        q.push(payload)
        localStorage.setItem('offline_attendance_queue', JSON.stringify(q))
        setOfflineCount(q.length)
        toast.success(t('offlineMode'))
      } else {
        toast.error(err.response?.data?.message || 'Failed to submit attendance')
      }
    } finally {
      setSubmitting(false)
    }
  }

  if (!user?.school) {
    return (
      <EmptyState
        icon={Building2}
        title={lang === 'mr' ? 'कोणतीही शाळा नियुक्त नाही' : 'No school assigned'}
        description={lang === 'mr' ? 'आपल्या खात्यास अद्याप कोणतीही शाळा जोडलेली नाही. कृपया केंद्र प्रमुखांशी संपर्क साधा.' : 'Your account is not linked to any school. Please contact the admin.'}
      />
    )
  }

  return (
    <div className="page-transition">
      <div className="page-header">
        <div>
          <h1 className="page-title">{t('attendance')}</h1>
          <p className="page-subtitle">{user.school.name}</p>
        </div>
        {/* Offline status badge */}
        {(!isOnline || offlineCount > 0) && (
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-semibold">
            <WifiOff className="w-3.5 h-3.5 text-amber-600" />
            <span>{!isOnline ? 'Offline' : `${offlineCount} pending sync`}</span>
            {isOnline && offlineCount > 0 && (
              <button onClick={syncOfflineQueue} className="ml-1 text-primary-600 underline hover:text-primary-700">
                Sync Now
              </button>
            )}
          </div>
        )}
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
                <h2 className="font-semibold text-gray-900">{t('submitAttendanceTitle')}</h2>
                <p className="text-xs text-gray-400">{user.school.village || user.school.name}</p>
              </div>
            </div>

            {alreadySubmittedToday && (
              <div className="mb-4 flex items-center gap-2.5 bg-green-50 border border-green-200 rounded-xl px-4 py-3">
                <CheckCircle2 className="w-4 h-4 text-green-600 flex-shrink-0" />
                <p className="text-sm text-green-700 font-medium">
                  {lang === 'mr' ? 'आजची उपस्थिती आधीच नोंदवली आहे!' : "Today's attendance already submitted!"}
                </p>
              </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="form-group">
                <label className="label">{lang === 'mr' ? 'दिनांक *' : 'Date *'}</label>
                <input type="date" className={`input ${errors.attendanceDate ? 'input-error' : ''}`}
                  max={today}
                  {...register('attendanceDate', { required: 'Date is required' })} />
                {errors.attendanceDate && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.attendanceDate.message}</p>}
              </div>

              <div className="p-3 bg-gray-50 rounded-xl space-y-3">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  {lang === 'mr' ? 'विद्यार्थी उपस्थिती' : 'Students'}
                </p>
                <div className="grid grid-cols-2 gap-3">
                  <div className="form-group">
                    <label className="label">{t('totalStudents')} *</label>
                    <input type="number" min="0" className={`input ${errors.totalStudents ? 'input-error' : ''}`}
                      placeholder="0"
                      {...register('totalStudents', { required: 'Required', min: { value: 1, message: 'Must be > 0' } })} />
                    {errors.totalStudents && <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.totalStudents.message}</p>}
                  </div>
                  <div className="form-group">
                    <label className="label">{t('presentStudents')} *</label>
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
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  {lang === 'mr' ? 'शिक्षक उपस्थिती' : 'Teachers (Optional)'}
                </p>
                <div className="grid grid-cols-2 gap-3">
                  <div className="form-group">
                    <label className="label">{t('totalTeachers')}</label>
                    <input type="number" min="0" className="input" placeholder="0"
                      {...register('totalTeachers')} />
                  </div>
                  <div className="form-group">
                    <label className="label">{t('presentTeachers')}</label>
                    <input type="number" min="0" className="input" placeholder="0"
                      {...register('presentTeachers')} />
                  </div>
                </div>
              </div>

              {/* Live preview */}
              {totalStudents > 0 && (
                <div className="p-3 bg-blue-50 rounded-xl">
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">{t('absentStudents')}: <strong className="text-red-500">{absentStudents < 0 ? '—' : absentStudents}</strong></span>
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
                <label className="label">{t('remarks')}</label>
                <textarea className="input" rows={2} placeholder="Any notes about today's attendance…"
                  {...register('remarks')} />
              </div>

              <button type="submit" disabled={submitting} className="btn-primary w-full">
                {submitting ? t('submittingBtn') : <><Send className="w-4 h-4" />{t('submitBtn')}</>}
              </button>
            </form>
          </div>
        </div>

        {/* History table */}
        <div className="lg:col-span-3">
          <div className="card">
            <div className="p-5 border-b border-gray-100">
              <h2 className="font-semibold text-gray-900">
                {lang === 'mr' ? 'मागील उपस्थिती इतिहास' : 'Attendance History'}
              </h2>
              <p className="text-xs text-gray-400 mt-0.5">{user.school.name}</p>
            </div>
            {loading ? <TableSkeleton rows={6} cols={5} /> : (records || []).length === 0 ? (
              <div className="py-12 text-center">
                <CalendarCheck2 className="w-10 h-10 text-gray-300 mx-auto mb-2" />
                <p className="text-sm text-gray-400">{t('noData')}</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="table">
                  <thead>
                    <tr>
                      <th>{lang === 'mr' ? 'दिनांक' : 'Date'}</th>
                      <th>{lang === 'mr' ? 'एकूण' : 'Total'}</th>
                      <th>{lang === 'mr' ? 'उपस्थित' : 'Present'}</th>
                      <th>{lang === 'mr' ? 'अनुपस्थित' : 'Absent'}</th>
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
