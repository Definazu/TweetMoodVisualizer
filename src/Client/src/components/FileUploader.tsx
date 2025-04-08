import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled, { keyframes } from 'styled-components';

// Animations
const fadeIn = keyframes`
    from { opacity: 0; transform: translate(-50%, -20px); }
    to { opacity: 1; transform: translate(-50%, 0); }
`;

const fadeOut = keyframes`
    from { opacity: 1; transform: translate(-50%, 0); }
    to { opacity: 0; transform: translate(-50%, -20px); }
`;

// Styled Components
const Container = styled.div`
    max-width: 550px;
    margin: 40px auto;
    padding: 30px;
    background: #1e1e1e;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #ddd;
`;

const Title = styled.h2`
    color: #fff;
    margin-bottom: 24px;
    text-align: center;
    font-weight: 600;
`;

const FileInput = styled.input`
    width: 100%;
    max-width: 500px;
    padding: 12px;
    margin-bottom: 20px;
    border: 2px dashed #3a7bd5;
    border-radius: 8px;
    background-color: #2d2d2d;
    color: #ddd;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
        border-color: #5a9be5;
        background-color: #333;
    }

    &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
`;

const UploadButton = styled.button`
    width: 100%;
    padding: 14px;
    background: ${props => props.disabled ? '#555' : '#3a7bd5'};
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;

    &:hover {
        background: ${props => props.disabled ? '#555' : '#4a8be5'};
        transform: ${props => props.disabled ? 'none' : 'translateY(-2px)'};
    }

    &:active {
        transform: ${props => props.disabled ? 'none' : 'translateY(0)'};
    }
`;

const ErrorMessage = styled.div`
    color: #ff6b6b;
    margin-top: 16px;
    padding: 12px;
    background: rgba(255, 0, 0, 0.1);
    border-radius: 6px;
    font-size: 14px;
`;

const FlashMessage = styled.div<{ $isVisible: boolean }>`
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 16px 24px;
    background: #2ecc71;
    color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    animation: ${props => props.$isVisible ? fadeIn : fadeOut} 0.3s forwards;
    display: flex;
    align-items: center;
    gap: 10px;
`;

const Spinner = styled.div`
    width: 18px;
    height: 18px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 1s ease-in-out infinite;
    margin-right: 8px;

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;

const FileUploader: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [showFlash, setShowFlash] = useState(false);

    useEffect(() => {
        let timer: ReturnType<typeof setTimeout>;
        if (showFlash) {
            timer = setTimeout(() => {
                setShowFlash(false);
            }, 3000);
        }
        return () => clearTimeout(timer);
    }, [showFlash]);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setError(null);
        const file = e.target.files?.[0];

        if (!file) {
            setError('Файл не выбран');
            return;
        }

        if (!file.name.endsWith('.txt')) {
            setError('Поддерживаются только .txt файлы');
            return;
        }

        setSelectedFile(file);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError('Файл не выбран');
            return;
        }

        setIsUploading(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', selectedFile);

            const response = await axios.post(
                'http://localhost:5001/upload',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                    timeout: 10000,
                }
            );

            console.log('Upload successful:', response.data);
            setShowFlash(true);
            setSelectedFile(null);
            // Reset file input
            const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
            if (fileInput) {
                fileInput.value = '';
            }
        } catch (err) {
            console.error('Upload error:', err);
            setError(
                axios.isAxiosError(err)
                    ? err.response?.data?.error || err.message || 'Ошибка загрузки файла'
                    : 'Неизвестная ошибка'
            );
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <>
            <FlashMessage $isVisible={showFlash}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                     xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                          stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Файл успешно загружен!
            </FlashMessage>

            <Container>
                <Title>Загрузка файла</Title>

                <FileInput
                    type="file"
                    onChange={handleFileChange}
                    accept=".txt"
                    disabled={isUploading}
                />

                <UploadButton
                    onClick={handleUpload}
                    disabled={!selectedFile || isUploading}
                >
                    {isUploading ? (
                        <>
                            <Spinner />
                            Отправка...
                        </>
                    ) : 'Загрузить файл'}
                </UploadButton>

                {error && <ErrorMessage>{error}</ErrorMessage>}
            </Container>
        </>
    );
};

export default FileUploader;