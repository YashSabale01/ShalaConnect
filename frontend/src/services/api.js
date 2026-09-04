import axios from 'axios'
import toast from 'react-hot-toast'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor — attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor — handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status
    const message = error.response?.data?.message || 'Something went wrong'

    if (status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
      toast.error('Session expired. Please login again.')
    } else if (status === 403) {
      toast.error('Access denied')
    } else if (status === 404) {
      toast.error(message)
    } else if (status === 400) {
      // Validation errors are shown by forms individually
    }

    return Promise.reject(error)
  }
)

export default api

// ─── Auth ────────────────────────────────────────────────────────────────────
export const authApi = {
  login:              (data)    => api.post('/auth/login', data),
  me:                 ()        => api.get('/auth/me'),
  registerHeadmaster: (data)    => api.post('/auth/register-headmaster', data),
  changePassword:     (data)    => api.post('/auth/change-password', data),
}

// ─── Schools ─────────────────────────────────────────────────────────────────
export const schoolApi = {
  getAll:      ()        => api.get('/schools'),
  getById:     (id)      => api.get(`/schools/${id}`),
  create:      (data)    => api.post('/schools', data),
  update:      (id, data)=> api.put(`/schools/${id}`, data),
  uploadPhoto: (id, file)=> {
    const fd = new FormData(); fd.append('file', file)
    return api.post(`/schools/${id}/photo`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  delete:      (id)      => api.delete(`/schools/${id}`),
  removeHeadmaster: (id) => api.delete(`/schools/${id}/headmaster`),
}

// ─── Attendance ───────────────────────────────────────────────────────────────
export const attendanceApi = {
  submit:       (data)               => api.post('/attendance', data),
  update:       (id, data)           => api.put(`/attendance/${id}`, data),
  getBySchool:  (schoolId)           => api.get(`/attendance/school/${schoolId}`),
  getByRange:   (schoolId, s, e)     => api.get(`/attendance/school/${schoolId}/range?start=${s}&end=${e}`),
  getByDate:    (date)               => api.get(`/attendance/date/${date}`),
  getSummary:   ()                   => api.get('/attendance/summary'),
  exportMonthly:(year, month)        => api.get(`/attendance/export-monthly?year=${year}&month=${month}`, { responseType: 'blob' }),
}

// ─── GR Documents ─────────────────────────────────────────────────────────────
export const grApi = {
  getAll:   ()   => api.get('/gr'),
  getById:  (id) => api.get(`/gr/${id}`),
  upload:   (fd) => api.post('/gr', fd, { headers: { 'Content-Type': 'multipart/form-data' } }),
  markSeen: (id) => api.post(`/gr/${id}/seen`),
  delete:   (id) => api.delete(`/gr/${id}`),
}

// ─── Meetings ─────────────────────────────────────────────────────────────────
export const meetingApi = {
  getAll:      ()       => api.get('/meetings'),
  getUpcoming: ()       => api.get('/meetings/upcoming'),
  getById:     (id)     => api.get(`/meetings/${id}`),
  create:      (data)   => api.post('/meetings', data),
  update:      (id, data)=> api.put(`/meetings/${id}`, data),
  acknowledge: (id)     => api.post(`/meetings/${id}/acknowledge`),
  delete:      (id)     => api.delete(`/meetings/${id}`),
}

// ─── Events ───────────────────────────────────────────────────────────────────
export const eventApi = {
  getAll:              ()        => api.get('/events'),
  getById:             (id)      => api.get(`/events/${id}`),
  create:              (data)    => api.post('/events', data),
  update:              (id, data)=> api.put(`/events/${id}`, data),
  uploadMedia:         (id, file)=> {
    const fd = new FormData(); fd.append('file', file)
    return api.post(`/events/${id}/media`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  uploadReport:        (id, file)=> {
    const fd = new FormData(); fd.append('file', file)
    return api.post(`/events/${id}/report`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  delete:              (id)      => api.delete(`/events/${id}`),
  // Implementation
  submitImplementation:(id, desc) => api.post(`/events/${id}/implement`, { description: desc }),
  uploadImplPhoto:     (id, file)=> {
    const fd = new FormData(); fd.append('file', file)
    return api.post(`/events/${id}/implement/photo`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  getImplementations:        (id)       => api.get(`/events/${id}/implementations`),
  getSchoolImplementations:  (schoolId) => api.get(`/events/school/${schoolId}/implementations`),
  getMyImplementation:       (id)       => api.get(`/events/${id}/my-implementation`),
}

// ─── Forms ────────────────────────────────────────────────────────────────────
export const formApi = {
  getAll:   ()          => api.get('/forms'),
  getById:  (id)        => api.get(`/forms/${id}`),
  create:   (data)      => api.post('/forms', data),
  respond:  (id, data)  => api.post(`/forms/${id}/respond`, data),
  export:   (id)        => api.get(`/forms/${id}/export`, { responseType: 'blob' }),
  delete:   (id)        => api.delete(`/forms/${id}`),
}

// ─── Notifications ────────────────────────────────────────────────────────────
export const notificationApi = {
  getAll:       ()   => api.get('/notifications'),
  getCount:     ()   => api.get('/notifications/unread-count'),
  markRead:     (id) => api.patch(`/notifications/${id}/read`),
  markAllRead:  ()   => api.patch('/notifications/read-all'),
}

// ─── Users ────────────────────────────────────────────────────────────────────
export const userApi = {
  getAll:         ()   => api.get('/users'),
  getHeadmasters: ()   => api.get('/users/headmasters'),
  toggleActive:   (id) => api.patch(`/users/${id}/toggle-active`),
  assignSchool:   (id, schoolId) => api.patch(`/users/${id}/assign-school`, { schoolId: schoolId || null }),
  delete:         (id) => api.delete(`/users/${id}`),
}
