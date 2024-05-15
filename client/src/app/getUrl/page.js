"use client";
import React, { useState } from 'react';
import styles from './page.module.css';

const HomePage = () => {
    const [imageUrl, setImageUrl] = useState('');

    const handleInputChange = (event) => {
        setImageUrl(event.target.value);
    };

    const processData = async () => {
        try {
            const response = await fetch('http://localhost:8080/process', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const result = await response.json();
            console.log(result);
            alert('Data processed successfully');
        }
        catch (error) {
            console.error('Error:', error);
            alert('Data processing failed');
        }
    };
    

    const tryCode = async () => {
        try {
            const response = await fetch('http://localhost:8080/code', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const result = await response.json();
            console.log(result);
            alert('Code executed successfully');
        } catch (error) {
            console.error('Error:', error);
            alert('Code execution failed');
        }
    };

    const uploadImage = async () => {
        console.log(imageUrl);  
        if (!imageUrl) {
            alert("Please enter an image URL!");
            return;
        }

        try {
            const response = await fetch('http://localhost:8080/api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ imageUrl }),
            });
            const result = await response.json();
            console.log(result);
            alert('Upload successful');
        } catch (error) {
            console.error('Error:', error);
            alert('Upload failed');
        }
    };

    const getData = async () => {
        try {
            const response = await fetch('http://localhost:8080/data', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const result = await response.json();
            console.log(result);
            alert('Data fetched successfully');
        } catch (error) {
            console.error('Error:', error);
            alert('Data fetch failed');
        }
    }

    const tryCSV = async () => {
        try {
            const response = await fetch('http://localhost:8080/csv', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const result = await response.json();
            console.log(result);
            alert('CSV generated successfully');
        } catch (error) {
            console.error('Error:', error);
            alert('CSV generation failed');
        }
    }
    



    return (
        <main className={styles.main}>
            <h1 className={styles.title}>LEAGUE OF LEGENDS DATA</h1>
            <div className={styles.center}>
                <div>
                    <input 
                        id="image-url" 
                        type="text" 
                        placeholder="Enter image URL" 
                        className={styles.urlInput} 
                        value={imageUrl} 
                        onChange={handleInputChange} 
                    />
                    <button onClick={uploadImage} className={styles.uploadButton}>GET URL</button>
                    <button onClick={tryCode} className={styles.uploadButton}>TRY THE CODE</button>
                    <button onClick={tryCSV} className={styles.uploadButton}>TRY THE CSV</button>
                    <button onClick={getData} className={styles.uploadButton}>GET THE DATA</button>
                    <button onClick={processData} className={styles.uploadButton}>PROCESS THE DATA</button>




                </div>
            </div>
        </main>
    );
};

export default HomePage;
