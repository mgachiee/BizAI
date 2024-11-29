/*
  Author: Mark Allen G. Bobadilla
  Date: November 2024
  Github: mgachiee
*/

import { useState } from 'react';
import MenuIcon from '../assets/menu-burger.png';
import Logo from '../assets/BizAI-Logo.png';
import './Components.css'

export default function NavBar() {
  const [showPopUp, setShowPopUp] = useState(false);

  // for hiding and showing popup
  const handlePopUp = () => {
    setShowPopUp((prevState) => !prevState);
  }

  return (
    <>
      <nav id="navbar">
        <img
          src={MenuIcon}
          alt="Hamburger Menu Icon"
          onClick={handlePopUp}
        />
        <img src={Logo} alt="BizAI Logo" id='bizai-logo'/>
      </nav>

      {/* will only appear if the state is true */}
      {showPopUp &&
        <section id='pop-up'>
          <p>About BizAI</p>
          <p>Chat with BizAI</p>
          <p>Loans and Plans</p>
        </section>
      }
    </>
  );
}