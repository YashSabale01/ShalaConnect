import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useApi } from '../../hooks/useApi'
import { schoolApi, eventApi } from '../../services/api'
import {
  GraduationCap, Search, MapPin, Users, Trophy,
  BookOpen, ArrowRight, Building2, Calendar, LogIn
} from 'lucide-react'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function PublicPortal() {
  const { data: schools } = useApi(() => schoolApi.getAll())
  const { data: events  } = useApi(() => eventApi.getAll())
  const [search, setSearch] = useState('')

  const filtered = (schools || []).filter(s =>
    s.name.toLowerCase().includes(search.toLowerCase()) ||
    s.village?.toLowerCase().includes(search.toLowerCase()) ||
    s.udiseCode?.includes(search)
  )

  const recentEvents = (events || []).slice(0, 3)

  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="sticky top-0 z-40 bg-white border-b border-gray-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-primary-600 rounded-xl flex items-center justify-center">
              <GraduationCap className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="font-bold text-gray-900 text-sm leading-tight">ShalaConnect</div>
              <div className="text-[10px] text-gray-400">शाळाकनेक्ट</div>
            </div>
          </div>
          <Link to="/login" className="btn-primary btn-sm">
            <LogIn className="w-3.5 h-3.5" />
            Staff Login
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="bg-gradient-to-br from-primary-700 to-primary-900 text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-full px-4 py-1.5 text-sm mb-6">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            Maharashtra Education Initiative
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-4 leading-tight">
            Empowering Rural Schools<br />through Digital Connect
          </h1>
          <p className="text-primary-200 text-lg mb-8 max-w-2xl mx-auto">
            ShalaConnect bridges the gap between cluster heads and schools — enabling real-time
            attendance tracking, document sharing, and event management.
          </p>
          {/* Search bar */}
          <div className="max-w-xl mx-auto">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search schools by name, village, or UDISE code…"
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="w-full pl-12 pr-4 py-4 rounded-2xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-300 shadow-lg text-sm"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Stats banner */}
      <section className="bg-primary-800 text-white py-6 px-4">
        <div className="max-w-4xl mx-auto grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold">{schools?.length || 0}</div>
            <div className="text-xs text-primary-200 mt-0.5">Schools Connected</div>
          </div>
          <div>
            <div className="text-2xl font-bold">
              {(schools || []).reduce((s, sc) => s + (sc.totalStudents || 0), 0).toLocaleString()}
            </div>
            <div className="text-xs text-primary-200 mt-0.5">Total Students</div>
          </div>
          <div>
            <div className="text-2xl font-bold">{events?.length || 0}</div>
            <div className="text-xs text-primary-200 mt-0.5">Events Documented</div>
          </div>
        </div>
      </section>

      {/* Schools list */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            {search ? `Results for "${search}"` : 'All Schools'}
          </h2>
          {search && (
            <button onClick={() => setSearch('')} className="text-sm text-primary-600 hover:underline">
              Clear search
            </button>
          )}
        </div>

        {filtered.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <Building2 className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p className="font-medium">No schools found</p>
            <p className="text-sm mt-1">Try a different search</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {filtered.map(school => (
              <Link
                key={school.id}
                to={`/school/${school.id}`}
                className="card-hover p-5 block group"
              >
                {/* School photo */}
                <div className="w-full h-32 rounded-xl bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center mb-4 overflow-hidden">
                  {school.schoolPhoto ? (
                    <img src={`/uploads/${school.schoolPhoto}`} alt={school.name}
                      className="w-full h-full object-cover" />
                  ) : (
                    <Building2 className="w-10 h-10 text-primary-400" />
                  )}
                </div>

                <h3 className="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors mb-1 line-clamp-2">
                  {school.name}
                </h3>

                <p className="text-xs font-mono text-gray-400 mb-3">
                  UDISE: {school.udiseCode}
                </p>

                <div className="space-y-1.5 text-sm text-gray-500">
                  {school.village && (
                    <div className="flex items-center gap-1.5">
                      <MapPin className="w-3.5 h-3.5 text-gray-400 flex-shrink-0" />
                      <span className="truncate">{[school.village, school.taluka].filter(Boolean).join(', ')}</span>
                    </div>
                  )}
                  <div className="flex items-center gap-1.5">
                    <Users className="w-3.5 h-3.5 text-gray-400 flex-shrink-0" />
                    <span>
                      {school.totalStudents ?? 0} students • {school.totalTeachers ?? 0} teachers
                    </span>
                  </div>
                </div>

                {school.topperName && (
                  <div className="mt-3 flex items-center gap-2 p-2 bg-yellow-50 rounded-lg">
                    <Trophy className="w-3.5 h-3.5 text-yellow-500 flex-shrink-0" />
                    <span className="text-xs text-yellow-800">
                      Topper: <strong>{school.topperName}</strong> ({school.topperPercentage}%)
                    </span>
                  </div>
                )}

                <div className="mt-4 flex items-center text-xs font-medium text-primary-600 group-hover:gap-2 transition-all gap-1">
                  View Details <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* Recent Events */}
      {recentEvents.length > 0 && (
        <section className="bg-gray-50 py-12 px-4">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Events</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
              {recentEvents.map(event => (
                <div key={event.id} className="card-hover p-5">
                  {event.mediaPaths?.length > 0 && (
                    <div className="w-full h-36 rounded-xl overflow-hidden mb-4">
                      <img src={`/uploads/${event.mediaPaths[0]}`} alt={event.title}
                        className="w-full h-full object-cover" />
                    </div>
                  )}
                  <div className="flex items-center gap-2 mb-2">
                    <BookOpen className="w-4 h-4 text-orange-500" />
                    <span className="text-xs text-gray-400">
                      {event.eventDate && format(new Date(event.eventDate), 'dd MMM yyyy')}
                    </span>
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-1">{event.title}</h3>
                  {event.description && (
                    <p className="text-sm text-gray-500 line-clamp-2">{event.description}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <GraduationCap className="w-5 h-5 text-primary-400" />
          <span className="font-semibold">ShalaConnect</span>
        </div>
        <p className="text-sm text-gray-400">
          Empowering education through digital connectivity • Maharashtra
        </p>
        <p className="text-xs text-gray-600 mt-2">© {new Date().getFullYear()} ShalaConnect. All rights reserved.</p>
      </footer>
    </div>
  )
}
