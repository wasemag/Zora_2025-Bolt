import React from 'react';
import { useNavigate } from 'react-router-dom';

function ReadingForm({ question, setQuestion, userInfo, setUserInfo, onSubmit, selectedCards }) {
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (selectedCards.length !== 3) {
      alert("Please select exactly 3 cards for your reading.");
      return;
    }
    onSubmit();
    navigate('/reading-result');
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'question') {
      setQuestion(value);
    } else {
      setUserInfo(prevState => ({ ...prevState, [name]: value }));
    }
  };


  return (
    <div className="reading-form bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Get Your Tarot Reading</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label htmlFor="name" className="block text-gray-700 text-sm font-bold mb-2">Name:</label>
          <input type="text" id="name" name="name" value={userInfo.name} onChange={handleChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" required />
        </div>
        <div>
          <label htmlFor="dob" className="block text-gray-700 text-sm font-bold mb-2">Date of Birth:</label>
          <input type="date" id="dob" name="dob" value={userInfo.dob} onChange={handleChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" required />
        </div>
        <div>
          <label htmlFor="gender" className="block text-gray-700 text-sm font-bold mb-2">Gender:</label>
          <select id="gender" name="gender" value={userInfo.gender} onChange={handleChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" required>
            <option value="">Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div>
          <label htmlFor="question" className="block text-gray-700 text-sm font-bold mb-2">Your Question:</label>
          <textarea id="question" name="question" value={question} onChange={handleChange} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" required></textarea>
        </div>
        <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Get Reading</button>
      </form>
    </div>
  );
}

export default ReadingForm;
