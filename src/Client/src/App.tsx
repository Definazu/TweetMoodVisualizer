
import './App.css'

import SVGMap from "./components/SVGMap.tsx";
import paths from "./components/pathes.tsx";


function App() {

  return (
    <div>
      <SVGMap paths={paths} />
    </div>
  )
}

export default App
