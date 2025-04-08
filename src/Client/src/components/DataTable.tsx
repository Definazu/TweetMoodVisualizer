import React, { useState, useEffect } from 'react';
import axios from "axios";

const DataTable: React.FC = () => {
    const [tables, setTables] = useState<string[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await axios.get<{ tables: string[] }>('http://localhost:5001/tables');
            setTables(response.data.tables);
            console.log(response.data);
        } catch (error) {
            console.error('Ошибка при загрузке данных:', error);
            setError('Не удалось загрузить данные');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    if (loading) {
        return <div>Загрузка данных...</div>;
    }

    if (error) {
        return (
            <div>
                <div style={{ color: 'red' }}>{error}</div>
                <button onClick={fetchData}>Повторить попытку</button>
            </div>
        );
    }

    return (
        <div style={{ padding: '20px', marginTop: '50px' }}>
            <button
                onClick={fetchData}
                style={{
                    marginBottom: '20px',
                    padding: '8px 16px',
                    backgroundColor: '#4CAF50',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                }}
            >
                Обновить таблицу
            </button>

            <table style={{
                width: '100%',
                borderCollapse: 'collapse',
                boxShadow: '0 0 10px rgba(0,0,0,0.1)'
            }}>
                <thead>
                <tr style={{ backgroundColor: '#242424' }}>
                    <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>#</th>
                    <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Имя таблицы</th>
                </tr>
                </thead>
                <tbody>
                {tables.length > 0 ? (
                    tables.map((tableName, index) => (
                        <tr key={index} style={{ borderBottom: '1px solid #ddd' }}>
                            <td style={{ padding: '12px' }}>{index + 1}</td>
                            <td style={{ padding: '12px' }}>{tableName}</td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan={2} style={{ padding: '12px', textAlign: 'center' }}>
                            Нет данных для отображения
                        </td>
                    </tr>
                )}
                </tbody>
            </table>
        </div>
    );
};

export default DataTable;
