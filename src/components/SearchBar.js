import { useState } from "react"

const SearchBar=()=>{
    const [searchText,setSearchText]=useState("");
    const [isChanging,setIsChanging]=useState(false);
    
    const onSearchChange=(event)=>{
        setSearchText((target)=>event);
        if(searchText!=="") setIsChanging(true);
        else setIsChanging(false);
    }
    const searchEvent=(value)=>{

    }
    
    const onSearchClick=(event)=>{
        event.preventDafault();
        searchEvent(searchText);
        setSearchText("");
    }
    return(
        <div className="search_container">
            <input className="search_text_input" type="text" value={searchText} onChange={onSearchChange} placeholder="검색어를 입력하세요"/>
            <div className="search_submit" onClick={onSearchClick}>검색</div>
            
        </div> 
    )
}

export default SearchBar;