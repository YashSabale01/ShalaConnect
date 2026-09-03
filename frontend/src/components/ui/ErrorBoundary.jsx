import React from 'react'
import { AlertTriangle, RefreshCw, Home } from 'lucide-react'

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Unhandled UI exception in ErrorBoundary:', error, errorInfo)
  }

  handleReload = () => {
    window.location.reload()
  }

  handleGoHome = () => {
    window.location.href = '/'
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-white rounded-2xl shadow-xl border border-slate-200 p-8 text-center animate-fade-in">
            <div className="w-16 h-16 bg-red-50 text-red-600 rounded-2xl flex items-center justify-center mx-auto mb-5 shadow-inner">
              <AlertTriangle className="w-8 h-8" />
            </div>
            <h2 className="text-xl font-bold text-slate-900 mb-2">
              Something went wrong / काहीतरी चूक झाली
            </h2>
            <p className="text-sm text-slate-600 mb-6 leading-relaxed">
              The application encountered an unexpected error. Don't worry, your data is safe.
            </p>
            {this.state.error && (
              <div className="bg-slate-100 rounded-lg p-3 text-left mb-6 overflow-x-auto">
                <p className="text-xs font-mono text-slate-700 break-words">
                  {this.state.error.message || String(this.state.error)}
                </p>
              </div>
            )}
            <div className="flex gap-3 justify-center">
              <button
                onClick={this.handleReload}
                className="btn-primary inline-flex items-center gap-2"
              >
                <RefreshCw className="w-4 h-4" />
                Reload Page
              </button>
              <button
                onClick={this.handleGoHome}
                className="btn-secondary inline-flex items-center gap-2"
              >
                <Home className="w-4 h-4" />
                Back to Home
              </button>
            </div>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
