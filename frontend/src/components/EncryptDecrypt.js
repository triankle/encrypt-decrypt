// src/components/EncryptDecrypt.js
import React, { useState } from 'react';
import axios from 'axios';

const EncryptDecrypt = () => {
    const [file, setFile] = useState(null);
    const [operation, setOperation] = useState('encrypt'); // Default operation
    const [statusMessage, setStatusMessage] = useState(''); // To store the status message
    const [statusType, setStatusType] = useState(''); // To define success or error message

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Determine the URL based on the operation
            const url = operation === 'encrypt' ? 'http://localhost:5000/encrypt' : 'http://localhost:5000/decrypt';

            const response = await axios.post(url, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            // Set the success message and its type
            setStatusMessage(response.data.message);
            setStatusType('success');  // Mark this as a success message
        } catch (error) {
            console.error('Error:', error);
            const errorMessage = error.response?.data?.error || 'An unknown error occurred';

            // Set the error message and its type
            setStatusMessage(errorMessage);
            setStatusType('error');  // Mark this as an error message
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} required />
                <select onChange={(e) => setOperation(e.target.value)} value={operation}>
                    <option value="encrypt">Encrypt</option>
                    <option value="decrypt">Decrypt</option>
                </select>
                <button type="submit">Submit</button>
            </form>

            {/* Display the status message dynamically below the form */}
            {statusMessage && (
                <p style={{ color: statusType === 'success' ? 'green' : 'red' }}>
                    {statusMessage}
                </p>
            )}
        </div>
    );
};

export default EncryptDecrypt;
