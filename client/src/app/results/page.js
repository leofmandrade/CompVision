"use client";
import React, { useEffect, useState } from 'react';
import styles from './page.module.css';
import Image from 'next/image'
import championIcons from './importChampionIcons'; // Importa os ícones dos campeões

const Results = () => {
    const [champions, setChampions] = useState([]);

    const getIcons = async () => {
        try {
            const response = await fetch('http://localhost:8080/results', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const result = await response.json();
            console.log("Result: ", result);
            const championsList = [];
            for (let i = 1; i <= 10; i++) {
                championsList.push(result[`champ${i}`]);
            }
            
            setChampions(championsList);
            alert('Data processed successfully');
        }
        catch (error) {
            console.error('Error:', error);
            alert('Data processing failed');
        }
    };

    const getEachChampData = async () => {
        try {
            const response = await fetch('http://localhost:8080/eachChampData', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const result = await response.json();
            console.log("Result: ", result);
            alert('Data processed successfully');
        }

        catch (error) {
            console.error('Error:', error);
            alert('Data processing failed');
        }
    };

    const getResults = async () => {
        try{
            await getIcons();
            await getEachChampData();
            alert('Data processed successfully');

        }
        catch (error) {
            console.error('Error:', error);
            alert('Data processing failed');
        }
    };



    return (
        <main className={styles.main}>
            <h1 className={styles.title}>LEAGUE OF LEGENDS DATA</h1>
            <div className={styles.center}>
                <div className={styles.column}>
                    <button className={styles.uploadButton} onClick={getResults}>Process Results</button>
                </div>
            </div>
            <div className={styles.championsRectangle}>
                <div className={styles.championsDisposition}>
                    <h2 className={styles.textTeam}>Blue Team:</h2>
                    <div className={styles.championsContainer}>
                        {champions.slice(0, 5).map((champion, index) => (
                            <div key={index} className={`${styles.champion} ${styles.blueBorder}`}>
                                <Image 
                                    src={championIcons[`${champion}.png`]}
                                    alt={champion}
                                    className={styles.championIcon}
                                />
                            </div>
                        ))}
                    </div>
                    <h2 className={styles.textTeam}>Red Team:</h2>
                    <div className={styles.championsContainer}>
                        {champions.slice(5).map((champion, index) => (
                            <div key={index} className={`${styles.champion} ${styles.redBorder}`}>
                                <Image 
                                    src={championIcons[`${champion}.png`]}
                                    alt={champion}
                                    className={styles.championIcon}
                                />
                            </div>
                        ))}
                    </div>
                </div>
                <div className={styles.graphs}>
                    alert
                </div>
            </div>
           
        </main>
    );
};

export default Results;