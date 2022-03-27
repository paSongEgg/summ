import Form from 'react-bootstrap/Form'

const Floating = () => {
    return(
        <section>
            <div>
                <form method="get" oninput="news_num = number.valueAsNumber">
                    <label><input type="radio" name="sort" value="view"/> 1. 많이 본&nbsp;&nbsp;&nbsp;</label>
                    <label><input type="radio" name="sort" value="comment"/> 2. 댓글 많은</label>
                    <br></br>
                    <br></br>
                    <label for="num">뉴스 개수&nbsp;&nbsp;</label>
                    <input type="range" id="num" name="number" min="10" max="120" step="20"/>
                    &nbsp;&nbsp;&nbsp;
                    <output for="num" name="news_num"></output>
                    <input type="submit" value="GO" onClick=''></input>
                </form>
            </div>
        </section>
    )
}

export default Floating;