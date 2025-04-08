import React, { useEffect, useRef, useMemo } from 'react';
import "../styles/SVGMapStyles.css";

interface PathData {
    id: string;
    dataName: string;
    dataId: string;
    d: string;
    style?: React.CSSProperties;
}

interface SVGMapProps {
    paths: PathData[];
    colorData: Record<string, string>;
}

const SVGMap: React.FC<SVGMapProps> = ({ paths, colorData }) => {
    const pathRefs = useRef<(SVGPathElement | null)[]>([]);
    const isColored = useMemo(() => {
        return paths.some((path) => {
            const color = colorData[path.id];
            return color && color.toLowerCase() !== "#c2c2c2";
        });
    }, [paths, colorData]);

    useEffect(() => {
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
    }, [paths, colorData]);

    const getFillColor = (path: PathData) => {
        return colorData[path.id] || path.style?.fill || "#f9f9f9";
    };

    return (
        <div className="svg-map-container">
            {/* Неоновая подсветка */}
            <div className={`neon-lamp ${isColored ? "neon-colored" : "neon-gray"}`} />
            <svg
                xmlns="http://www.w3.org/2000/svg"
                height="589px"
                width="1000px"
                viewBox="0 0 1000 589"
                className="us-map-svg"
            >
                {paths.map((path, index) => (
                    <React.Fragment key={`${path.id}-${index}`}>
                        <path
                            ref={(el) => {
                                pathRefs.current[index] = el;
                            }}
                            id={path.id}
                            data-name={path.dataName}
                            data-id={path.dataId}
                            d={path.d}
                            style={{
                                ...path.style,
                                fill: getFillColor(path),
                                transition: "fill 0.3s ease-in-out"
                            }}
                            className="state-path"
                        />
                        <text
                            id={`text-${path.id}`}
                            textAnchor="middle"
                            className="state-label"
                        >
                            {path.dataId}
                        </text>
                    </React.Fragment>
                ))}
            </svg>
        </div>
    );
};

export default SVGMap;
