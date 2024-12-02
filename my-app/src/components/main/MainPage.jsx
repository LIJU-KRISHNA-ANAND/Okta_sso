import { useOktaAuth } from "@okta/okta-react";
import Protected from "./Protected";
import './MainPage.css'; // Import the CSS file

const MainPage = () => {
    const { oktaAuth } = useOktaAuth();
    const logout = async () => oktaAuth.signOut('/');
    
    return (
        <div className="container">
            <div className="main-content">
                <p>Logged in!</p>
                <Protected/>
                <button onClick={logout}>Logout</button>
            </div>
        </div>
    );
}

export default MainPage;
