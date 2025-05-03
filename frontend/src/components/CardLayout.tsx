import React from "react";
import "./CardLayout.css";

interface CardLayoutProps {
  children: React.ReactNode;
  isNavbarExpanded: boolean;
}

const CardLayout: React.FC<CardLayoutProps> = ({ children, isNavbarExpanded }) => {
  console.log("Navbar expanded:", isNavbarExpanded); // Debug log

  return (
    <div
      className="card-layout"
      style={{ marginTop: isNavbarExpanded ? "380px" : "180px" }} // Adjust dynamically
    >
      {children}
    </div>
  );
};

export default CardLayout;