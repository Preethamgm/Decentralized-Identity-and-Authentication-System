import React, { useState } from "react";
import { signup } from "../services/api";

const Signup = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const [responseMessage, setResponseMessage] = useState("");
  const [error, setError] = useState("");

  // ✅ Handle Input Change
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // ✅ Handle Form Submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponseMessage("");
    setError("");

    try {
      const response = await signup(formData);
      setResponseMessage(`Signup successful! Your DID: ${response.data.did}`);
    } catch (err) {
      setError(err.response?.data?.detail || "Signup failed. Try again.");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto", textAlign: "center" }}>
      <h2>Signup</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <br />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <br />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <br />
        <button type="submit">Signup</button>
      </form>
      {responseMessage && <p style={{ color: "green" }}>{responseMessage}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default Signup;
