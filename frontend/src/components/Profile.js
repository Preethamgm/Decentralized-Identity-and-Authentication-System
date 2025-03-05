import React, { useEffect, useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Profile = () => {
  const { auth } = useContext(AuthContext);
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (!auth?.token) {
      navigate("/login");
      return;
    }

    const fetchProfile = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/did", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${auth.token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch profile data");
        }

        const data = await response.json();
        setProfileData(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchProfile();
  }, [auth, navigate]);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Profile</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {profileData ? (
        <div>
          <p><strong>Username:</strong> {profileData.username}</p>
          <p><strong>DID:</strong> {profileData.did}</p>
          <p><strong>Public Key:</strong></p>
          <textarea
            readOnly
            value={profileData.public_key}
            style={{
              width: "80%",
              height: "100px",
              resize: "none",
              padding: "10px",
            }}
          />
        </div>
      ) : (
        <p>Loading profile...</p>
      )}
    </div>
  );
};

export default Profile;
