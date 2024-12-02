import './MainPage.css'; // Import the CSS file

const Protected = () => {
  return (
    <div className="protected-content">
      <h1>Protected Page</h1>
      <p>This page is only accessible to authenticated users.</p>
    </div>
  );
};  

export default Protected;
