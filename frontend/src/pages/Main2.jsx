//홈_로그인 후
//'/home'을 주소 뒤에 붙인다
import React from 'react'
import HomeTop from '../components/HomeTop'
import HomeNew from '../components/HomeNew'
import HomeLogo from '../components/HomeLogo'
import HomeClass from '../components/HomeClass'



function Main2() {
    return (
        <div>
            <HomeTop/>
            <HomeLogo></HomeLogo>
            <HomeClass></HomeClass>
            <HomeNew></HomeNew>
        </div>
    )
}

export default Main2