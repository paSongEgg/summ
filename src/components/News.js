const News=({newsObj})=>{
    const onNewsClick=()=>{

    }

    return(
        <div className="news_contents" onClick={onNewsClick}>
            <span>{newsObj.title}</span>
            <span>{newsObj.date}</span>
        </div>
    )
}

export default News;