// import React from 'react';
// import { MapContainer, TileLayer, Polygon } from 'react-leaflet';
// import 'leaflet/dist/leaflet.css';
// import polygonsList from '../components/polygons.tsx'; // Импортируем ваш JSON-файл
//
// const MapComponent: React.FC = () => {
//     return (
//         <MapContainer
//             center={[37.8, -96]}
//             zoom={4}
//             style={{ height: '100vh', width: '100%' }}
//         >
//             <TileLayer
//                 url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//                 attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//             />
//
//             {Object.entries(polygonsList).map(([state, polygons]) => (
//                 polygons.map((polygon, index) => (
//                     <Polygon
//                         key={`${state}-${index}`}
//                         positions={polygon}
//                         color="blue"
//                         fillColor="lightblue"
//                         fillOpacity={0.4}
//                     />
//                 ))
//             ))}
//         </MapContainer>
//     );
// };
//
// export default MapComponent;