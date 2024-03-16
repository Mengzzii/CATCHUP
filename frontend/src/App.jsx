import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Main1 from "./pages/Main1";
import Main2 from "./pages/Main2";
import SignUp from "./pages/SignUp";
import Classroomchat from "./pages/Classroomchat";
import Newclassroomchat from "./pages/Newclassroomchat";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/new/class/:classid" element={<Newclassroomchat />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Main1 />} />
        <Route path="/home" element={<Main2 />} />
        <Route path="/class/:classid" element={<Classroomchat />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
