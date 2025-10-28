import React, { useState, useEffect, useRef } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import './AnimatedLogin.css';

const AnimatedLogin = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [isPasswordFocused, setIsPasswordFocused] = useState(false);
  const [loginSuccess, setLoginSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [isEmailFocused, setIsEmailFocused] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    const handleMouseMove = (e) => {
      const x = (e.clientX / window.innerWidth) * 100;
      const y = (e.clientY / window.innerHeight) * 100;
      setMousePos({ x, y });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
      await onLogin(email, password);
      setLoginSuccess(true);
      setTimeout(() => setLoginSuccess(false), 2000);
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="animated-login-container" ref={containerRef}>
      {/* Left Side - Character Shapes */}
      <div className="shapes-container">
        <div className="shapes-wrapper">
          {/* Orange Semicircle Character */}
          <div className={`character orange-semicircle ${isPasswordFocused ? 'privacy-mode' : ''} ${loginSuccess ? 'celebrate' : ''} ${isEmailFocused ? 'excited' : ''}`}
               style={{'--mouse-x': `${mousePos.x}%`, '--mouse-y': `${mousePos.y}%`}}>
            <div className="eyes">
              <div className="eye left-eye"></div>
              <div className="eye right-eye"></div>
            </div>
            <div className="mouth"></div>
          </div>
          
          {/* Violet Rectangle Character */}
          <div className={`character violet-rectangle ${isPasswordFocused ? 'privacy-mode' : ''} ${loginSuccess ? 'celebrate' : ''} ${isEmailFocused ? 'excited' : ''}`}
               style={{'--mouse-x': `${mousePos.x}%`, '--mouse-y': `${mousePos.y}%`}}>
            <div className="eyes">
              <div className="eye left-eye"></div>
              <div className="eye right-eye"></div>
            </div>
            <div className="mouth"></div>
          </div>
          
          {/* Black Small Rectangle Character */}
          <div className={`character black-rectangle ${isPasswordFocused ? 'privacy-mode' : ''} ${loginSuccess ? 'celebrate' : ''} ${isEmailFocused ? 'excited' : ''}`}
               style={{'--mouse-x': `${mousePos.x}%`, '--mouse-y': `${mousePos.y}%`}}>
            <div className="eyes">
              <div className="eye left-eye"></div>
              <div className="eye right-eye"></div>
            </div>
            <div className="mouth"></div>
          </div>
          
          {/* Yellow Cylinder Character */}
          <div className={`character yellow-cylinder ${isPasswordFocused ? 'privacy-mode' : ''} ${loginSuccess ? 'celebrate' : ''} ${isEmailFocused ? 'excited' : ''}`}
               style={{'--mouse-x': `${mousePos.x}%`, '--mouse-y': `${mousePos.y}%`}}>
            <div className="eyes">
              <div className="eye left-eye"></div>
              <div className="eye right-eye"></div>
            </div>
            <div className="mouth"></div>
          </div>
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div className="form-container">
        <div className="form-wrapper">
          <div className="form-header">
            <h2>Welcome back!</h2>
            <p>Please enter your details</p>
            {error && (
              <div className="error-message" style={{color: '#ef4444', fontSize: '0.875rem', marginTop: '0.5rem'}}>
                {error}
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onFocus={() => setIsEmailFocused(true)}
                onBlur={() => setIsEmailFocused(false)}
                placeholder="Enter your email"
                required
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <div className="password-input">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onFocus={() => setIsPasswordFocused(true)}
                  onBlur={() => setIsPasswordFocused(false)}
                  placeholder="Enter your password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="password-toggle"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            <div className="form-options">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                />
                <span>Remember for 30 days</span>
              </label>
              <a href="#" className="forgot-link">
                Forgot password?
              </a>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="login-btn"
            >
              {isLoading ? (
                <div className="loading">
                  <div className="spinner"></div>
                  Signing in...
                </div>
              ) : (
                'Log In'
              )}
            </button>


          </form>

          <p className="signup-link">
            Don't have an account?{' '}
            <a href="/register">Sign Up</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AnimatedLogin;