"use client";
import React, { useEffect, useState } from 'react';
import styles from './page.module.css';
import Image from 'next/image';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import championIcons from './importChampionIcons';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const Results = () => {
    const [champions, setChampions] = useState([]);
    const [championStats, setChampionStats] = useState([]);
    const [selectedChampion, setSelectedChampion] = useState(1);
    const [selectedChampionName, setSelectedChampionName] = useState('');

    const goBack = () => {
        window.history.back();
    };

    const getIcons = async () => {
        try {
            const response = await fetch('https://compvision-production.up.railway.app/results', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const result = await response.json();
            const championsList = [];
            for (let i = 1; i <= 10; i++) {
                championsList.push(result[`champ${i}`]);
            }
            setChampions(championsList);
        } catch (error) {
            console.error('Error:', error);
            alert('Data processing failed');
        }
    };

    const getEachChampData = async () => {
        try {
            const response = await fetch('https://compvision-production.up.railway.app/eachChampData', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const result = await response.json();
            const champData = getChampionData(result, selectedChampion);
            setChampionStats(champData);
            setSelectedChampionName(champData[0].CHAMPION);
        } catch (error) {
            console.error('Error:', error);
            alert('Data processing failed');
        }
    };

    const getChampionData = (data, champion) => {
        const championData = data[`champ${champion}`];
        if (!championData) {
            throw new Error(`Champion ${champion} not found`);
        }

        return championData;
    };

    const handleImageClick = (index) => {
        setSelectedChampion(index + 1);
    };

    useEffect(() => {
        if (champions.length > 0) {
            getEachChampData();
        }
    }, [selectedChampion]);

    const fillMissingData = (data) => {
        for (let i = 1; i < data.length; i++) {
            if (isNaN(data[i])) {
                data[i] = data[i - 1];
            }
        }
        return data;
    };

    const processedChampionStats = {
        labels: championStats.map(stat => stat.frame),
        datasets: [
            {
                label: 'Kills',
                data: fillMissingData(championStats.map(stat => stat.KILLS)),
                borderColor: 'rgba(0, 192, 0, 1)',
                backgroundColor: 'rgba(0, 192, 0, 0.2)',
                fill: false,
            },
            {
                label: 'Deaths',
                data: fillMissingData(championStats.map(stat => stat.DEATHS)),
                borderColor: 'rgba(255, 10, 30, 1)',
                backgroundColor: 'rgba(255, 10, 30, 0.2)',
                fill: false,
            },
            {
                label: 'Assists',
                data: fillMissingData(championStats.map(stat => stat.ASSISTS)),
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: false,
            },
            {
                label: 'Farm',
                data: fillMissingData(championStats.map(stat => stat.FARM)),
                borderColor: 'rgba(255, 255, 0, 1)',
                backgroundColor: 'rgba(255, 255, 0, 0.2)',
                fill: false,
            }
        ]
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Champion Stats Over Time',
            },
        },
    };

    return (
        <main className={styles.main}>
            <h1 className={styles.title}>LEAGUE OF LEGENDS DATA</h1>
            <div className={styles.center}>
                <div className={styles.column}>
                    <button className={styles.uploadButton} onClick={goBack}>Back</button>
                    <button className={styles.uploadButton} onClick={getIcons}>Process Results</button>
                </div>
            </div>
            {selectedChampionName && <h3 className={styles.champname}>{selectedChampionName}</h3>}
            {selectedChampionName && <Image 
                src={championIcons[`${selectedChampionName}.png`]}
                alt={selectedChampionName}
                className={styles.championIcon}
            />}
            <div className={styles.championsRectangle}>
                <div className={styles.championsDisposition}>
                    <h2 className={styles.textTeam}>Blue Team:</h2>
                    <div className={styles.championsContainer}>
                        {champions.slice(0, 5).map((champion, index) => (
                            <div key={index} className={`${styles.champion} ${styles.blueBorder}`} onClick={() => handleImageClick(index)}>
                                <Image 
                                    src={championIcons[`${champion}.png`]}
                                    alt={champion[0].CHAMPION}
                                    className={styles.championIcon}
                                />
                            </div>
                        ))}
                    </div>
                    <h2 className={styles.textTeam}>Red Team:</h2>
                    <div className={styles.championsContainer}>
                        {champions.slice(5).map((champion, index) => (
                            <div key={index} className={`${styles.champion} ${styles.redBorder}`} onClick={() => handleImageClick(index + 5)}>
                                <Image 
                                    src={championIcons[`${champion}.png`]}
                                    alt={champion[0].CHAMPION}
                                    className={styles.championIcon}
                                />
                            </div>
                        ))}
                    </div>
                </div>
                <div className={styles.graphs}>
                    {championStats.length > 0 && (
                        <Line data={processedChampionStats} options={options} />
                    )}
                </div>
            </div>
        </main>
    );
};

export default Results;
