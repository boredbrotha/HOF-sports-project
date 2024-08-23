import './App.css';
import Home from "./components/Home"
import Login from "./components/Login"
import Signup from "./components/Signup"
import Verify from "./components/Verify"
import Forgot from "./components/Forgot"
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";

function App() {
  return (
    <div className = "App">
      <Router>
        <Routes>
          <Route path= "/login" element= {<Login/>} />
          <Route path= "/signup" element= {<Signup/>} />
          <Route path= "/" element= {<Home/>} />
          <Route path = "/verify" element = {<Verify/>} />
          <Route path = "/forgot" element = {<Forgot/>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
