import React, { useState, useEffect, createContext } from 'react';
import './App.css';
import Header from './components/Header';
import Home from './components/Home'

const ServerEventsContext = createContext(null);

function App() {
  const [serverData, setServerData] = useState(null);

  useEffect(() => {
    const eventSource = new EventSource('http://10.0.122.233:5001');

    eventSource.onmessage = function (event) {
      const receivedData = JSON.parse(event.data);
      setServerData(receivedData); // Update server data in the context
    };

    //console.log(serverData);

    return () => {
      eventSource.close();
    };
  }, []);

  return (
    <div className="grid-container">
      <ServerEventsContext.Provider value={serverData}>
        <Header />
        <Home />
      </ServerEventsContext.Provider>
    </div>
  );
}

export default App;
export { ServerEventsContext };
