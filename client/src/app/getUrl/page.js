"use client";
import React, { useState } from 'react';
import styles from './page.module.css';

const HomePage = () => {
    const [imageUrl, setImageUrl] = useState('');
    const [showNextPage, setShowNextPage] = useState(false);

    const handleInputChange = (event) => {
        setImageUrl(event.target.value);
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




    const downloadFiles = async () => {
        try {
            const response = await fetch('http://localhost:8080/download', {
                method: 'GET',
            });
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'dados_files.zip';
            document.body.appendChild(a);
            a.click();
            a.remove();
            setShowNextPage(true);
        } catch (error) {
            console.error('Error:', error);
            alert('File download failed');
        }
    };

    const runAllTasks = async () => {
        try {
            await uploadImage();
            await downloadFiles();
            alert('All tasks completed successfully');
            setShowNextPage(true);
        } catch (error) {
            console.error('Error:', error);
            alert('One or more tasks failed');
        }
    };

    return (
        <main className={styles.main}>
            <h1 className={styles.title}>LEAGUE OF LEGENDS DATA</h1>
            <div className={styles.center}>
                <div className={styles.coluna}>
                    <input 
                        id="image-url" 
                        type="text" 
                        placeholder="Enter image URL" 
                        className={styles.urlInput} 
                        value={imageUrl} 
                        onChange={handleInputChange} 
                    />
                    <button onClick={runAllTasks} className={styles.uploadButton2}>RUN</button>
                    {/* <div className={styles.row} >
                    <button onClick={uploadImage} className={styles.uploadButton}>GET URL</button>
                    <button onClick={tryCode} className={styles.uploadButton}>TRY THE CODE</button>
                    <button onClick={tryCSV} className={styles.uploadButton}>TRY THE CSV</button>
                    <button onClick={getData} className={styles.uploadButton}>GET THE DATA</button>
                    <button onClick={processData} className={styles.uploadButton}>PROCESS THE DATA</button>*/}
                    <button onClick={downloadFiles} className={styles.uploadButton}>DOWNLOAD FILES</button>
                </div>
            </div>
            {showNextPage && (
                <button onClick={() => window.location.href='/results'} className={styles.uploadButton}>
                    Go to Results Page
                </button>
            )}
        </main>
    );
};

export default HomePage;
