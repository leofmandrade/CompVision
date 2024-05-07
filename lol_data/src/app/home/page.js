"use client";
import React, { useState } from 'react';
import styles from './page.module.css';

const HomePage = () => {
    const [image, setImage] = useState(null);

    const handleImageChange = (event) => {
        const file = event.target.files[0];
        if (file && file.type.substr(0, 5) === "image") {
            setImage(URL.createObjectURL(file));
        } else {
            setImage(null);
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
                            {/* input de texto para o usuario escrever uma url */}
                            <input id="file-upload" type="file" onChange={handleImageChange} accept="image/*" className={styles.fileInput} />
                            <input type="text" placeholder="URL" className={styles.urlInput} />

                        </>
                    )}
                    {image && <img src={image} alt="Uploaded" className={styles.uploadedImage} />}
                </div>
            </div>
        </main>
    );
};

export default HomePage;
