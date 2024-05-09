"use client"
import React, { useEffect, useState } from 'react';

function index(){
    useEffect(() => {
        fetch('http://localhost:8080/api')
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
        });
    }, []);

    return <div>index</div>
}

export default index;