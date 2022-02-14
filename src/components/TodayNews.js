import { useState } from "react";
import News from "components/News";
import styles from "../styles/Home.module.css"

const TodayNews=()=>{
    const[newslist,setNewslist]=useState([]);

    return(
        <div className={styles.todaynews_container}>
            <div className={styles.themed_newslists}>
                {newslist.map((news)=>
                    <News newsObj={news}/>
                )}
            </div>
        </div>
    )
}
export default TodayNews;