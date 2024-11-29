/*
  Author: Mark Allen G. Bobadilla
  Date: November 2024
  Github: mgachiee
*/

import { useState } from 'react';
import axios from 'axios';
import NavBar from './components/NavBar';
import InputField from './components/InputField';
import MessageList from './components/MessageList';
import BotIcon from './assets/bot.png';
import { promptGreetings, isBPI, isYesOrNo, specificKeywords } from './util';
import './App.css';

// initialize optionIndex to undefined
let optionIndex = undefined; // will check if option buttons should be displayed
const customerId = '00000.01'; // sample id from the dump database

function App() {
  // messages initial state
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      account_id: 1104.2024,
      content: promptGreetings,
      filename: null,
    }
  ]);
  // state for generating response loader
  const [generatingResponse, setGeneratingResponse] = useState(false);
  const [fileUrl, setFileUrl] = useState(null);

  // check if the messages is in default state
  const defaultMessage = messages.length === 1;

  // handle prompts from the user
  const handleMessages = async (prompt, file) => {
    const userMessage = {
      id: messages.length + 1,
      role: 'user',
      account_id: '',
      content: prompt,
      filename: file ? file.name : null,
    };

    // add user message to the messages state
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setGeneratingResponse(true); // set loader to true
    
    try {
      optionIndex = undefined; // reset optionIndex to undefined
      let response = ''; // initialize response variable

      // create form data and append prompt
      const formData = new FormData();
      formData.append('prompt', prompt);

      // append file and history to form data
      if (file) {
        formData.append('attachment', file)
        formData.append('history', JSON.stringify(messages))
      }
      
      // check if the prompt is BPI-related or Bank-related
      if (isBPI(prompt)) {
        // fetch response from the Flask server
        const url = 'http://<localhost>:5000/bpi'; // use the trained model
        response = await axios.post(url, file ? formData : {
          query: `User: ${prompt}`,
          history: messages,
          customer_id: customerId,
        }, {
          headers: file ? {'Content-Type': 'multipart/form-data'} : undefined,
        });
      } else { // use the default model
        response = await axios.post('http://<localhost>/generate', file ? formData : {
          prompt: `User: ${prompt}`,
          history: messages,
          customer_id: customerId,
        });
      }
      
      // create bot message
      let botMessage = {
        id: messages.length + 2,
        role: 'assistant',
        account_id: 1104.2024,
        content: response.data.response,
        filename: null,
      };

      // check if the response contains specific keywords
      if (isYesOrNo(response.data.response)) {
        specificKeywords.forEach((keyword, index) => {
          if (response.data.response.toLowerCase().includes(keyword.toLowerCase())) {
            optionIndex = index;
            botMessage['options'] = index;
          }
        });
      }

      // fetch the file url from the response
      const file_url = response.data.file_url;
      setFileUrl(file_url);

      // add bot message to the messages state
      setMessages((prevMessages) => [...prevMessages, botMessage]);

    } catch (error) {
      console.error('Error fetching response from the Flask server:', error);
      // create error message
      const errorMessage = {
        id: messages.length + 2,
        role: 'assistant',
        account_id: 1104.2024,
        content: 'Sorry, there was an error processing your request.',
        filename: null,
      };
      // add error message to the messages state
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setGeneratingResponse(false); // always set loader to false after fetching response
    }
  };

  return (
    <>
      <NavBar />
      <MessageList messages={messages} defaultButtons={defaultMessage} optionButtons={optionIndex} handlePrompt={handleMessages} />
      {/* // display loader if generatingResponse is true */}
      {generatingResponse && 
        <div className="message-wrapper-bot">
          <img src={BotIcon} alt="" id='profile-icon' style={{marginRight: '5px'}}/>
          <div className='message bot-message'>
            <div className="message bot-message">
              <div className="loader"></div>
            </div>
          </div>
        </div>
      }
      { // display download url if fileUrl is not null
        fileUrl &&
        <a className='download-url' href={fileUrl}>Download Loan Statement ↓</a>
      }
      <InputField onSendPrompt={handleMessages}/>
    </>
  );
}

export default App;