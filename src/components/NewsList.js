import styles from "../styles/NewsList.module.css"
import data from "../public/data.json"

const NewsList = () => {
    // let xhttp = new XMLHttpRequest();

    // function jsonfunc(jsonText) {
    //     let arrDate = new Array();
    //     let arrPress = new Array();
    //     let arrRank = new Array();
    //     let arrViews = new Array();
    //     let arrSection = new Array();
    //     let arrTitle = new Array();
    //     let arrKeywords = new Array();

    //     let json = JSON.parse(jsonText);

    //     let i = 0;

    //     for(i = 0; i < json.length; i++) {
    //         arrDate[i] = json[i].date;
    //         arrPress[i] = json[i].press;
    //         arrRank[i] = json[i].ranking;
    //         arrViews[i] = json[i].views;
    //         arrSection[i] = json[i].section;
    //         arrTitle[i] = json[i].title;
    //         arrKeywords[i] = json[i].keyword;
    //     }

    //     let table = document.getElementById('news_table');

    //     for(i = 0; i < arrTitle.length; i++) {
    //         let tr = document.createElement('tr');

    //         let td1 = document.createElement('td');
    //         td1.appendChild(document.createTextNode(arrRank[i] + ""));

    //         let td2 = document.createElement('td');
    //         td1.appendChild(document.createTextNode(arrDate[i] + ""));

    //         let td3 = document.createElement('td');
    //         td1.appendChild(document.createTextNode(arrPress[i] + ""));

    //         let td4 = document.createElement('td');
    //         td1.appendChild(document.createTextNode(arrViews[i] + ""));

    //         let td5 = document.createElement('td');
    //         td1.appendChild(document.createTextNode(arrTitle[i] + ""));

    //         let td6 = document.createElement('td');
    //         td1.appendChild(document.createTextNode(arrKeywords[i] + ""));

    //         tr.appendChild(td1);
    //         tr.appendChild(td2);
    //         tr.appendChild(td3);
    //         tr.appendChild(td4);
    //         tr.appendChild(td5);
    //         tr.appendChild(td6);

    //         table.appendChild(tr);
    //     }
    // }
    
    // xhttp.onreadystatechange = function() {
    //     if(xhttp.readyState == 4 && xhttp.status == 200) {
    //         jsonfunc(this.responseText);
    //     }
    // }
    // xhttp.open("GET", "data.json", true);
    // xhttp.send();

    return(
        <div className={styles.news_table}>
            <table id="news_table">
                <thead className={styles.table_head}>
                    <tr>
                        <th>No.&nbsp;</th>
                        <th>날짜&nbsp;</th>
                        <th>언론사&nbsp;</th>
                        <th>조회수/댓글&nbsp;</th>
                        <th>제목&nbsp;</th>
                        <th>키워드</th>
                    </tr>
                </thead>
                <tbody>
                    <td></td>
                </tbody>
            </table>
        </div>
    )
}

export default NewsList;