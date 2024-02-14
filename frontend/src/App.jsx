import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Classchat from './pages/Classchat'
import Contentchat from './pages/Contentchat'
import Createaccount from './pages/Createaccount'
import Login from './pages/Login'
import Main1 from './pages/Main1'
import Main2 from './pages/Main2'

const App = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/classchat' element={<Classchat />} />
                <Route path='/contentschat' element={<Contentchat />} />
                <Route path='/createaccount' element={<Createaccount />} />
                <Route path='/login' element={<Login />} />
                <Route path='/' element={<Main1 />} />
                <Route path='/home' element={<Main2 />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;