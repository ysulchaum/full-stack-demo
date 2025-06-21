import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);
  const [isClicked, setIsClicked] = useState(false);

  const API_BASE_URL = 'http://synthpartner';

  // Fetch initial count on component mount
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/count`)
      .then((response) => response.json())
      .then((data) => setCount(data.count))
      .catch((error) => console.error('Error fetching count:', error));
  }, []);

  // Handle button click
  const handleClick = async () => {
    setIsClicked(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/click`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      setCount(data.count);
    } catch (error) {
      console.error('Error sending click:', error);
    } finally {
      setIsClicked(false);
    }
  };

  return (
    <div className="App">
      <h1>Click Counter</h1>
      <p>Total Clicks: {count}</p>
      <button onClick={handleClick} disabled={isClicked}>
        {isClicked ? 'Processing...' : 'Click Me'}
      </button>
    </div>
  );
}

export default App;