import Themed from "components/Themed";
import TodayNews from "components/TodayNews";
import { useState } from "react";
import styles from "../styles/Home.module.css"

const Home=()=>{
    return(
        <section className={styles.home_container}>
            <div className={styles.theme}>
                <button className={styles.home_button_changeOption}>통합</button>            
                <button className={styles.button_theme}>정치</button>
                <button className={styles.button_theme}>경제</button>
                <button className={styles.button_theme}>사회</button>
                <button className={styles.button_theme}>생활/문화</button>
                <button className={styles.button_theme}>IT/과학</button>
                <button className={styles.button_theme}>세계</button>
            </div>
        </section>
    )
}

export default Home;