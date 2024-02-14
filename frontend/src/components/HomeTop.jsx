import React from 'react'
import styles from '../css/hometop.module.css'

const HomeTop = () => {
    return (
        <>
        <button className={styles.userBt}>
            이화연 님
        </button>
        <svg className={styles.userIc} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" /></svg>
        </>
    )
}

export default HomeTop