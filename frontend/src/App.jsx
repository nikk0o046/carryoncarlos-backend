import React, { useState } from 'react'
import './App.css' // Import the CSS file

function App() {
  const [user_request, setQuery] = useState('')
  const [results, setResults] = useState('')

  const handleInputChange = (event) => {
    setQuery(event.target.value)
  }

  const handleSearchClick = async () => {
    const response = await fetch('http://localhost:5000/search_flights', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({user_request})
    })

    const data = await response.json()
    setResults(data.join('\n'))
  }

  return (
    <div className="app">
      <h3>✈️ Just type what kind of trip you are looking for and when you'd want to go 🌍</h3>
      <textarea className="search-input" value={user_request} onChange={handleInputChange} />
      <button onClick={handleSearchClick}>Search</button>
      <pre>{results}</pre>
    </div>
  )
}

export default App
