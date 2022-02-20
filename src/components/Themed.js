import { useState,useEffect } from "react";
import News from "components/News";
import { 
    Button, 
    ButtonGroup} from "react-bootstrap";

const Themed=({theme})=>{
    const[newslist,setNewslist]=useState([]);
    //분류 리스트 가져오기
    useEffect=()=>{
        //페이지 렌더할 때 NewsCrawler.py에서 뉴스 리스트 받아오기
        setNewslist();
    }
    
    return(
        <div className="themed_container">
            <div className="themed_newslists">
                {newslist.map((news)=>
                    <News newsObj={news}/>
                )}
            </div>
        </div>
    )
}
export default Themed;

