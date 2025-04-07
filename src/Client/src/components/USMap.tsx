import React, { useState } from "react";

interface USMapProps {
    onStateClick?: (stateCode: string) => void;
}
const USMap: React.FC<USMapProps> = ({ onStateClick }) => {
    const [colors, setColors] = useState<{ [key: string]: string }>({});

    const handleStateClick = (stateCode: string) => {
        const newColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`; // Генерация случайного цвета
        setColors((prevColors) => ({
            ...prevColors,
            [stateCode]: newColor,
        }));
        onStateClick?.(stateCode); // Вызов колбэка, если он передан
    };

    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1000 589"
            width="100%"
            height="100%"
        >
            {Object.entries(colors).map(([stateCode, color]) => (
                <path
                    key={stateCode}
                    id={stateCode}
                    data-name={stateCode}
                    fill={color}
                    onClick={() => handleStateClick(stateCode)}
                    style={{cursor: "pointer"}}
                />
            ))}

            <path
                id="MA"
                data-name="Massachusetts"
                data-id="MA"
                d="m 956.31178,153.05085 -0.29118,-0.19412 0,0.29119 0.29118,-0.0971 z m -2.91189,-2.6207 0.67944,-0.29119 0,-0.38825 -0.67944,0.67944 z m 12.03583,-7.57092 -0.0971,-1.35889 -0.19412,-0.7765 0.29119,2.13539 z m -42.41659,-9.9975 -0.67944,0.29119 -5.5326,1.65007 -1.94126,0.67944 -2.23245,0.67944 -0.7765,0.29119 0,0.29119 0.29118,5.04728 0.29119,4.65903 0.29119,4.27078 0.48532,0.29119 1.74714,-0.48532 7.86211,-2.32951 0.19412,0.48531 13.97709,-5.33847 0.0971,0.19413 1.26182,-0.48532 4.4649,-1.74713 4.27078,5.14434 0,0 0.58238,-0.48531 0.29119,-1.45595 -0.0971,2.32952 0,0 0.97063,0 0.29119,1.16475 0.87357,1.65008 0,0 4.56197,-5.5326 3.78546,1.26182 0.87357,-1.94126 6.21204,-3.30015 -2.62071,-5.14435 0.67945,3.30015 -3.20309,2.42658 -3.59133,0.29119 -7.18267,-7.66799 -3.20309,-4.85315 3.20309,-3.39721 -3.30015,-0.19413 -1.35888,-3.20308 -0.0971,-0.19413 -5.53259,6.01791 -12.22996,4.07666 -3.97959,1.26182 0,0 z"
                fill={colors["MA"] || "#f9f9f9"}
                onClick={() => handleStateClick("MA")}
                style={{cursor: "pointer"}}
            />

        </svg>
    );
};

export default USMap;