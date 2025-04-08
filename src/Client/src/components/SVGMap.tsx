import React, { useEffect, useRef, useState } from 'react';
import "../styles/SVGMapStyles.css"
import axios from "axios";

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
    // const [hoveredState, setHoveredState] = useState<string | null>(null);
    const [colorData, setColorData] = useState<Record<string, string>>({});
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    useEffect(() => {
        const fetchColors = async () => {
            try {
                setLoading(true);
                const response = await axios.get(`http://localhost:5000/analyze/football_tweets2014`);
                setColorData(response.data);
                setError(null);
            } catch (error) {
                console.error("Error fetching color data:", error);
                setError("Failed to load color data");

                setColorData(Object.fromEntries(
                    paths.map(path => [path.id, path.style?.fill || "#f9f9f9"])
                ));
            } finally {
                setLoading(false);
            }
        };

        fetchColors();
    }, [paths]);

    useEffect(() => {
        if (loading) return;

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
    }, [paths, loading]);

    const getFillColor = (path: PathData) => {
        // Priority: API color > path style fill > default
        return colorData[path.id] || path.style?.fill || "#f9f9f9";
    };

    if (loading) {
        return <div className="loading-indicator">Loading map data...</div>;
    }

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    return (
        <div className="svg-map-container">
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
                            // onMouseEnter={() => setHoveredState(path.id)}
                            // onMouseLeave={() => setHoveredState(null)}
                        />
                        <text
                            id={`text-${path.id}`}
                            textAnchor="middle"
                            className={`state-label`}
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