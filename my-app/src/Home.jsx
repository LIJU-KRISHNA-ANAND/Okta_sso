import { useOktaAuth } from '@okta/okta-react';
import { useState, useEffect } from 'react';
import LoginPage from './components/auth/LoginPage';
import MainPage from './components/main/MainPage';

const Home = () => {
  const { oktaAuth, authState } = useOktaAuth();
  const [isVerified, setIsVerified] = useState(false);
  const [error, setError] = useState(null);

  const verifyUser = async (accessToken) => {
    try {
      const response = await fetch('http://localhost:5000/verify', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();

      if (response.ok) {
        setIsVerified(true);
        console.log('User verified:', data);
      } else {
        throw new Error(data.error || 'Verification failed');
      }
    } catch (error) {
      setIsVerified(false);
      setError(error.message || 'An error occurred during verification');
      console.error('Error during verification:', error);
    }
  };

  useEffect(() => {
    if (!authState?.isAuthenticated) {
      return;
    }

    const verifyUser = async () => {
      if (!authState.isAuthenticated) {
        return;
      }

      try {
        const token = await oktaAuth.tokenManager.get("accessToken");
        console.log(token.accessToken)
        const response = await fetch('http://localhost:5000/verify', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token.accessToken}`,
            'Content-Type': 'application/json'
          }
        });

        const data = await response.json();

        if (response.ok) {
          console.log('User verified and stored:', data);
          setIsVerified(true);
        } else {
          console.error('Error:', data.error);
          setIsVerified(false);
          setError(data.error);
        }
      } catch (error) {
        console.error('Error during verification:', error);
        setIsVerified(false);
        setError('An error occurred during verification');
      }
    };

    verifyUser();
  }, [authState, oktaAuth]);

  if (!authState) {
    return <div>Loading...</div>;
  }

  if (!authState.isAuthenticated) {
    return <LoginPage />;
  }

  if (error) {
    return <LoginPage />;
  }

  if (isVerified) {
    return <MainPage />;
  }

  return <div>Loading user verification...</div>;
};

export default Home;
