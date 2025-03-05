import axios from "axios";

// ✅ Set the base API URL (Adjust if backend is deployed)
const API_BASE_URL = "http://127.0.0.1:8000";

// ✅ Create an Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ✅ Function to Signup
export const signup = async (userData) => {
  return api.post("/signup", userData);
};



// ✅ Function to Fetch User's DID
export const getUserDID = async (token) => {
  return api.get("/did", {
    headers: { Authorization: `Bearer ${token}` },
  });
};

// ✅ Function to Verify Signed Message
export const verifySignature = async (signatureData, token) => {
  return api.post("/verify", signatureData, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const login = async (email, password) => {
  const response = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }), // Ensure correct field names
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Login failed"); // Handle error
  }
  return data;
};



// ✅ Export the API instance
export default api;
