import { useState } from 'react'
import { Outlet, NavLink, useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { useLanguage } from '../../context/LanguageContext'
import NotificationBell from '../ui/NotificationBell'
import {
  LayoutDashboard, School, CalendarCheck2, FileText, Users,
  BookOpen, CalendarDays, ClipboardList, Menu, X, LogOut,
  ChevronRight, GraduationCap, Building2, UserCircle, Globe
} from 'lucide-react'
import clsx from 'clsx'

export default function DashboardLayout({ role }) {
  const { user, logout } = useAuth()
  const { t, lang, toggleLanguage } = useLanguage()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const adminNav = [
    { to: '/admin',             icon: LayoutDashboard, label: t('dashboard'),    end: true },
    { to: '/admin/schools',     icon: Building2,       label: t('schools') },
    { to: '/admin/attendance',  icon: CalendarCheck2,  label: t('attendance') },
    { to: '/admin/gr-documents',icon: FileText,        label: t('grDocuments') },
    { to: '/admin/meetings',    icon: CalendarDays,    label: t('meetings') },
    { to: '/admin/events',      icon: BookOpen,        label: t('events') },
    { to: '/admin/forms',       icon: ClipboardList,   label: t('forms') },
    { to: '/admin/users',       icon: Users,           label: t('users') },
    { to: '/admin/profile',     icon: UserCircle,      label: t('profile') },
  ]

  const headmasterNav = [
    { to: '/headmaster',              icon: LayoutDashboard, label: t('dashboard'),    end: true },
    { to: '/headmaster/attendance',   icon: CalendarCheck2,  label: t('attendance') },
    { to: '/headmaster/gr-documents', icon: FileText,        label: t('grDocuments') },
    { to: '/headmaster/meetings',     icon: CalendarDays,    label: t('meetings') },
    { to: '/headmaster/forms',        icon: ClipboardList,   label: t('forms') },
    { to: '/headmaster/events',       icon: BookOpen,        label: t('events') },
    { to: '/headmaster/profile',      icon: UserCircle,      label: t('profile') },
  ]

  const nav = role === 'ADMIN' ? adminNav : headmasterNav

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const SidebarContent = () => (
    <div className="flex flex-col h-full bg-white">
      {/* Logo */}
      <div className="flex items-center gap-3 px-5 py-5 border-b border-gray-100">
        <div className="w-10 h-10 bg-primary-700 rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm">
          <GraduationCap className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="font-bold text-gray-900 text-sm tracking-tight leading-tight">ShalaConnect</div>
          <div className="text-[11px] font-medium text-amber-600">शाळाकनेक्ट पोर्टल</div>
        </div>
      </div>

      {/* Role badge */}
      <div className="px-5 py-3">
        <span className={clsx(
          'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold tracking-wide',
          role === 'ADMIN' ? 'bg-purple-50 text-purple-700 border border-purple-200' : 'bg-blue-50 text-blue-700 border border-blue-200'
        )}>
          <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
          {role === 'ADMIN' ? t('roleAdmin') : t('roleHeadmaster')}
        </span>
      </div>

      {/* Nav links */}
      <nav className="flex-1 px-3 py-2 space-y-1 overflow-y-auto">
        {nav.map(({ to, icon: Icon, label, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            onClick={() => setSidebarOpen(false)}
            className={({ isActive }) =>
              clsx('sidebar-link group rounded-xl transition-all', isActive ? 'sidebar-link-active shadow-sm font-semibold' : 'sidebar-link-inactive')
            }
          >
            {({ isActive }) => (
              <>
                <Icon className={clsx('w-4 h-4 flex-shrink-0 transition-colors',
                  isActive ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-600')} />
                <span className="flex-1 text-sm">{label}</span>
                {isActive && <ChevronRight className="w-3.5 h-3.5 text-primary-400" />}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* User section */}
      <div className="border-t border-gray-100 p-3 bg-gray-50/50">
        <Link
          to={role === 'ADMIN' ? '/admin/profile' : '/headmaster/profile'}
          onClick={() => setSidebarOpen(false)}
          className="flex items-center gap-3 px-2 py-2 rounded-lg mb-1 hover:bg-gray-100/70 transition-colors group"
          title={t('profile')}
        >
          <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0 text-primary-700 font-bold text-xs group-hover:scale-105 transition-transform">
            {user?.name?.[0]?.toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-semibold text-gray-900 truncate group-hover:text-primary-600 transition-colors">{user?.name}</div>
            <div className="text-xs text-gray-400 truncate">
              {role === 'HEADMASTER' && user?.school?.name ? user.school.name : user?.email}
            </div>
          </div>
        </Link>

        <button
          onClick={handleLogout}
          className="sidebar-link sidebar-link-inactive w-full text-red-600 hover:bg-red-50 hover:text-red-700 rounded-xl"
        >
          <LogOut className="w-4 h-4" />
          <span className="text-xs font-semibold">{t('logout')}</span>
        </button>
      </div>
    </div>
  )

  return (
    <div className="flex h-screen bg-slate-50/70 overflow-hidden font-sans">
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex flex-col w-64 bg-white border-r border-gray-100 flex-shrink-0 shadow-sm">
        <SidebarContent />
      </aside>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="lg:hidden fixed inset-0 z-40">
          <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity" onClick={() => setSidebarOpen(false)} />
          <aside className="relative w-72 h-full bg-white flex flex-col z-50 shadow-2xl">
            <button
              onClick={() => setSidebarOpen(false)}
              className="absolute top-4 right-4 p-1.5 rounded-lg text-gray-400 hover:bg-gray-100"
            >
              <X className="w-5 h-5" />
            </button>
            <SidebarContent />
          </aside>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Topbar */}
        <header className="bg-white border-b border-gray-100 px-4 sm:px-6 h-14 flex items-center justify-between flex-shrink-0 shadow-[0_1px_2px_rgba(0,0,0,0.02)]">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 rounded-lg text-gray-400 hover:bg-gray-100"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="hidden sm:block text-xs font-medium text-gray-400">
              {new Date().toLocaleDateString(lang === 'mr' ? 'mr-IN' : 'en-IN', {
                weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
              })}
            </div>
          </div>

          <div className="flex items-center gap-3 ml-auto">
            {/* Language toggle */}
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-gray-200 hover:border-primary-300 hover:bg-primary-50/50 text-xs font-semibold text-gray-700 transition-all shadow-2xs"
              title="Toggle language (English / मराठी)"
            >
              <Globe className="w-3.5 h-3.5 text-primary-600" />
              <span>{lang === 'en' ? 'मराठी' : 'English'}</span>
            </button>

            <NotificationBell />

            <div className="hidden sm:flex items-center gap-2 text-sm pl-2 border-l border-gray-100">
              <div className="w-7 h-7 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center font-bold text-xs">
                {user?.name?.[0]?.toUpperCase()}
              </div>
              <span className="font-semibold text-gray-700 text-xs">{user?.name}</span>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto">
          <div className="p-4 sm:p-6 page-transition">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
