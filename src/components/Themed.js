import { constructor, useState } from "react";
import News from "components/News";

const Themed=()=>{
    const [themes,setThemes]=useState([]);
    const[newslist,setNewslist]=useState([]);
    const [clicked,setClicked]=useState("");
    //분류 리스트 가져오기
    constructor();
    const onThemeClick=()=>{

    }
    return(
        <div className="themed_container">
            <div className="themed_selectBoxes">
                {themes.map((theme)=>
                    <div className="themed_selectBox" onClick={onThemeClick}>
                        <span>{theme}</span>
                    </div>
                )}
            </div>
            <div className="themed_newslists">
                {newslist.map((news)=>
                    <News newsObj={news}/>
                )}
            </div>
        </div>
    )
}
export default Themed;

