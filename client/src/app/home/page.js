"use client";
import React, { useState } from 'react';
import styles from './page.module.css';

const HomePage = () => {
    const [image, setImage] = useState(null);
    const [file, setFile] = useState(null);

    const handleImageChange = (event) => {
        const file = event.target.files[0];
        if (file && file.type.substr(0, 5) === "image") {
            setImage(URL.createObjectURL(file));
            setFile(file);
            
        } else {
            setImage(null);
            setFile(null);
        }
    };

    const uploadImage = async () => {
        if (!file) {
            alert("Please select an image first!");
            return;
        }
    
        const formData = new FormData();
        formData.append('image', file); // 'image' é a chave esperada pelo backend
    
        try {
            const response = await fetch('http://localhost:8080/api', {
                method: 'POST',
                body: formData,
            });
    
            const result = await response.json();
            console.log(result);
            alert('Upload successful');
        } catch (error) {
            console.error('Error:', error);
            alert('Upload failed');
        }
    };
    

    return (
        <main className={styles.main}> 
            <h1 className={styles.title}>LEAGUE OF LEGENDS DATA</h1>
            <div className={styles.center}>
                <div>
                    {!image && (
                        <>
                            <label htmlFor="file-upload" className={styles.customFileUpload}>
                                UPLOAD IMAGE
                            </label>
                            <input id="file-upload" type="file" onChange={handleImageChange} accept="image/*" className={styles.fileInput} />
                            <input type="text" placeholder="URL" className={styles.urlInput} />
                        </>
                    )}
                    {image && (
                        <>
                            <div>A</div>
                            <img src={image} alt="Uploaded" className={styles.uploadedImage} />
                            <button onClick={uploadImage} className={styles.uploadButton}>Send Image</button>
                        </>
                    )}
                </div>
            </div>
        </main>
    );
};

export default HomePage;
