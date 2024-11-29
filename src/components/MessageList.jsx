/*
  Author: Mark Allen G. Bobadilla
  Date: November 2024
  Github: mgachiee
*/

import ReactMarkDown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import BotIcon from '../assets/bot.png';
import MessageDefault from './MessageDefault';
import ButtonOptions from './ButtonOptions';

export default function MessageList({ messages, defaultButtons, optionButtons, handlePrompt }) {
  // initially set to false
  let isOptions = false;

  // will return all the session's messages
  return (
    <div className="message-list">
      {
        messages.map((message) => {
          const isUserMessage = message.role === 'user';
          return (
            <div
              key={message.id}
              className={`message-wrapper-${isUserMessage ? 'user' : 'bot'}`}
            >
              {/* show image preview if attached */}
              {message.filename && (
                <img src={`src\\backend\\uploads\\${message.filename}`} alt="Uploaded Image" className='image-attachment'/>
              )}
              {!isUserMessage ? <img src={BotIcon} alt="User Icon" id='profile-icon' style={{marginRight: '5px'}}/> : ''}
              {/* set the isOptions to true only if the message.options is not undefined */}
              {message.options !== undefined && (isOptions = true)}
              <div className={`message ${isUserMessage ? 'user-message' : 'bot-message'}`}>
                <ReactMarkDown remarkPlugins={[remarkGfm]}>
                  { message?.content ?
                    (typeof message.content === 'string' ? message.content : message.content.content || 'No! content available.')
                    : 'No content available'
                  }
                </ReactMarkDown>
              </div>
            </div>
          )
        }
      )}

      {/* handles default and option buttons conditionally */}
      {defaultButtons && <MessageDefault handleButtons={handlePrompt}/>}
      {isOptions && <ButtonOptions index={optionButtons} handleButtons={handlePrompt}/>}
    </div>
  );
}