import React, { useEffect, useRef, useState } from 'react';
import "../styles/SVGMapStyles.css"
// Интерфейс для данных пути
interface PathData {
    id: string;
    dataName: string;
    dataId: string;
    d: string;
    style?: React.CSSProperties;
}

interface SVGMapProps {
    paths: PathData[];
}

const SVGMap: React.FC<SVGMapProps> = ({ paths }) => {
    const pathRefs = useRef<(SVGPathElement | null)[]>([]);
    const [hoveredState, setHoveredState] = useState<string | null>(null);

    useEffect(() => {
        // После рендеринга вычисляем центр для каждого пути и позиционируем текст
        pathRefs.current.forEach((path, index) => {
            if (path) {
                const bbox = path.getBBox();
                const textElement = document.getElementById(`text-${paths[index].id}`);
                if (textElement) {
                    textElement.setAttribute('x', String(bbox.x + bbox.width / 2));
                    textElement.setAttribute('y', String(bbox.y + bbox.height / 2));
                }
            }
        });
    }, [paths]);

    return (
        <>
            <style>
                {`
    @keyframes fadein {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    `}
            </style>
            <svg
                xmlns="http://www.w3.org/2000/svg"
                height="589px"
                width="1000px"
                viewBox="0 0 1000 589"
                style={{strokeLinejoin: 'round', stroke: '#000', fill: 'none'}}
            >
                {paths.map((path, index) => (
                    <React.Fragment key={path.id}>
                        <path
                            ref={(el) => {
                                pathRefs.current[index] = el; // Сохраняем ссылку на путь
                            }}
                            id={path.id}
                            data-name={path.dataName}
                            data-id={path.dataId}
                            d={path.d}
                            style={path.style}
                            onMouseEnter={() => setHoveredState(path.id)} // Показываем текст при наведении
                            onMouseLeave={() => setHoveredState(null)} // Скрываем текст при уходе курсора
                        />
                        <text
                            id={`text-${path.id}`}
                            textAnchor="middle"
                            className="hover-text"
                            style={{
                                pointerEvents: 'none',
                                opacity: hoveredState === path.id ? 1 : 0, // Используем opacity для анимации
                                animation: hoveredState === path.id ? 'fadein 0.25s ease-in-out' : 'none', // Правильное написание ease-in-out
                                transition: 'opacity 0.5s ease-in-out', // Добавляем transition для плавного исчезновения
                            }}
                        >
                            {path.dataId}
                        </text>
                    </React.Fragment>
                ))}
            </svg>
        </>

    );
};

export default SVGMap;