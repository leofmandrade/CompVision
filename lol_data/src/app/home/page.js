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
                    {!image && ( // Só exibe o botão se não houver imagem carregada
                        <>
                            <label htmlFor="file-upload" className={styles.customFileUpload}>
                                Upload Image
                            </label>
                            <input id="file-upload" type="file" onChange={handleImageChange} accept="image/*" className={styles.fileInput} />
                        </>
                    )}
                    {image && <img src={image} alt="Uploaded" className={styles.uploadedImage} />}
                </div>
            </div>
        </main>
    );
};

export default HomePage;
