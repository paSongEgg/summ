import { useState } from "react";
import Themed from "components/Themed";
import TodayNews from "components/TodayNews";
import styles from "../styles/Home.module.css"

const Home=()=>{
    const [isToday,setIsToday]=useState(true);
    const onOptionClick=()=>setIsToday((prev)=>!prev);
    return(
        <section className={styles.home_container}>
            <button className={styles.home_button_changeOption} onClick={onOptionClick}>통합</button>            
            {isToday?(
                <TodayNews/>
            ):(
                <div className={styles.theme}>
                    <button className={styles.button_theme}>정치</button>
                    <button className={styles.button_theme}>경제</button>
                    <button className={styles.button_theme}>사회</button>
                    <button className={styles.button_theme}>생활/문화</button>
                    <button className={styles.button_theme}>IT/과학</button>
                    <button className={styles.button_theme}>세계</button>
                    <Themed/>
                </div>
            )}
        </section>
    )
}

export default Home;