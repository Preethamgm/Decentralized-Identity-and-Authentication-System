import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useState(() => {
        const token = localStorage.getItem("token");
        return token ? { token } : null;
    });

    useEffect(() => {
        if (auth?.token) {
            localStorage.setItem("token", auth.token);
        } else {
            localStorage.removeItem("token");
        }
    }, [auth]);

    return (
        <AuthContext.Provider value={{ auth, setAuth }}>
            {children}
        </AuthContext.Provider>
    );
};
