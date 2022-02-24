import {useState} from "react";
import { Carousel } from "react-bootstrap";

const SliderContent=({contentObj})=>{
    return(
        <Carousel variant="dark">
            <Carousel.Item>
                <a href={contentObj.src}>
                    <img
                        className="d-block w-100"
                        src={contentObj.img}
                        alt={contentObj.title}
                    />
                </a>
                <Carousel.Caption>
                    <h3>{contentObj.title}</h3>
                    <p>{contentObj.tags.map((tag)=>
                        <span>#{tag} </span>
                    )}</p>
                </Carousel.Caption>
            </Carousel.Item>
        </Carousel>
    )
}

export default SliderContent;