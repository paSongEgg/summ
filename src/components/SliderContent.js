import {useState} from "react";

const SliderContent=({contentObj})=>{
    const [contents,setContents]=useState([]);

    const onContentClick=()=>{

    }

    return(
        <div className="sliderContent_contents">
            {contents.map((content)=>
                <div className="sliderContent_content" onClick={onContentClick}>
                    <div className="sliderContent_tags">
                    {content.tags.map((tag)=>{
                        <span className="sliderContent_tag">{tag}</span>
                    })}
                    </div>
                    <div className="sliderContent_background">
                        {content.image}
                    </div>
                </div>
            )}
        </div>
    )
}

export default SliderContent;