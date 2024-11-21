import { useState, useEffect } from "react";
import "./Theme.css";
const savedTheme: string = localStorage.getItem("theme") || "light";

function Theme() {
  const [theme, setTheme] = useState(savedTheme);

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  return (
    <input id="button" type="button" value="Theme" onClick={toggleTheme} />
  );
}

export default Theme;
