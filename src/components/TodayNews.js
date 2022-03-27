import { useState,useEffect } from "react";
import News from "components/News";
import styles from "../styles/Home.module.css"

const TodayNews=()=>{
    const[newslist,setNewslist]=useState([]);
    useEffect=()=>{
        //페이지 렌더할 때 NewsCrawler.py에서 뉴스 리스트 받아오기
    }
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