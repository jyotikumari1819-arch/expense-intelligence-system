import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api.js";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    setSubmitting(true);
    try {
      const res = await api.forgotPassword({ email });
      setMessage(res.message);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <form onSubmit={handleSubmit} className="auth-form">
        <h2>Reset Password</h2>
        <p style={{ fontSize: "0.85rem", color: "var(--ink-soft)" }}>
          Enter your account email — we'll send a link to reset your password.
        </p>
        {error && <p className="error">{error}</p>}
        {message && <p style={{ color: "var(--green)", fontSize: "0.88rem" }}>{message}</p>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit" disabled={submitting}>
          {submitting ? "Sending..." : "Send Reset Link"}
        </button>
        <p><Link to="/login">Back to log in</Link></p>
      </form>
    </div>
  );
}
