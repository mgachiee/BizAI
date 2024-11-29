/*
  Author: Mark Allen G. Bobadilla
  Date: November 2024
  Github: mgachiee
*/

import { useState } from "react";
import PlusIcon from "../assets/add.png";
import SendIcon from "../assets/send.png";
import "./Components.css";

export default function InputField({ onSendPrompt }) {
  const [prompt, setPrompt] = useState('');
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);

  const handlePrompt = (e) => setPrompt(e.target.value);

  const handleSendClick = () => {
    onSendPrompt(prompt, file);
    // reset the states
    setPrompt('');
    setImage(null);
    setFile(null);
    setError(null);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendClick(); // call the send function
    }
  };

  const handleAttachment = () => document.getElementById('attachment').click();
  
  const handleImageChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      const reader = new FileReader();
      reader.onloadend = () => setImage(reader.result);
      reader.readAsDataURL(selectedFile);
      setFile(selectedFile);
      setError(null);
    }
  };

  return (
    <>
      {image && <img src={image} alt="Image Preview" className="image-preview" />}
      {error && <p className="error-message">{error}</p>}
      <form id="input-holder" onSubmit={(e) => { e.preventDefault(); handleSendClick(); }}>
        <img src={PlusIcon} alt="Attachment Icon" onClick={handleAttachment} />
        <input
          type="file"
          id="attachment"
          style={{ display: 'none' }}
          accept="image/*"
          onChange={handleImageChange}
        />
        <input
          type="text"
          id="prompt"
          placeholder="Need help in loaning?"
          autoComplete="off"
          value={prompt}
          onChange={handlePrompt}
          onKeyDown={handleKeyPress}
        />
        <img src={SendIcon} alt="Send Icon" onClick={handleSendClick} />
      </form>
    </>
  );
}
