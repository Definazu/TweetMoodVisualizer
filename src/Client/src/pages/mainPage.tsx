import React, {useState} from 'react';
import SVGMap from '../components/SVGMap.tsx';
import paths from '../components/pathes.tsx';
import DataTable from "../components/DataTable.tsx";
import FileUploader from "../components/FileUploader.tsx";
import axios from "axios";

const App: React.FC = () => {
    const [colorData, setColorData] = useState<Record<string, string>>({});

    const handleClearMap = () => {
        const clearedColorData: Record<string, string> = {};
        paths.forEach(path => {
            clearedColorData[path.id] = "#c2c2c2";
        });
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
        setTimeout(() => {
            window.scrollTo({
                top: 1400,
                behavior: "smooth"
            });
        }, 10000);
        setColorData(clearedColorData);
    };

    const handleColorizeMap = async (tableName: string) => {
        try {
            const response = await axios.get(`http://localhost:5000/analyze/${tableName}`);
            setColorData(response.data);
        } catch (error) {
            console.error("Error fetching color data:", error);
        }
    };

    return (
        <>
            <SVGMap paths={paths} colorData={colorData} />
            <FileUploader/>
            <DataTable onColorizeMap={handleColorizeMap} onClearMap={handleClearMap} />
        </>
    );
};

export default App;