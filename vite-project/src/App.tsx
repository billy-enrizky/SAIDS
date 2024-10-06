import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import ReactMarkdown from 'react-markdown';
import { ChevronDown, ChevronUp } from 'lucide-react';

import './App.css';

// Add this import for the Google Fonts
import { Helmet } from 'react-helmet';

type WebMessage = {
  Date: Date;
  Info: string;
};

const MessageCard: React.FC<{ message: WebMessage }> = ({ message }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => setIsExpanded(!isExpanded);

  return (
    <div className="message-card">
      <div className="message-date">{message.Date.toLocaleString()}</div>
      <div className={`message-content ${isExpanded ? 'expanded' : ''}`}>
        <ReactMarkdown>{message.Info}</ReactMarkdown>
      </div>
      <button className="expand-button" onClick={toggleExpand}>
        {isExpanded ? (
          <>
            <ChevronUp size={16} /> See Less
          </>
        ) : (
          <>
            <ChevronDown size={16} /> See More
          </>
        )}
      </button>
    </div>
  );
};

function App() {
  const [messages, setMessages] = useState<WebMessage[]>([]);

  useEffect(() => {
    fetch('http://localhost:5001/get_data', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((msg: WebMessage[]) => {
        const formattedMsg = msg.map((x) => ({ ...x, Date: new Date(x.Date) }));
        setMessages((prevMessages) => [...prevMessages, ...formattedMsg]);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }, []);

  useEffect(() => {
    const socket = io('http://localhost:5001');

    socket.emit('RetrievePastMessages');

    socket.on('server_message', (msg: WebMessage) => {
      setMessages((prevMessages) => [
        { Info: msg.Info, Date: new Date(msg.Date) },
        ...prevMessages,
      ]);
    });

    return () => {
      socket.off('server_message');
      socket.disconnect();
    };
  }, []);

  return (
    <>
      <Helmet>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&family=Orbitron:wght@400;700&display=swap" rel="stylesheet" />
      </Helmet>
      <div className="app">
        <header className="app-header">
          <h1>SAIDS - Smart Alert Intrusion Detection System</h1>
          <h3>A cybercatching software that helps non-tech savvy people understand cyber threats to their server.</h3>
        </header>
        <main className="messages-container">
          {messages.map((message, index) => (
            <MessageCard key={index} message={message} />
          ))}
        </main>
      </div>
    </>
  );
}

export default App;