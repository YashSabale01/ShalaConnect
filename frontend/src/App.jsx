import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './context/AuthContext'
import { LanguageProvider } from './context/LanguageContext'
import ErrorBoundary from './components/ui/ErrorBoundary'
import ProtectedRoute from './components/layout/ProtectedRoute'
import DashboardLayout from './components/layout/DashboardLayout'

// Auth pages
import LoginPage from './pages/auth/LoginPage'

// Admin pages
import AdminDashboard    from './pages/admin/AdminDashboard'
import SchoolsPage       from './pages/admin/SchoolsPage'
import SchoolDetailPage  from './pages/admin/SchoolDetailPage'
import AttendancePage    from './pages/admin/AttendancePage'
import GrDocumentsPage   from './pages/admin/GrDocumentsPage'
import MeetingsPage      from './pages/admin/MeetingsPage'
import EventsPage        from './pages/admin/EventsPage'
import FormsPage         from './pages/admin/FormsPage'
import UsersPage         from './pages/admin/UsersPage'
import AdminProfilePage  from './pages/admin/AdminProfilePage'

// Headmaster pages
import HeadmasterDashboard from './pages/headmaster/HeadmasterDashboard'
import SubmitAttendancePage from './pages/headmaster/SubmitAttendancePage'
import HeadmasterGrPage    from './pages/headmaster/HeadmasterGrPage'
import HeadmasterMeetingsPage from './pages/headmaster/HeadmasterMeetingsPage'
import HeadmasterFormsPage from './pages/headmaster/HeadmasterFormsPage'
import HeadmasterEventsPage from './pages/headmaster/HeadmasterEventsPage'
import HeadmasterProfilePage from './pages/headmaster/HeadmasterProfilePage'

// Public pages
import PublicPortal from './pages/public/PublicPortal'
import PublicSchoolDetail from './pages/public/PublicSchoolDetail'

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <LanguageProvider>
          <AuthProvider>
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: { borderRadius: '12px', fontSize: '14px', fontWeight: '500' },
                success: { iconTheme: { primary: '#16a34a', secondary: '#fff' } },
                error:   { iconTheme: { primary: '#dc2626', secondary: '#fff' } },
              }}
            />
            <Routes>
              {/* Public routes */}
              <Route path="/"          element={<PublicPortal />} />
              <Route path="/school/:id" element={<PublicSchoolDetail />} />
              <Route path="/login"     element={<LoginPage />} />

              {/* Admin routes */}
              <Route element={<ProtectedRoute allowedRoles={['ADMIN']} />}>
                <Route element={<DashboardLayout role="ADMIN" />}>
                  <Route path="/admin"                element={<AdminDashboard />} />
                  <Route path="/admin/schools"        element={<SchoolsPage />} />
                  <Route path="/admin/schools/:id"    element={<SchoolDetailPage />} />
                  <Route path="/admin/attendance"     element={<AttendancePage />} />
                  <Route path="/admin/gr-documents"   element={<GrDocumentsPage />} />
                  <Route path="/admin/meetings"       element={<MeetingsPage />} />
                  <Route path="/admin/events"         element={<EventsPage />} />
                  <Route path="/admin/forms"          element={<FormsPage />} />
                  <Route path="/admin/users"          element={<UsersPage />} />
                  <Route path="/admin/profile"        element={<AdminProfilePage />} />
                </Route>
              </Route>

              {/* Headmaster routes */}
              <Route element={<ProtectedRoute allowedRoles={['HEADMASTER']} />}>
                <Route element={<DashboardLayout role="HEADMASTER" />}>
                  <Route path="/headmaster"               element={<HeadmasterDashboard />} />
                  <Route path="/headmaster/attendance"    element={<SubmitAttendancePage />} />
                  <Route path="/headmaster/gr-documents"  element={<HeadmasterGrPage />} />
                  <Route path="/headmaster/meetings"      element={<HeadmasterMeetingsPage />} />
                  <Route path="/headmaster/forms"         element={<HeadmasterFormsPage />} />
                  <Route path="/headmaster/events"        element={<HeadmasterEventsPage />} />
                  <Route path="/headmaster/profile"       element={<HeadmasterProfilePage />} />
                </Route>
              </Route>

              {/* Fallback */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </AuthProvider>
        </LanguageProvider>
      </BrowserRouter>
    </ErrorBoundary>
  )
}
