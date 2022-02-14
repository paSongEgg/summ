import {useState} from "react";
import SliderContent from 'components/SliderContent.js';
import { Carousel } from "react-bootstrap";

const Slider =()=>{
    const [contents,setContents]=useState([]);

    const slideAction=()=>{
        //if width>767(tablet~)
        //else (~mobile)
    }
    const onClick=()=>{

    }
    const onTouchMove=()=>{

    }

    return(
        <section className="slider_container">
            <div className="slider" >
                <div className="slider_button_left" onClick={onClick} ></div>
                <div className="slider_button_right" onClick={onClick}></div>
                <div className="slider_button_up" onClick={onClick}></div>
                <div className="slider_button_down" onClick={onClick}></div>
                <div className="slider_contents" onTouchMove={onTouchMove}>
                    {contents.map((content)=>(
                        <SliderContent contentObj={content}/>
                    ))}
                </div>
                <div>
                    <Carousel variant="dark">
                      <Carousel.Item>
                          <a href="http://www.sookmyung.ac.kr/bbs/sookmyungkr/164/28205/artclView.do?layout=unknown">
                            <img
                              className="d-block w-100"
                              src="img/3.png"
                              alt="First slide"
                            />
                          </a>
                        <Carousel.Caption>
                          <h3>뉴스 제목 1</h3>
                          <p>#해시태그1 #해시태그2 #해시태그3</p>
                        </Carousel.Caption>
                      </Carousel.Item>

                      <Carousel.Item>
                          <a href="http://www.sookmyung.ac.kr/bbs/sookmyungkr/164/28686/artclView.do?layout=unknown">
                            <img
                              className="d-block w-100"
                              src="img/4.png"
                              alt="Second slide"
                            />
                          </a>
                        <Carousel.Caption>
                        <h3>뉴스 제목 2</h3>
                          <p>#해시태그1 #해시태그2 #해시태그3</p>
                        </Carousel.Caption>
                      </Carousel.Item>

                      <Carousel.Item>
                          <a href="http://www.sookmyung.ac.kr/bbs/sookmyungkr/164/28688/artclView.do?layout=unknown">
                            <img
                              className="d-block w-100"
                              src="img/5.png"
                              alt="Third slide"
                            />
                          </a>
                        <Carousel.Caption>
                        <h3>뉴스 제목 3</h3>
                          <p>#해시태그1 #해시태그2 #해시태그3</p>
                        </Carousel.Caption>
                      </Carousel.Item>
                    </Carousel>
                </div>
            </div>
        </section>
    )
}
export default Slider;