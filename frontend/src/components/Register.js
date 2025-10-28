import React, { useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../App';
import AnimatedRegister from './AnimatedRegister';

const Register = () => {
  const { login } = useContext(AuthContext);

  const handleRegister = async (email, password) => {
    try {
      const response = await axios.post('/auth/register', { email, password });
      
      // Auto-login after successful registration
      const loginResponse = await axios.post('/auth/login', { email, password });
      login(loginResponse.data.user, loginResponse.data.access_token);
    } catch (err) {
      throw new Error(err.response?.data?.error || 'Registration failed');
    }
  };

  return <AnimatedRegister onRegister={handleRegister} />;
};

export default Register;