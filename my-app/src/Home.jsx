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

    const getAccessTokenAndVerify = async () => {
      try {
        const token = await oktaAuth.tokenManager.get("accessToken");
        await verifyUser(token.accessToken);
      } catch (error) {
        setIsVerified(false);
        setError('Failed to retrieve access token');
        console.error('Error retrieving access token:', error);
      }
    };

    getAccessTokenAndVerify();
  }, [authState, oktaAuth]);

  if (!authState) return <div>Loading...</div>;
  if (!authState.isAuthenticated || error) return <LoginPage />;

  if (isVerified) return <MainPage />;
  return <div>Loading user verification...</div>;
};

export default Home;
