import React, { useState, useEffect } from 'react';
import axios from "axios";
import styled, { keyframes, css } from 'styled-components';

interface DataTableProps {
    onColorizeMap: (tableName: string) => void;
    onClearMap: () => void;
}

const fadeIn = keyframes`
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
`;

const pulse = keyframes`
    0% { transform: scale(1); }
    50% { transform: scale(1.03); }
    100% { transform: scale(1); }
`;

const TableContainer = styled.div`
    padding: 2rem;
    margin-top: 2rem;
    background: #1e1e1e;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    animation: ${fadeIn} 0.5s ease-out;
`;

const ButtonGroup = styled.div`
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
`;

const ActionButton = styled.button<{ $active?: boolean }>`
    padding: 0.75rem 1.5rem;
    background: ${props => props.$active ? '#3a7bd5' : '#4CAF50'};
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

    &:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        background: ${props => props.$active ? '#4a8be5' : '#5CBF60'};
    }

    &:disabled {
        background: #555;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
`;

const StyledTable = styled.table`
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    animation: ${fadeIn} 0.7s ease-out;
`;

const TableHeader = styled.thead`
    th {
        padding: 1rem;
        text-align: left;
        background: #2d2d2d;
        color: #fff;
        font-weight: 600;
        position: sticky;
        top: 0;
        z-index: 10;

        &:first-child {
            border-top-left-radius: 8px;
        }

        &:last-child {
            border-top-right-radius: 8px;
        }
    }
`;

const TableRow = styled.tr<{ $selected: boolean }>`
    transition: all 0.3s ease;
    cursor: pointer;
    background: ${props => props.$selected ? 'rgba(58, 123, 213, 0.2)' : 'transparent'};

    &:hover {
        background: rgba(255, 255, 255, 0.05);
    }

    &:active {
        transform: scale(0.98);
    }

    td {
        padding: 1.2rem 1rem;
        border-bottom: 1px solid #333;
        color: ${props => props.$selected ? '#fff' : '#ddd'};
        transition: all 0.3s ease;
        position: relative;
    }

    &:last-child td {
        border-bottom: none;
    }

    ${props => props.$selected && css`
    animation: ${pulse} 0.5s ease;
    transform-origin: center;
    box-shadow: 0 0 0 2px rgba(58, 123, 213, 0.5);
    border-radius: 8px;
    margin: 8px 0;
    
    td:first-child {
      border-left: 3px solid #3a7bd5;
      border-top-left-radius: 8px;
      border-bottom-left-radius: 8px;
    }
    
    td:last-child {
      border-right: 3px solid #3a7bd5;
      border-top-right-radius: 8px;
      border-bottom-right-radius: 8px;
    }
  `}
`;

const SelectIndicator = styled.div<{ $selected: boolean }>`
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: ${props => props.$selected ? '#3a7bd5' : '#444'};
    border: 2px solid ${props => props.$selected ? '#5a9be5' : '#666'};
    transition: all 0.3s ease;
`;

const LoadingText = styled.div`
    padding: 2rem;
    text-align: center;
    color: #aaa;
    font-size: 1.2rem;
`;

const ErrorContainer = styled.div`
    padding: 2rem;
    text-align: center;
    color: #ff6b6b;
    background: rgba(255, 0, 0, 0.1);
    border-radius: 8px;
    margin: 1rem 0;
`;

const DataTable: React.FC<DataTableProps> = ({ onColorizeMap , onClearMap }) => {
    const [tables, setTables] = useState<string[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedTable, setSelectedTable] = useState<string | null>(null);

    const fetchData = async () => {
        window.scrollTo({
            top: 1400,
            behavior: "smooth"
        });
        try {
            setLoading(true);
            setError(null);
            const response = await axios.get<{ tables: string[] }>(`http://localhost:5001/tables`);
            setTables(response.data.tables);
        } catch (error) {
            console.error('Ошибка при загрузке данных:', error);
            setError('Не удалось загрузить данные');
        } finally {
            setLoading(false);
        }
    };

    const handleColorizeClick = () => {
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
        if (selectedTable) {
            onColorizeMap(selectedTable);
        }
    };

    const handleRowClick = (tableName: string) => {

        setSelectedTable(tableName === selectedTable ? null : tableName);
    };

    useEffect(() => {
        fetchData();
    }, []);

    if (loading) {
        return <LoadingText>Загрузка данных...</LoadingText>;
    }

    if (error) {
        return (
            <ErrorContainer>
                <div style={{ marginBottom: '1rem' }}>{error}</div>
                <ActionButton onClick={fetchData}>Повторить попытку</ActionButton>
            </ErrorContainer>
        );
    }

    return (
        <TableContainer>
            <ButtonGroup>
                <ActionButton onClick={fetchData}>
                    Обновить таблицу
                </ActionButton>

                <ActionButton
                    onClick={handleColorizeClick}
                    disabled={!selectedTable}
                    $active
                >
                    Раскрасить карту
                </ActionButton>

                <ActionButton onClick={onClearMap} style={{ background: '#c0392b' }}>
                    Очистить карту
                </ActionButton>
            </ButtonGroup>


            <StyledTable>
                <TableHeader>
                    <tr>
                        <th>#</th>
                        <th>Имя таблицы</th>
                        <th></th>
                    </tr>
                </TableHeader>
                <tbody>
                {tables.map((tableName, index) => (
                    <TableRow
                        key={tableName}
                        $selected={selectedTable === tableName}
                        onClick={() => handleRowClick(tableName)}
                    >
                        <td>{index + 1}</td>
                        <td>{tableName}</td>
                        <td>
                            <SelectIndicator $selected={selectedTable === tableName} />
                        </td>
                    </TableRow>
                ))}
                </tbody>
            </StyledTable>
        </TableContainer>
    );
};

export default DataTable;