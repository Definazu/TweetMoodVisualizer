import React, { useState, useEffect } from 'react';

interface TableData {
    id: string;
    name: string;
    value: string;
}

const DataTable: React.FC = () => {
    const [tableData, setTableData] = useState<TableData[]>([]);

    // Функция для загрузки данных с API
    const fetchData = async () => {
        try {
            const response = await fetch('https://your-api-url.com/data');
            const data = await response.json();
            setTableData(data);
        } catch (error) {
            console.error('Ошибка при загрузке данных:', error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            <button onClick={fetchData}>Обновить таблицу</button>
            <table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Имя</th>
                    <th>Значение</th>
                </tr>
                </thead>
                <tbody>
                {tableData.map((row) => (
                    <tr key={row.id}>
                        <td>{row.id}</td>
                        <td>{row.name}</td>
                        <td>{row.value}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
};

export default DataTable;
