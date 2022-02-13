import {useState} from "react";
import SliderContent from 'components/SliderContent.js';
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
            </div>
        </section>
    )
}
export default Slider;