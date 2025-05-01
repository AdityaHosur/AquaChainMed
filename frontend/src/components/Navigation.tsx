import React, { useState } from "react";
import "./Navigation.css";

interface NavigationProps {
  onExpand: (isExpanded: boolean) => void;
}

const Navigation: React.FC<NavigationProps> = ({ onExpand }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    const newState = !isMenuOpen;
    setIsMenuOpen(newState);
    onExpand(newState); // Notify parent about the expanded state
  };

  return (
    <nav className={`navigation ${isMenuOpen ? "expanded" : ""}`}>
      <div className="nav-header">
        <div className="nav-logo">AquaMedChain</div>
        <button className="hamburger" onClick={toggleMenu}>
          <span className="line"></span>
          <span className="line"></span>
          <span className="line"></span>
        </button>
      </div>
      <ul className={`nav-links ${isMenuOpen ? "show" : ""}`}>
        <li><a href="#upload">Upload</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </nav>
  );
};

export default Navigation;