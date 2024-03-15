import React from 'react';
import './Header.css'

function Header() {
    return (
      <header className="header">
        <div className="header-left">
          <h1>Condition Monitoring Overview</h1>
        </div>
        <div className="header-right">
          <div className="user-initials">KD</div>
          <div className="user-name">KDDI Asia Pacific</div>
        </div>
      </header>
    );
  }
  
export default Header;