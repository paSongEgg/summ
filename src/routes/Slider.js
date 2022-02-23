import {useState,useEffect} from "react";
import SliderContent from 'components/SliderContent.js';

const Slider =()=>{
    const [contents,setContents]=useState([]);
    //아래는 테스트용 임시코드
    const testData=[
      {
        src:"http://www.sookmyung.ac.kr/bbs/sookmyungkr/164/28205/artclView.do?layout=unknown",
        img:"img/3.png",
        title:"뉴스 제목 1",
        tags:["해시태그1", "해시태그2", "해시태그3"]
      },
      {
        src:"http://www.sookmyung.ac.kr/bbs/sookmyungkr/164/28686/artclView.do?layout=unknown",
        img:"img/4.png",
        title:"뉴스 제목 2",
        tags:["해시태그1", "해시태그2", "해시태그3"]
      },
      {
        src:"http://www.sookmyung.ac.kr/bbs/sookmyungkr/164/28688/artclView.do?layout=unknown",
        img:"img/5.png",
        title:"뉴스 제목 3",
        tags:["해시태그1", "해시태그2", "해시태그3"]
      }]
    
    useEffect=()=>{
      //크롤러에서 contents 가져오기
      setContents(testData);
    }

    return(
        <section className="slider_container">
            <div className="slider" >
                <div>
                  {contents.map((content)=>(
                        <SliderContent contentObj={content}/>
                    ))}
                </div>
            </div>
        </section>
    )
}
export default Slider;