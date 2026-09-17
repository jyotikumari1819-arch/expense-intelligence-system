import { useState } from "react";
import { useSearchParams, useNavigate, Link } from "react-router-dom";
import { api } from "../api.js";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") || "";
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await api.resetPassword({ token, new_password: newPassword });
      setSuccess(true);
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (!token) {
    return (
      <div className="auth-page">
        <div className="auth-form">
          <h2>Invalid Link</h2>
          <p>This reset link is missing a token. Please request a new one.</p>
          <p><Link to="/forgot-password">Request a new link</Link></p>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-page">
      <form onSubmit={handleSubmit} className="auth-form">
        <h2>Set New Password</h2>
        {error && <p className="error">{error}</p>}
        {success ? (
          <p style={{ color: "var(--green)" }}>Password reset! Redirecting to login...</p>
        ) : (
          <>
            <input
              type="password"
              placeholder="New password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              minLength={6}
              required
            />
            <button type="submit" disabled={submitting}>
              {submitting ? "Saving..." : "Reset Password"}
            </button>
          </>
        )}
        <p><Link to="/login">Back to log in</Link></p>
      </form>
    </div>
  );
}
