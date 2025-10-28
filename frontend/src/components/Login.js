import React, { useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../App';
import AnimatedLogin from './AnimatedLogin';

const Login = () => {
  const { login } = useContext(AuthContext);

  const handleLogin = async (email, password) => {
    try {
      const response = await axios.post('/auth/login', { email, password });
      login(response.data.user, response.data.access_token);
    } catch (err) {
      throw new Error(err.response?.data?.error || 'Login failed');
    }
  };

  return <AnimatedLogin onLogin={handleLogin} />;
};

export default Login;