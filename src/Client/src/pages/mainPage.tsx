import React from 'react';
import SVGMap from '../components/SVGMap.tsx';
import paths from '../components/pathes.tsx';
import DataTable from "../components/DataTable.tsx";

const App: React.FC = () => {
    return (
        <>
            <SVGMap paths={paths} />
            <DataTable/>
        </>
    );
};

export default App;