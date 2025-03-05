import React, { useEffect, useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const { auth, setAuth } = useContext(AuthContext);
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Redirect to login if the user is not authenticated
  useEffect(() => {
    if (!auth?.token) {
      navigate("/login");
      return;
    }

    const fetchUserData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/did", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${auth.token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch user data");
        }

        const data = await response.json();
        setUserData(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchUserData();
  }, [auth, navigate]);

  // Logout function
  const handleLogout = () => {
    setAuth(null);
    navigate("/login");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Welcome to Your Dashboard</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {userData ? (
        <div>
          <p><strong>Username:</strong> {userData.username}</p>
          <p><strong>Your DID:</strong> {userData.did}</p>
          <p><strong>Public Key:</strong></p>
          <textarea
            readOnly
            value={userData.public_key}
            style={{
              width: "80%",
              height: "100px",
              resize: "none",
              padding: "10px",
            }}
          />
          <br />
          <button onClick={handleLogout} style={{ marginTop: "20px", padding: "10px 20px", cursor: "pointer" }}>
            Logout
          </button>
        </div>
      ) : (
        <p>Loading dashboard...</p>
      )}
    </div>
  );
};

export default Dashboard;
