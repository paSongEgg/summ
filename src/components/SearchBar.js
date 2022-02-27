import styles from "../styles/SearchBar.module.css"

const SearchBar=()=>{
    return(
        <div className={styles.search_bar}>
            <form method="get">
                <input className={styles.search_box} size="40" type="text" placeholder="Search keyword"/>
                <input className={styles.search_btn} value="검색" type="submit"/>
            </form>
        </div>
    )
}

export default SearchBar;