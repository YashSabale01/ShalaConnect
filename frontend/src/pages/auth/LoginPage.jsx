import { useState } from 'react'
import { useNavigate, Navigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useAuth } from '../../context/AuthContext'
import { Eye, EyeOff, GraduationCap, Loader2, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'

export default function LoginPage() {
  const { login, user } = useAuth()
  const navigate = useNavigate()
  const [showPass, setShowPass] = useState(false)
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState('')

  const { register, handleSubmit, formState: { errors } } = useForm()

  if (user) {
    return <Navigate to={user.role === 'ADMIN' ? '/admin' : '/headmaster'} replace />
  }

  const onSubmit = async ({ email, password }) => {
    setLoading(true)
    setError('')
    try {
      const loggedUser = await login(email, password)
      toast.success(`Welcome back, ${loggedUser.name}!`)
      navigate(loggedUser.role === 'ADMIN' ? '/admin' : '/headmaster', { replace: true })
    } catch (err) {
      const msg = err.response?.data?.message || 'Invalid email or password'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-900 via-primary-800 to-primary-700 flex items-center justify-center p-4">
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-10"
        style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, white 1px, transparent 0)', backgroundSize: '32px 32px' }} />

      <div className="relative w-full max-w-md">
        {/* Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <GraduationCap className="w-9 h-9 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900">ShalaConnect</h1>
            <p className="text-gray-500 text-sm mt-1">शाळाकनेक्ट — School Management Portal</p>
          </div>

          {/* Error alert */}
          {error && (
            <div className="mb-4 flex items-center gap-2.5 bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm animate-fade-in">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              {error}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="form-group">
              <label className="label">Email Address</label>
              <input
                type="email"
                placeholder="you@shalaconnect.in"
                className={`input ${errors.email ? 'input-error' : ''}`}
                {...register('email', {
                  required: 'Email is required',
                  pattern: { value: /^\S+@\S+\.\S+$/, message: 'Enter a valid email' }
                })}
              />
              {errors.email && (
                <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.email.message}</p>
              )}
            </div>

            <div className="form-group">
              <label className="label">Password</label>
              <div className="relative">
                <input
                  type={showPass ? 'text' : 'password'}
                  placeholder="••••••••"
                  className={`input pr-10 ${errors.password ? 'input-error' : ''}`}
                  {...register('password', { required: 'Password is required' })}
                />
                <button
                  type="button"
                  onClick={() => setShowPass(!showPass)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPass ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              {errors.password && (
                <p className="error-message"><AlertCircle className="w-3 h-3" />{errors.password.message}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full btn-lg mt-2"
            >
              {loading ? (
                <><Loader2 className="w-4 h-4 animate-spin" /> Signing in…</>
              ) : 'Sign In'}
            </button>
          </form>

        </div>

        {/* Public portal link */}
        <div className="text-center mt-4">
          <a href="/" className="text-white/70 hover:text-white text-sm transition-colors">
            ← Visit Public Portal
          </a>
        </div>
      </div>
    </div>
  )
}
