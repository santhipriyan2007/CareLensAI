import { useState } from 'react'
import { api } from '../services/api'

function Register({ onRegistered, onLogin }) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('doctor')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()

    setError('')
    setSuccess('')
    setLoading(true)

    try {
      await api.register({
        name,
        email,
        password,
        role,
      })

      setSuccess(
        'Account created successfully. You can now sign in.',
      )

      setTimeout(() => {
        onRegistered()
      }, 1000)
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
          <span className="eyebrow">GET STARTED</span>
          <h2>Create account</h2>
          <p>
            Create a secure account for the CareLens clinical platform.
          </p>
        </div>

        {error && <div className="error-box">{error}</div>}
        {success && <div className="success-box">{success}</div>}

        <form onSubmit={handleSubmit}>
          <label>
            Full name
            <input
              type="text"
              placeholder="Dr. Alex"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </label>

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
              placeholder="Create a password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              minLength="6"
              required
            />
          </label>

          <label>
            Role
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="doctor">Doctor</option>
              <option value="patient">Patient</option>
            </select>
          </label>

          <button
            className="primary-button full"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Create account'}
          </button>
        </form>

        <div className="auth-footer">
          Already have an account?
          <button onClick={onLogin}>
            Sign in
          </button>
        </div>
      </div>
    </div>
  )
}

export default Register