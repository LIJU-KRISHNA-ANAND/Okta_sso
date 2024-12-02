import { useOktaAuth } from '@okta/okta-react';
import './LoginPage.css'; // Import the CSS file

const LoginPage = () => {
    const { oktaAuth } = useOktaAuth();

    const login = async () => oktaAuth.signInWithRedirect();  

    return (
        <div className="login-container">
            <p>Not Logged in yet</p>
            <button className="login-button" onClick={login}>Login</button>
        </div>
    );
}

export default LoginPage;
