import { useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { useLanguage } from '../../context/LanguageContext'
import { authApi } from '../../services/api'
import { useForm } from 'react-hook-form'
import { User, Lock, ShieldCheck, Mail, Shield, KeyRound, CheckCircle2 } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AdminProfilePage() {
  const { user } = useAuth()
  const { lang } = useLanguage()
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

  return (
    <div className="page-transition max-w-4xl mx-auto space-y-6">
      <div className="page-header">
        <div>
          <h1 className="page-title">{lang === 'mr' ? 'माझी माहिती व खाते' : 'Admin Profile & Account'}</h1>
          <p className="page-subtitle">
            {lang === 'mr'
              ? 'प्रशासक खाते माहिती आणि सुरक्षितता व्यवस्थापन'
              : 'View administrator details, authority scope, and manage password security'}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Admin profile card */}
        <div className="card p-6 md:col-span-1 flex flex-col items-center text-center">
          <div className="w-20 h-20 rounded-full bg-purple-100 text-purple-700 flex items-center justify-center text-2xl font-bold mb-4 shadow-sm">
            {user?.name?.[0]?.toUpperCase()}
          </div>
          <h2 className="text-lg font-bold text-gray-900">{user?.name}</h2>
          <p className="text-xs text-gray-500 mb-3">{user?.email}</p>
          <span className="badge badge-purple mb-4">
            {lang === 'mr' ? 'केंद्र प्रमुख (प्रशासक)' : 'Cluster Head (Admin)'}
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
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-purple-500 flex-shrink-0" />
              <span>{lang === 'mr' ? 'पूर्ण प्रशासकीय अधिकार' : 'Full Cluster Privileges'}</span>
            </div>
          </div>
        </div>

        {/* Administration scope details */}
        <div className="card p-6 md:col-span-2 space-y-4">
          <div className="flex items-center gap-3 pb-3 border-b border-gray-100">
            <div className="w-9 h-9 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center">
              <KeyRound className="w-5 h-5" />
            </div>
            <div>
              <h2 className="font-semibold text-gray-900 text-base">
                {lang === 'mr' ? 'प्रशासक भूमिका व जबाबदाऱ्या' : 'Administrative Scope & Security'}
              </h2>
              <p className="text-xs text-gray-400">
                {lang === 'mr'
                  ? 'केंद्र प्रमुख अधिकार क्षेत्र व व्यवस्थापन नियंत्रण'
                  : 'Cluster Resource Center governance & account safety guidelines'}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div className="p-3 bg-purple-50/50 rounded-xl border border-purple-100/60">
              <div className="font-semibold text-purple-900 mb-1 flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-purple-600" />
                {lang === 'mr' ? 'शाळा व शिक्षक नियंत्रण' : 'Schools & Staff'}
              </div>
              <p className="text-purple-700 leading-relaxed">
                {lang === 'mr'
                  ? 'केंद्रातील सर्व शाळा व्यवस्थापन, मुख्याध्यापक खाते वाटप व नियंत्रण.'
                  : 'Full jurisdiction over cluster schools, headmaster accounts, and staff records.'}
              </p>
            </div>

            <div className="p-3 bg-blue-50/50 rounded-xl border border-blue-100/60">
              <div className="font-semibold text-blue-900 mb-1 flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-blue-600" />
                {lang === 'mr' ? 'अहवाल व उपस्थिती' : 'Reports & Governance'}
              </div>
              <p className="text-blue-700 leading-relaxed">
                {lang === 'mr'
                  ? 'दैनिक उपस्थिती निरीक्षण, BEO मासिक अहवाल निर्यात व शासन निर्णय.'
                  : 'Daily attendance monitoring, official BEO monthly Excel exports, and GR publishing.'}
              </p>
            </div>
          </div>

          <div className="p-4 bg-amber-50 rounded-xl border border-amber-200 text-amber-800 text-xs leading-relaxed">
            <span className="font-semibold">
              {lang === 'mr' ? 'सुरक्षा सूचना: ' : 'Security Recommendation: '}
            </span>
            {lang === 'mr'
              ? 'प्रशासक खात्यास उच्च अधिकार असल्याने आपला पासवर्ड कोणाशीही सामायिक करू नका. नियमित अंतराने नवीन पासवर्ड सेट करा.'
              : 'As this account holds high-level administrative access to all schools in the cluster, please use a strong, unique password and update it periodically.'}
          </div>
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
              {lang === 'mr' ? 'सुरक्षिततेसाठी आपला प्रशासक पासवर्ड वेळोवेळी बदला' : 'Keep your administrative account secure with a strong password'}
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
