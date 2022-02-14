import SearchBar from "components/SearchBar";
import Themed from "components/Themed";
import TodayNews from "components/TodayNews";
import { useState } from "react";
const Home=()=>{
    const [isToday,setIsToday]=useState(true);
    const onOptionClick=()=>setIsToday((prev)=>!prev);
    return(
        <section className="home_container">
            <div className="home_button_changeOption" onClick={onOptionClick}>click</div>
            <SearchBar/>
            {isToday?(
                <TodayNews/>
            ):(
                <Themed/>
            )}
        </section>
    )
}

export default Home;