// filepath: d:\coding\AquaChainMed\frontend\src\App.tsx
import React, { useState } from "react";
import "./App.css";
import Navigation from "./components/Navigation";
import CardLayout from "./components/CardLayout";
import UploadPage from "./UploadPage";

function App() {
  const [isNavbarExpanded, setIsNavbarExpanded] = useState(false);

  return (
    <div className="App">
      <Navigation onExpand={setIsNavbarExpanded} />
      <CardLayout isNavbarExpanded={isNavbarExpanded}>
        <UploadPage />
      </CardLayout>
    </div>
  );
}

export default App;