import { useState } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import NotificationBell from '../ui/NotificationBell'
import {
  LayoutDashboard, School, CalendarCheck2, FileText, Users,
  BookOpen, CalendarDays, ClipboardList, Menu, X, LogOut,
  ChevronRight, GraduationCap, Building2
} from 'lucide-react'
import clsx from 'clsx'

const adminNav = [
  { to: '/admin',             icon: LayoutDashboard, label: 'Dashboard',    end: true },
  { to: '/admin/schools',     icon: Building2,       label: 'Schools' },
  { to: '/admin/attendance',  icon: CalendarCheck2,  label: 'Attendance' },
  { to: '/admin/gr-documents',icon: FileText,        label: 'GR Documents' },
  { to: '/admin/meetings',    icon: CalendarDays,    label: 'Meetings' },
  { to: '/admin/events',      icon: BookOpen,        label: 'Events' },
  { to: '/admin/forms',       icon: ClipboardList,   label: 'Forms' },
  { to: '/admin/users',       icon: Users,           label: 'Users' },
]

const headmasterNav = [
  { to: '/headmaster',              icon: LayoutDashboard, label: 'Dashboard',    end: true },
  { to: '/headmaster/attendance',   icon: CalendarCheck2,  label: 'Attendance' },
  { to: '/headmaster/gr-documents', icon: FileText,        label: 'GR Documents' },
  { to: '/headmaster/meetings',     icon: CalendarDays,    label: 'Meetings' },
  { to: '/headmaster/forms',        icon: ClipboardList,   label: 'Forms' },
  { to: '/headmaster/events',       icon: BookOpen,        label: 'Events' },
]

export default function DashboardLayout({ role }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const nav = role === 'ADMIN' ? adminNav : headmasterNav

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const SidebarContent = () => (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-gray-100">
        <div className="w-9 h-9 bg-primary-600 rounded-lg flex items-center justify-center flex-shrink-0">
          <GraduationCap className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="font-bold text-gray-900 text-sm leading-tight">ShalaConnect</div>
          <div className="text-xs text-gray-400">शाळाकनेक्ट</div>
        </div>
      </div>

      {/* Role badge */}
      <div className="px-4 py-3">
        <span className={clsx(
          'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold',
          role === 'ADMIN' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
        )}>
          <span className="w-1.5 h-1.5 rounded-full bg-current" />
          {role === 'ADMIN' ? 'Cluster Head Admin' : 'School Headmaster'}
        </span>
      </div>

      {/* Nav links */}
      <nav className="flex-1 px-3 py-2 space-y-0.5 overflow-y-auto">
        {nav.map(({ to, icon: Icon, label, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            onClick={() => setSidebarOpen(false)}
            className={({ isActive }) =>
              clsx('sidebar-link group', isActive ? 'sidebar-link-active' : 'sidebar-link-inactive')
            }
          >
            {({ isActive }) => (
              <>
                <Icon className={clsx('w-4 h-4 flex-shrink-0',
                  isActive ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-600')} />
                <span className="flex-1">{label}</span>
                {isActive && <ChevronRight className="w-3 h-3 text-primary-400" />}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* User section */}
      <div className="border-t border-gray-100 p-3">
        <div className="flex items-center gap-3 px-2 py-2 rounded-lg mb-1">
          <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0">
            <span className="text-primary-700 text-sm font-semibold">
              {user?.name?.[0]?.toUpperCase()}
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium text-gray-900 truncate">{user?.name}</div>
            <div className="text-xs text-gray-400 truncate">
              {role === 'HEADMASTER' && user?.school?.name ? user.school.name : user?.email}
            </div>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="sidebar-link sidebar-link-inactive w-full text-red-600 hover:bg-red-50 hover:text-red-700"
        >
          <LogOut className="w-4 h-4" />
          <span>Logout</span>
        </button>
      </div>
    </div>
  )

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex flex-col w-60 bg-white border-r border-gray-100 flex-shrink-0">
        <SidebarContent />
      </aside>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="lg:hidden fixed inset-0 z-40">
          <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={() => setSidebarOpen(false)} />
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
        <header className="bg-white border-b border-gray-100 px-4 sm:px-6 h-14 flex items-center justify-between flex-shrink-0">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden p-2 rounded-lg text-gray-400 hover:bg-gray-100"
          >
            <Menu className="w-5 h-5" />
          </button>
          <div className="hidden lg:block text-sm text-gray-400">
            {new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          </div>
          <div className="flex items-center gap-3 ml-auto">
            <NotificationBell />
            <div className="hidden sm:flex items-center gap-2 text-sm">
              <div className="w-7 h-7 rounded-full bg-primary-100 flex items-center justify-center">
                <span className="text-primary-700 text-xs font-semibold">
                  {user?.name?.[0]?.toUpperCase()}
                </span>
              </div>
              <span className="font-medium text-gray-700">{user?.name}</span>
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
