import React, { useState } from "react";
import "./Navigation.css";

interface NavigationProps {
  onExpand: (isExpanded: boolean) => void;
  onNavigate: (page: string) => void;
}

const Navigation: React.FC<NavigationProps> = ({ onExpand, onNavigate }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    const newState = !isMenuOpen;
    setIsMenuOpen(newState);
    onExpand(newState); // Notify parent about the expanded state
  };

  const handleNavigation = (page: string) => {
    onNavigate(page); // Notify parent about the selected page
    setIsMenuOpen(false); // Close the menu after navigation
    onExpand(false); // Notify parent that the menu is closed
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
        <li>
          <a href="#Upload" onClick={() => handleNavigation("Upload")}>
            Upload
          </a>
        </li>
        <li>
          <a href="#Verify" onClick={() => handleNavigation("Verify")}>
            Verify
          </a>
        </li>
      </ul>
    </nav>
  );
};

export default Navigation;