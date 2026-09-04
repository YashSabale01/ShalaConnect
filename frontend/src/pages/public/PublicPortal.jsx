import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useApi } from '../../hooks/useApi'
import { schoolApi, eventApi } from '../../services/api'
import {
  GraduationCap, Search, MapPin, Users, Trophy,
  BookOpen, ArrowRight, Building2, Calendar, LogIn,
  Camera, X, ZoomIn, School
} from 'lucide-react'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function PublicPortal() {
  const { data: schools } = useApi(() => schoolApi.getAll())
  const { data: events  } = useApi(() => eventApi.getAll())
  const [search, setSearch] = useState('')
  const [selectedEvent, setSelectedEvent] = useState(null)
  const [eventImpls, setEventImpls] = useState([])
  const [loadingImpls, setLoadingImpls] = useState(false)
  const [lightboxPhoto, setLightboxPhoto] = useState(null)

  const filtered = (schools || []).filter(s =>
    s.name.toLowerCase().includes(search.toLowerCase()) ||
    s.village?.toLowerCase().includes(search.toLowerCase()) ||
    s.udiseCode?.includes(search)
  )

  const recentEvents = (events || []).slice(0, 6)

  const handleOpenEvent = async (event) => {
    setSelectedEvent(event)
    setLoadingImpls(true)
    try {
      const res = await eventApi.getImplementations(event.id)
      setEventImpls(res.data?.data || [])
    } catch (e) {
      console.error('Failed to load event implementations', e)
      setEventImpls([])
    } finally {
      setLoadingImpls(false)
    }
  }

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
              <div className="text-[10px] text-gray-400">शाळाकनेक्ट • महाराष्ट्र</div>
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
            ShalaConnect bridges the gap between cluster heads, headmasters, and citizens — showcasing real-time
            school activities, student attendance, and celebration photo galleries.
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
            {search ? `Results for "${search}"` : 'All Schools (शाळा यादी)'}
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
                <div className="w-full h-36 rounded-xl bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center mb-4 overflow-hidden">
                  {school.schoolPhoto ? (
                    <img src={`/uploads/${school.schoolPhoto}`} alt={school.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
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
                  <div className="mt-3 flex items-center gap-2 p-2 bg-yellow-50 rounded-lg border border-yellow-100">
                    <Trophy className="w-3.5 h-3.5 text-yellow-500 flex-shrink-0" />
                    <span className="text-xs text-yellow-800 truncate">
                      Topper: <strong>{school.topperName}</strong> ({school.topperPercentage}%)
                    </span>
                  </div>
                )}

                <div className="mt-4 flex items-center text-xs font-medium text-primary-600 group-hover:gap-2 transition-all gap-1">
                  View Profile & Activity Photos <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* Recent Events & Celebrations Gallery */}
      {recentEvents.length > 0 && (
        <section className="bg-slate-50 py-16 px-4 border-t border-gray-100">
          <div className="max-w-7xl mx-auto">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-8">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <Camera className="w-6 h-6 text-primary-600" />
                  Cluster Events & School Photo Proof (शालेय उपक्रम व छायाचित्रे)
                </h2>
                <p className="text-sm text-gray-500 mt-1">
                  Click any celebration event to explore photo proof and implementation reports from participating schools
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {recentEvents.map(event => (
                <div
                  key={event.id}
                  onClick={() => handleOpenEvent(event)}
                  className="card-hover p-5 cursor-pointer flex flex-col justify-between group border border-gray-200"
                >
                  <div>
                    {event.mediaPaths?.length > 0 ? (
                      <div className="w-full h-40 rounded-xl overflow-hidden mb-4 bg-gray-100">
                        <img src={`/uploads/${event.mediaPaths[0]}`} alt={event.title}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                      </div>
                    ) : (
                      <div className="w-full h-32 rounded-xl bg-gradient-to-br from-orange-50 to-primary-50 flex items-center justify-center mb-4 text-primary-400">
                        <BookOpen className="w-10 h-10" />
                      </div>
                    )}

                    <div className="flex items-center gap-2 mb-2">
                      <Calendar className="w-3.5 h-3.5 text-primary-500" />
                      <span className="text-xs font-medium text-gray-500">
                        {event.eventDate && format(new Date(event.eventDate), 'dd MMMM yyyy')}
                      </span>
                    </div>

                    <h3 className="font-bold text-gray-900 group-hover:text-primary-600 transition-colors mb-1.5">
                      {event.title}
                    </h3>

                    {event.description && (
                      <p className="text-sm text-gray-500 line-clamp-2 leading-relaxed mb-3">
                        {event.description}
                      </p>
                    )}
                  </div>

                  <div className="pt-3 border-t border-gray-100 flex items-center justify-between">
                    <span className="text-xs font-semibold text-primary-600 flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
                      📸 View School Photos <ArrowRight className="w-3.5 h-3.5" />
                    </span>
                    <span className="badge badge-blue text-[10px]">
                      {event.eventType || 'CELEBRATION'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Event Details & School Implementation Photos Modal */}
      {selectedEvent && (
        <div
          className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto"
          onClick={() => setSelectedEvent(null)}
        >
          <div
            className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto shadow-2xl p-6 sm:p-8"
            onClick={e => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="flex items-start justify-between border-b border-gray-100 pb-4 mb-6">
              <div>
                <div className="inline-flex items-center gap-1.5 text-xs text-primary-600 font-semibold mb-1">
                  <Calendar className="w-3.5 h-3.5" />
                  {selectedEvent.eventDate && format(new Date(selectedEvent.eventDate), 'dd MMMM yyyy')}
                  {selectedEvent.venue && <span>• {selectedEvent.venue}</span>}
                </div>
                <h2 className="text-xl sm:text-2xl font-bold text-gray-900">{selectedEvent.title}</h2>
                {selectedEvent.description && (
                  <p className="text-sm text-gray-600 mt-2 leading-relaxed">{selectedEvent.description}</p>
                )}
              </div>
              <button
                onClick={() => setSelectedEvent(null)}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors ml-4"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* School Implementations List */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-gray-900 text-base flex items-center gap-2">
                  <Camera className="w-5 h-5 text-primary-600" />
                  School Photo Proof & Reports ({eventImpls.length} Schools)
                </h3>
              </div>

              {loadingImpls ? (
                <div className="py-12 flex justify-center">
                  <div className="w-7 h-7 border-2 border-primary-600 border-t-transparent rounded-full animate-spin" />
                </div>
              ) : eventImpls.length === 0 ? (
                <div className="text-center py-10 bg-gray-50 rounded-xl border border-dashed border-gray-200 text-gray-400">
                  <Camera className="w-8 h-8 mx-auto mb-2 text-gray-300" />
                  <p className="text-sm font-medium text-gray-600">No schools have uploaded photo proof yet</p>
                  <p className="text-xs text-gray-400 mt-0.5">Headmasters will submit event reports and photos here.</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {eventImpls.map(impl => (
                    <div key={impl.id} className="border border-gray-200 rounded-xl p-5 bg-gray-50/50">
                      <div className="flex items-center justify-between mb-2">
                        <Link
                          to={`/school/${impl.schoolId}`}
                          className="font-bold text-primary-700 hover:underline flex items-center gap-1.5 text-base"
                        >
                          <School className="w-4 h-4" />
                          {impl.schoolName}
                        </Link>
                        {impl.photoPaths?.length > 0 && (
                          <span className="badge badge-green text-xs">
                            {impl.photoPaths.length} Photo{impl.photoPaths.length > 1 ? 's' : ''}
                          </span>
                        )}
                      </div>

                      {impl.description && (
                        <p className="text-sm text-gray-700 bg-white p-3 rounded-lg border border-gray-100 mb-3 whitespace-pre-wrap">
                          {impl.description}
                        </p>
                      )}

                      {/* Photo Grid */}
                      {impl.photoPaths?.length > 0 && (
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                          {impl.photoPaths.map((photo, pIdx) => (
                            <div
                              key={pIdx}
                              onClick={() => setLightboxPhoto(`/uploads/${photo}`)}
                              className="group relative h-28 rounded-lg overflow-hidden cursor-pointer border border-gray-200 bg-gray-100"
                            >
                              <img
                                src={`/uploads/${photo}`}
                                alt={`School implementation photo ${pIdx + 1}`}
                                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                                loading="lazy"
                              />
                              <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                <ZoomIn className="w-5 h-5 text-white" />
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Lightbox / Zoom Modal */}
      {lightboxPhoto && (
        <div
          className="fixed inset-0 z-50 bg-black/90 backdrop-blur-sm flex items-center justify-center p-4"
          onClick={() => setLightboxPhoto(null)}
        >
          <button
            onClick={() => setLightboxPhoto(null)}
            className="absolute top-4 right-4 text-white hover:text-gray-300 p-2 rounded-full bg-white/10 hover:bg-white/20 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
          <img
            src={lightboxPhoto}
            alt="Enlarged photo"
            className="max-h-[90vh] max-w-[95vw] rounded-xl shadow-2xl object-contain"
            onClick={e => e.stopPropagation()}
          />
        </div>
      )}

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <GraduationCap className="w-5 h-5 text-primary-400" />
          <span className="font-semibold">ShalaConnect | शाळाकनेक्ट</span>
        </div>
        <p className="text-sm text-gray-400">
          Empowering education through digital connectivity • Maharashtra
        </p>
        <p className="text-xs text-gray-600 mt-2">© {new Date().getFullYear()} ShalaConnect. All rights reserved.</p>
      </footer>
    </div>
  )
}
