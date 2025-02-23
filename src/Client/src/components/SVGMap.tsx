import React from 'react';

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
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            height="589px"
            width="1000px"
            viewBox="0 0 1000 589"
            style={{ strokeLinejoin: 'round', stroke: '#000', fill: 'none' }}
        >
            {paths.map((path) => (
                <path
                    key={path.id}
                    id={path.id}
                    data-name={path.dataName}
                    data-id={path.dataId}
                    d={path.d}
                    style={path.style}
                />
            ))}
        </svg>
    );
};

export default SVGMap;