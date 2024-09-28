import { createContext, useState, useEffect } from "react";
import { useRouter } from "next/router";
import jwtDecode from "jwt-decode";
import axios from "axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      const decoded = jwtDecode(token);
      setUser({ id: decoded.sub });
    } else {
      router.push("/login");
    }
  }, []);

  const login = async (credential) => {
    try {
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/user/login`,
        {},
        {
          headers: {
            Authorization: credential,
          },
        }
      );
      localStorage.setItem("access_token", res.data.access_token);
      setUser(res.data.user);
      router.push("/chat");
    } catch (error) {
      console.error(error);
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
