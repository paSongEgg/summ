import { useState } from "react";
import News from "components/News";
const TodayNews=()=>{
    const[newslist,setNewslist]=useState([]);

    return(
        <div className="todaynews_container">
            <div className="themed_newslists">
                {newslist.map((news)=>
                    <News newsObj={news}/>
                )}
            </div>
        </div>
    )
}
export default TodayNews;