import { useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { useLanguage } from '../../context/LanguageContext'
import { authApi } from '../../services/api'
import { useForm } from 'react-hook-form'
import { User, School, Lock, ShieldCheck, Mail, Building2, MapPin, Users, Phone } from 'lucide-react'
import toast from 'react-hot-toast'

export default function HeadmasterProfilePage() {
  const { user } = useAuth()
  const { t, lang } = useLanguage()
  const [changingPass, setChangingPass] = useState(false)

  const { register, handleSubmit, reset, formState: { errors } } = useForm()

  const onPasswordSubmit = async (data) => {
    if (data.newPassword !== data.confirmPassword) {
      toast.error(lang === 'mr' ? 'नवीन पासवर्ड आणि खात्री पासवर्ड जुळत नाहीत' : 'New passwords do not match')
      return
    }
    setChangingPass(true)
    try {
      await authApi.changePassword({
        currentPassword: data.currentPassword,
        newPassword: data.newPassword,
      })
      toast.success(lang === 'mr' ? 'पासवर्ड यशस्वीरित्या बदलला' : 'Password changed successfully')
      reset()
    } catch (err) {
      toast.error(err.response?.data?.message || (lang === 'mr' ? 'पासवर्ड बदलण्यात त्रुटी' : 'Failed to change password'))
    } finally {
      setChangingPass(false)
    }
  }

  const school = user?.school

  return (
    <div className="page-transition max-w-4xl mx-auto space-y-6">
      <div className="page-header">
        <div>
          <h1 className="page-title">{lang === 'mr' ? 'माझी माहिती व खाते' : 'Profile & Account'}</h1>
          <p className="page-subtitle">
            {lang === 'mr'
              ? 'आपली वैयक्तिक माहिती, नियुक्त शाळा आणि सुरक्षा व्यवस्थापन'
              : 'View personal details, assigned school, and manage password'}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* User profile card */}
        <div className="card p-6 md:col-span-1 flex flex-col items-center text-center">
          <div className="w-20 h-20 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center text-2xl font-bold mb-4 shadow-sm">
            {user?.name?.[0]?.toUpperCase()}
          </div>
          <h2 className="text-lg font-bold text-gray-900">{user?.name}</h2>
          <p className="text-xs text-gray-500 mb-3">{user?.email}</p>
          <span className="badge badge-purple mb-4">
            {lang === 'mr' ? 'शाळा मुख्याध्यापक' : 'School Headmaster'}
          </span>
          <div className="w-full border-t border-gray-100 pt-4 text-left space-y-2.5 text-xs text-gray-600">
            <div className="flex items-center gap-2">
              <Mail className="w-4 h-4 text-gray-400 flex-shrink-0" />
              <span className="truncate">{user?.email}</span>
            </div>
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-green-500 flex-shrink-0" />
              <span>{lang === 'mr' ? 'सक्रिय खाते' : 'Active Account'}</span>
            </div>
          </div>
        </div>

        {/* Assigned School Details */}
        <div className="card p-6 md:col-span-2">
          <div className="flex items-center gap-3 mb-4 pb-3 border-b border-gray-100">
            <div className="w-9 h-9 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <School className="w-5 h-5" />
            </div>
            <div>
              <h2 className="font-semibold text-gray-900 text-base">
                {lang === 'mr' ? 'नियुक्त शाळा माहिती' : 'Assigned School Information'}
              </h2>
              <p className="text-xs text-gray-400">
                {lang === 'mr' ? 'केंद्राकडून जोडण्यात आलेली शाळा' : 'School linked to your headmaster account'}
              </p>
            </div>
          </div>

          {school ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
              <div className="bg-gray-50/70 p-3.5 rounded-xl border border-gray-100">
                <span className="text-xs font-medium text-gray-400 block mb-1">
                  {lang === 'mr' ? 'शाळेचे नाव' : 'School Name'}
                </span>
                <span className="font-semibold text-gray-900">{school.name}</span>
              </div>
              <div className="bg-gray-50/70 p-3.5 rounded-xl border border-gray-100">
                <span className="text-xs font-medium text-gray-400 block mb-1">
                  {lang === 'mr' ? 'यु-डायस कोड' : 'UDISE Code'}
                </span>
                <span className="font-semibold font-mono text-gray-900">{school.udiseCode}</span>
              </div>
              <div className="bg-gray-50/70 p-3.5 rounded-xl border border-gray-100">
                <span className="text-xs font-medium text-gray-400 block mb-1">
                  {lang === 'mr' ? 'गाव / परिसर' : 'Village / Location'}
                </span>
                <span className="text-gray-800 flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-gray-400" />
                  {school.village || '—'}, {school.taluka || '—'}
                </span>
              </div>
              <div className="bg-gray-50/70 p-3.5 rounded-xl border border-gray-100">
                <span className="text-xs font-medium text-gray-400 block mb-1">
                  {lang === 'mr' ? 'विद्यार्थी व शिक्षक' : 'Students & Teachers'}
                </span>
                <span className="text-gray-800 flex items-center gap-1.5">
                  <Users className="w-3.5 h-3.5 text-gray-400" />
                  {school.totalStudents || 0} {lang === 'mr' ? 'विद्यार्थी' : 'students'} / {school.totalTeachers || 0} {lang === 'mr' ? 'शिक्षक' : 'teachers'}
                </span>
              </div>
            </div>
          ) : (
            <div className="p-6 text-center bg-amber-50 rounded-xl border border-amber-200 text-amber-800 text-sm">
              {lang === 'mr'
                ? 'आपल्या खात्यास अद्याप कोणतीही शाळा जोडलेली नाही. कृपया केंद्र प्रमुख (प्रशासक) यांच्याशी संपर्क साधा.'
                : 'No school has been assigned to your account yet. Please contact the cluster admin.'}
            </div>
          )}
        </div>
      </div>

      {/* Change password card */}
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-5 pb-3 border-b border-gray-100">
          <div className="w-9 h-9 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center">
            <Lock className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-semibold text-gray-900 text-base">
              {lang === 'mr' ? 'पासवर्ड बदला' : 'Change Password'}
            </h2>
            <p className="text-xs text-gray-400">
              {lang === 'mr' ? 'सुरक्षिततेसाठी आपला पासवर्ड वेळोवेळी बदला' : 'Keep your account secure with a strong password'}
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onPasswordSubmit)} className="space-y-4 max-w-md">
          <div>
            <label className="form-label">{lang === 'mr' ? 'सध्याचा पासवर्ड' : 'Current Password'}</label>
            <input
              type="password"
              {...register('currentPassword', { required: 'Current password is required' })}
              className="form-input"
              placeholder="••••••••"
            />
            {errors.currentPassword && (
              <p className="form-error">{errors.currentPassword.message}</p>
            )}
          </div>

          <div>
            <label className="form-label">{lang === 'mr' ? 'नवीन पासवर्ड' : 'New Password'}</label>
            <input
              type="password"
              {...register('newPassword', {
                required: 'New password is required',
                minLength: { value: 6, message: 'Password must be at least 6 characters' }
              })}
              className="form-input"
              placeholder="••••••••"
            />
            {errors.newPassword && (
              <p className="form-error">{errors.newPassword.message}</p>
            )}
          </div>

          <div>
            <label className="form-label">{lang === 'mr' ? 'नवीन पासवर्ड खात्री करा' : 'Confirm New Password'}</label>
            <input
              type="password"
              {...register('confirmPassword', { required: 'Please confirm password' })}
              className="form-input"
              placeholder="••••••••"
            />
            {errors.confirmPassword && (
              <p className="form-error">{errors.confirmPassword.message}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={changingPass}
            className="btn-primary"
          >
            {changingPass
              ? (lang === 'mr' ? 'बदलत आहे...' : 'Updating...')
              : (lang === 'mr' ? 'पासवर्ड अपडेट करा' : 'Update Password')}
          </button>
        </form>
      </div>
    </div>
  )
}
