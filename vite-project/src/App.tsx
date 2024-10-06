import { useState, useEffect } from 'react'
import { io } from 'socket.io-client';
import './App.css'
import ReactMarkdown from 'react-markdown';

type WebMessage = {
  Date: Date,
  Info: string
}

function App() {
  

  const [messages, setMessages] = useState<WebMessage[]>([]);

  useEffect(()=>{
    fetch('http://localhost:5001/get_data', 
      {method: 'GET', // HTTP method
      headers: {
          'Content-Type': 'application/json', // Specify content type as JSON
      }} // Convert data object to JSON string
    )
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse JSON response
    })
    .then((msg: WebMessage[]) => {
        const formattedmsg = msg.map(x => {return {...x, Date: new Date(x.Date)}})
        setMessages((prevMessages: WebMessage[]) => [...prevMessages, ...formattedmsg])
    })
    .catch(error => {
        console.error('Error:', error); // Handle any errors
    });
  }, [])

  useEffect(() => {
      const socket = io('http://localhost:5001');
      console.log("AWPODJ")

      socket.emit('RetrievePastMessages')

      // Listen for messages from the server
      socket.on('server_message', (msg: WebMessage) => {
        console.log(msg)
        setMessages((prevMessages: WebMessage[]) => [{Info: msg.Info, Date: new Date(msg.Date)}, ...prevMessages])
      });

      return () => {
          socket.off('server_message'); // Cleanup the listener on unmount
          socket.disconnect()
      };
  }, []);

  const FormattedMessages = messages.map(x => {
    
    return <div className='MessageEntry'>
        <h2>{x.Date.toString()}</h2>
        <ReactMarkdown>{x.Info}</ReactMarkdown>
      </div>
  })

  return (
    <>
      <div className='Main'>
        <h1 className='Title'>
          CyberAttack Detector
        </h1>
        <h3 className='Description'>A cybercatching software that helps non-tech savvy people understand cyber threats to their server.</h3>
        <div className='Messages-list'>
          {FormattedMessages}
        </div>
        
      </div>
    </>
  )
}

export default App
