import { useOktaAuth } from "@okta/okta-react";
import './MainPage.css';

const MainPage = () => {
    const { oktaAuth } = useOktaAuth();
    const logout = async () => oktaAuth.signOut('/');
    
    return (
        <div className="container">
            <div className="main-content">
                <p>Logged in!</p>
                <div className="protected-content">
                    <h1>Protected Page</h1>
                    <p>This page is only accessible to authenticated users.</p>
                </div>
                <button onClick={logout}>Logout</button>
            </div>
        </div>
    );
}

export default MainPage;
