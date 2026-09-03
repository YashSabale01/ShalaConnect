import { createContext, useContext, useState, useEffect } from 'react'

const LanguageContext = createContext()

export const translations = {
  en: {
    // Nav
    appName: 'ShalaConnect',
    tagline: 'Cluster Education Portal',
    dashboard: 'Dashboard',
    schools: 'Schools',
    attendance: 'Attendance',
    grDocuments: 'GR Documents',
    meetings: 'Meetings',
    events: 'Events',
    forms: 'Forms',
    users: 'Users',
    profile: 'Profile',
    logout: 'Logout',
    roleAdmin: 'Cluster Head Admin',
    roleHeadmaster: 'School Headmaster',

    // Attendance
    attendanceOverview: 'Attendance Overview',
    monitorAttendance: 'Monitor daily attendance across all cluster schools',
    submittedToday: 'Submitted Today',
    schoolsReported: 'Schools reported',
    avgToday: 'Avg Today',
    avgMonth: 'Avg This Month',
    todaysStatus: 'Today\'s Submission Status',
    exportBeoReport: 'Export BEO Monthly Report',
    exporting: 'Exporting...',
    statusSubmitted: 'Submitted',
    statusPending: 'Pending',
    submitAttendanceTitle: 'Submit Daily Attendance',
    totalStudents: 'Total Students',
    presentStudents: 'Present Students',
    absentStudents: 'Absent Students',
    totalTeachers: 'Total Teachers',
    presentTeachers: 'Present Teachers',
    remarks: 'Remarks / Comments',
    submitBtn: 'Submit Attendance',
    submittingBtn: 'Submitting...',
    offlineMode: 'Offline Mode: Attendance saved locally and will auto-sync when online',
    syncingOffline: 'Syncing offline attendance submissions...',
    offlineSyncSuccess: 'Offline attendance synchronized with server!',

    // Common
    search: 'Search...',
    allSchools: 'All Schools',
    schoolDetails: 'School Details',
    udiseCode: 'UDISE Code',
    village: 'Village',
    taluka: 'Taluka',
    district: 'District',
    headmaster: 'Headmaster',
    actions: 'Actions',
    close: 'Close',
    save: 'Save',
    cancel: 'Cancel',
    loading: 'Loading...',
    noData: 'No records found',
    notifications: 'Notifications',
    markAllRead: 'Mark all read',
  },
  mr: {
    // Nav
    appName: 'शाळाकनेक्ट',
    tagline: 'केंद्र शिक्षण पोर्टल',
    dashboard: 'डॅशबोर्ड',
    schools: 'शाळा माहिती',
    attendance: 'दैनिक उपस्थिती',
    grDocuments: 'शासन निर्णय (GR)',
    meetings: 'केंद्र बैठका',
    events: 'शालेय उपक्रम',
    forms: 'माहिती प्रपत्रे',
    users: 'वापरकर्ते',
    profile: 'माझी माहिती',
    logout: 'बाहेर पडणे',
    roleAdmin: 'केंद्र प्रमुख (प्रशासक)',
    roleHeadmaster: 'शाळा मुख्याध्यापक',

    // Attendance
    attendanceOverview: 'उपस्थिती आढावा',
    monitorAttendance: 'केंद्रातील सर्व शाळांची दैनिक उपस्थिती निरीक्षण',
    submittedToday: 'आज नोंद झालेली',
    schoolsReported: 'शाळांनी नोंद केली',
    avgToday: 'आजची सरासरी',
    avgMonth: 'मासिक सरासरी',
    todaysStatus: 'आजची उपस्थिती स्थिती',
    exportBeoReport: 'मासिक केंद्र अहवाल (BEO Report)',
    exporting: 'डाउनलोड होत आहे...',
    statusSubmitted: 'नोंद झाली',
    statusPending: 'प्रलंबित',
    submitAttendanceTitle: 'दैनिक उपस्थिती नोंदवा',
    totalStudents: 'पटसंख्या (विद्यार्थी)',
    presentStudents: 'उपस्थित विद्यार्थी',
    absentStudents: 'अनुपस्थित विद्यार्थी',
    totalTeachers: 'मंजूर शिक्षक',
    presentTeachers: 'हजर शिक्षक',
    remarks: 'शेरा / विशेष नोंद',
    submitBtn: 'उपस्थिती सादर करा',
    submittingBtn: 'सादर होत आहे...',
    offlineMode: 'ऑफलाइन मोड: उपस्थिती स्थानिकरित्या जतन झाली, नेटवर्क आल्यावर आपोआप सिंक होईल',
    syncingOffline: 'ऑफलाइन उपस्थिती सर्व्हरवर सिंक करत आहे...',
    offlineSyncSuccess: 'ऑफलाइन उपस्थिती यशस्वीरित्या नोंद झाली!',

    // Common
    search: 'शोधा...',
    allSchools: 'सर्व शाळा',
    schoolDetails: 'शाळा तपशील',
    udiseCode: 'यु-डायस कोड',
    village: 'गाव',
    taluka: 'तालुका',
    district: 'जिल्हा',
    headmaster: 'मुख्याध्यापक',
    actions: 'कृती',
    close: 'बंद करा',
    save: 'जतन करा',
    cancel: 'रद्द करा',
    loading: 'माहिती लोड होत आहे...',
    noData: 'माहिती उपलब्ध नाही',
    notifications: 'सूचना',
    markAllRead: 'सर्व वाचल्याचे चिन्हांकित करा',
  }
}

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(() => localStorage.getItem('shalaconnect_lang') || 'en')

  useEffect(() => {
    localStorage.setItem('shalaconnect_lang', lang)
    document.documentElement.lang = lang === 'mr' ? 'mr' : 'en'
  }, [lang])

  const toggleLanguage = () => {
    setLang(prev => (prev === 'en' ? 'mr' : 'en'))
  }

  const t = (key) => translations[lang]?.[key] || translations.en[key] || key

  return (
    <LanguageContext.Provider value={{ lang, setLang, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
}
