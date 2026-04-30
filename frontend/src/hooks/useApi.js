import { useState, useEffect, useCallback } from 'react'

// Generic data-fetching hook
export function useApi(apiFn, deps = []) {
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)

  const fetch = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiFn()
      setData(res.data.data)
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }, deps) // eslint-disable-line

  useEffect(() => { fetch() }, [fetch])

  return { data, loading, error, refetch: fetch }
}

// Mutation hook for create/update/delete
export function useMutation(apiFn) {
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

  const mutate = useCallback(async (...args) => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiFn(...args)
      return res.data
    } catch (err) {
      const msg = err.response?.data?.message || 'Operation failed'
      setError(msg)
      throw err
    } finally {
      setLoading(false)
    }
  }, [apiFn])

  return { mutate, loading, error }
}
