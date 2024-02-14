//홈_로그인 전
import React from 'react'
import Main1_left from '../components/Main1_left'
import Main1_right from '../components/Main1_right'
import styles from '../css/main1.module.css'

const Main1 = () => {
    return (
        <div className={styles.home}>
            <div className={styles.container}>
                <Main1_left/>
                <Main1_right/>
            </div>
        </div>
    )
}

export default Main1