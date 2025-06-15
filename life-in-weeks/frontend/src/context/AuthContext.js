import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, signup as apiSignup } from '../services/auth';

export const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
      setCurrentUser(user);
    }
    setLoading(false);
  }, []);

  const signup = async (email, password, birthdate) => {
  try {
    const response = await apiSignup(email, password, birthdate);
    const user = {
      email: email,
      token: response.data.access_token  // Make sure this matches backend response
    };
    localStorage.setItem('user', JSON.stringify(user));
    setCurrentUser(user);
    return user;
  } catch (error) {
    throw new Error('Signup failed');
  }
};

const login = async (email, password) => {
  try {
    const response = await apiLogin(email, password);
    const user = {
      email: email,
      token: response.data.access_token  // Make sure this matches backend response
    };
    localStorage.setItem('user', JSON.stringify(user));
    setCurrentUser(user);
    return user;
  } catch (error) {
    throw new Error('Login failed');
  }
};

  const logout = () => {
    localStorage.removeItem('user');
    setCurrentUser(null);
  };

  const value = {
    currentUser,
    login,
    signup,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}