import React from 'react';
import SVGMap from '../components/SVGMap.tsx';
import paths from '../components/pathes.tsx';

const App: React.FC = () => {
    return (
        <div>
            <SVGMap paths={paths} />
        </div>
    );
};

export default App;