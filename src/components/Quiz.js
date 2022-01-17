import React, { useState, useEffect } from "react";
import styles from "./Quiz.module.css";
import "bootstrap/dist/css/bootstrap.css";
import { Link } from "react-router-dom";
import axios from "axios";
import {
  Container,
  Row,
  Button,
  Pagination,
  Tabs,
  Tab,
  Spinner,
  Table,
} from "react-bootstrap";

function Quiz() {
  const [key, setKey] = useState("lastQuiz");
  const [id, setID] = useState("");

  const [lastquiz, setLastQuiz] = useState("lastQuiz");

  const onChange = (e) => {
    setLastQuiz(e.target.value);
  };

  let active = 2;
  let items = [];

  for (let number = 1; number <= 5; number++) {
    items.push(
      <Pagination.Item key={number} active={number === active}>
        {number}
      </Pagination.Item>
    );
  }

  useEffect(() => {
    axios.get("/quiz/test").then((res) => {
      console.log(res);
    });
  }, []);

  const [inputData, setInputData] = useState([
    {
      id: "",
      quizTitle: "",
      userResult: "",
    },
  ]);

  useEffect(async () => {
    try {
      const res = await axios.get("/quiz/test");
      const _Data = await res.data.map((rowData) => ({
        id: rowData.id,
        quizTitle: rowData.quizTitle,
        userResult: rowData.userResult,
      }));
      // 선언된 _inputData 를 최초 선언한 inputData 에 concat 으로 추가
      setInputData(inputData.concat(_Data));
    } catch (e) {
      console.error(e.message);
    }
  }, []);

  return (
    <Container className={styles.nanumGothicFont}>
      <Row className="d-flex justify-content-center">
        <span className="mt-5 d-flex justify-content-center border">
          <h1>Quiz</h1>
        </span>

        <Row className="m-5 row-cols-1 d-flex justify-content-center">
          <Spinner animation="border" role="status" className="m-5"></Spinner>
          <span className="d-flex justify-content-center">
            <Button variant="success">퀴즈 생성하기</Button>
          </span>
        </Row>

        <Row className="m-3 d-flex row-cols-1 justify-content-center">
          <Tabs activeKey={key} onSelect={(k) => setKey(k)} className="mb-2">
            <Tab eventKey="lastQuiz" title="지난 퀴즈" onClick={onChange}>
              <Container>
                <Row className="list-group">
                  <a href="lastquiz" class="list-group-item bg-light">
                    지난 퀴즈 1
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    지난 퀴즈 2
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    지난 퀴즈 3
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    지난 퀴즈 4
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    지난 퀴즈 5
                  </a>
                </Row>

                <Table className="invisible">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>#</th>
                      <th>#</th>
                      <th>#</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td className="listId" th></td>
                      <td className="listQuizTitle" th></td>
                      <td className="listUserResult" th></td>
                    </tr>
                    {id !== 0 ? (
                      inputData.map(
                        (rowData) =>
                          // 최초 선언한 기본값은 나타내지 않음
                          rowData.id !== "" && (
                            <tr>
                              <td className="listId">
                                <Link to={`${rowData.id}`}>{rowData.id}</Link>
                              </td>
                              <td className="listQuizTitle">
                                <Link to={`${rowData.id}`}>
                                  {rowData.quizTitle}
                                </Link>
                              </td>
                              <td className="listUserResult">
                                <Link to={`${rowData.id}`}>
                                  {rowData.userResult}
                                </Link>
                              </td>
                            </tr>
                          )
                      )
                    ) : (
                      <tr>
                        <td className="listId"></td>
                        <td className="listQuizTitle noData">
                          작성된 글이 없습니다.
                        </td>
                        <td className="listUserResult noData"></td>
                      </tr>
                    )}
                  </tbody>
                </Table>
              </Container>
            </Tab>

            <Tab eventKey="wrong" title="오답">
              <Container>
                <Row className="list-group">
                  <a href="#" class="list-group-item bg-light">
                    오답 1
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    오답 2
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    오답 3
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    오답 4
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    오답 5
                  </a>
                </Row>
              </Container>
            </Tab>
          </Tabs>
        </Row>

        <Pagination className="m-3 d-flex justify-content-center">
          <Pagination.First tabindex="-1" />
          <Pagination.Prev />
          <Pagination.Item active>{1}</Pagination.Item>
          <Pagination.Item>{2}</Pagination.Item>
          <Pagination.Item>{3}</Pagination.Item>
          <Pagination.Item>{4}</Pagination.Item>
          <Pagination.Item>{5}</Pagination.Item>
          <Pagination.Next />
          <Pagination.Last />
        </Pagination>
      </Row>
    </Container>
  );
}

export default Quiz;
