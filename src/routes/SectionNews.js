import SearchBar from "components/SearchBar";
import Themed from "components/Themed";
import TodayNews from "components/TodayNews";
import NewsList from "components/NewsList";
import { useState } from "react";
import styles from "styles/SectionNews.module.css"
import News from "components/News";
import Floating from "components/Floating";

const SectionNews=()=>{
    const themes=["정치","경제","사회","생활/문화","IT/과학","세계"];
    const [isThemeClicked,setIsThemeClicked]=useState(false);
    const [clickedTheme,setClickedTheme]=useState("");

    const onThemeClick=(e)=>{
        setClickedTheme(e.target.id);
        setIsThemeClicked(true);
    }

    const onAllClick=()=>{
        setIsThemeClicked(false);
    }

    return(
        <section className={styles.home_container}>
            <div className={styles.theme}>
                <button onClick={onAllClick} className={styles.home_button_changeOption} id="통합">통합</button>       
                {themes.map((theme)=>(
                    <button onClick={onThemeClick} key={theme} id={theme} className={styles.button_theme}>{theme}</button>
                ))}
            </div>
            {/* {(isThemeClicked)?
                <Themed theme={clickedTheme}/>:
                <TodayNews/>
            } */}
            <div className={styles.floating}>
                <Floating/>
            </div>
            <div className={styles.news_list}>
                <NewsList/>
            </div>
        </section>
    )
}

export default SectionNews;