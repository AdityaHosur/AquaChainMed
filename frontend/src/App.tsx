import React, { useState } from "react";
import "./App.css";
import Navigation from "./components/Navigation";
import CardLayout from "./components/CardLayout";
import UploadPage from "./UploadPage";
import Verify from "./Verify";

function App() {
  const [isNavbarExpanded, setIsNavbarExpanded] = useState(false);
  const [currentPage, setCurrentPage] = useState("Upload"); // Default to Upload page

  const renderPage = () => {
    switch (currentPage) {
      case "Upload":
        return <UploadPage />;
      case "Verify":
        return <Verify />;
      default:
        return <UploadPage />;
    }
  };

  return (
    <div className="App">
      <Navigation
        onExpand={setIsNavbarExpanded} // Pass the state updater for navbar expansion
        onNavigate={setCurrentPage} // Pass the navigation handler
      />
      <CardLayout isNavbarExpanded={isNavbarExpanded}>
        {renderPage()}
      </CardLayout>
    </div>
  );
}

export default App;