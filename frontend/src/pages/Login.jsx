import { useState } from 'react'
import { api } from '../services/api'

function Login({ onLogin, onRegister }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()

    setError('')
    setLoading(true)

    try {
      const data = await api.login({
        email,
        password,
      })

      const token =
        data.access_token ||
        data.token ||
        data.accessToken

      if (!token) {
        throw new Error('Login succeeded but no access token was returned.')
      }

      localStorage.setItem('carelens_token', token)

      if (data.user) {
        localStorage.setItem(
          'carelens_user',
          JSON.stringify(data.user),
        )
      }

      onLogin()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-brand">
        <div className="brand-icon large">C</div>
        <div>
          <h1>CareLens AI</h1>
          <p>Intelligent Clinical Decision Support</p>
        </div>
      </div>

      <div className="auth-card">
        <div className="auth-header">
          <span className="eyebrow">SECURE ACCESS</span>
          <h2>Welcome back</h2>
          <p>
            Sign in to access your clinical intelligence workspace.
          </p>
        </div>

        {error && <div className="error-box">{error}</div>}

        <form onSubmit={handleSubmit}>
          <label>
            Email
            <input
              type="email"
              placeholder="doctor@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>

          <button
            className="primary-button full"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>

        <div className="auth-footer">
          Don't have an account?
          <button onClick={onRegister}>
            Create account
          </button>
        </div>
      </div>

      <p className="auth-disclaimer">
        CareLens AI is a clinical decision-support tool and does not
        replace professional medical judgment.
      </p>
    </div>
  )
}

export default Login